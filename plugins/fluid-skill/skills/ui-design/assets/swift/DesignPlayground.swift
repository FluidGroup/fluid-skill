// Structured randomization and the contact sheet, for a playground or a debug-only target.
// Copy this file next to the prototype. It compiles for iOS 17+ and macOS 14+ and never ships.
#if DEBUG
import SwiftUI

/// SplitMix64. The system generator cannot be seeded, and a contact sheet must come out the
/// same on every run.
public struct SeededGenerator: RandomNumberGenerator {
  private var state: UInt64

  public init(seed: UInt64) { state = seed }

  public mutating func next() -> UInt64 {
    state &+= 0x9E37_79B9_7F4A_7C15
    var z = state
    z = (z ^ (z >> 30)) &* 0xBF58_476D_1CE4_E5B9
    z = (z ^ (z >> 27)) &* 0x94D0_49BB_1331_11EB
    return z ^ (z >> 31)
  }
}

/// A legality rule. `rejects` returns true for a variant that must not be shown.
public struct VariantRule<Variant> {
  public let reason: String
  public let rejects: (Variant) -> Bool

  public init(_ reason: String, rejects: @escaping (Variant) -> Bool) {
    self.reason = reason
    self.rejects = rejects
  }
}

public struct VariantSpace<Variant: Hashable> {
  public struct Rejection: Identifiable {
    public let reason: String
    public let count: Int
    public var id: String { reason }
  }

  public let legal: [Variant]
  public let rejections: [Rejection]
  /// Candidates examined: the size of the cross product, or the number of draws.
  public let total: Int
  public let seed: UInt64

  /// Discrete levers. Pass the full cross product; the result is every legal variant, shuffled
  /// with `seed` so the order carries no ranking.
  public static func enumerate(
    _ candidates: [Variant],
    rules: [VariantRule<Variant>],
    seed: UInt64
  ) -> VariantSpace {
    var generator = SeededGenerator(seed: seed)
    var counts = [Int](repeating: 0, count: rules.count)
    var legal: [Variant] = []
    for candidate in candidates {
      if let index = rules.firstIndex(where: { $0.rejects(candidate) }) {
        counts[index] += 1
      } else {
        legal.append(candidate)
      }
    }
    legal.shuffle(using: &generator)
    return VariantSpace(legal: legal, rejections: rejections(rules, counts), total: candidates.count, seed: seed)
  }

  /// Continuous levers, or a cross product too large to show. Draws random candidates inside
  /// the lever ranges and keeps the first `count` distinct legal ones. `draw` must take every
  /// value from the generator it is given, or the sheet will not reproduce.
  public static func sample(
    count: Int,
    rules: [VariantRule<Variant>],
    seed: UInt64,
    maxDraws: Int = 10_000,
    draw: (inout SeededGenerator) -> Variant
  ) -> VariantSpace {
    var generator = SeededGenerator(seed: seed)
    var counts = [Int](repeating: 0, count: rules.count)
    var seen: Set<Variant> = []
    var legal: [Variant] = []
    var draws = 0
    while legal.count < count, draws < maxDraws {
      draws += 1
      let candidate = draw(&generator)
      if let index = rules.firstIndex(where: { $0.rejects(candidate) }) {
        counts[index] += 1
      } else if seen.insert(candidate).inserted {
        legal.append(candidate)
      }
    }
    return VariantSpace(legal: legal, rejections: rejections(rules, counts), total: draws, seed: seed)
  }

  private static func rejections(_ rules: [VariantRule<Variant>], _ counts: [Int]) -> [Rejection] {
    zip(rules, counts).map { Rejection(reason: $0.reason, count: $1) }
  }
}

/// Every legal variant in one grid, each drawn by the same view the prototype uses, scaled
/// down. `canvas` is the size the real layout is given (a device or window size in points).
public struct ContactSheet<Variant: Hashable, Frame: View>: View {
  private let space: VariantSpace<Variant>
  private let canvas: CGSize
  private let scale: CGFloat
  private let label: (Variant) -> String
  private let onPick: (Variant) -> Void
  private let frame: (Variant) -> Frame

  public init(
    _ space: VariantSpace<Variant>,
    canvas: CGSize,
    scale: CGFloat = 0.3,
    label: @escaping (Variant) -> String,
    onPick: @escaping (Variant) -> Void = { _ in },
    @ViewBuilder frame: @escaping (Variant) -> Frame
  ) {
    self.space = space
    self.canvas = canvas
    self.scale = scale
    self.label = label
    self.onPick = onPick
    self.frame = frame
  }

  private var thumbnail: CGSize {
    CGSize(width: canvas.width * scale, height: canvas.height * scale)
  }

  public var body: some View {
    ScrollView {
      VStack(alignment: .leading, spacing: 16) {
        header
        LazyVGrid(
          columns: [GridItem(.adaptive(minimum: thumbnail.width), spacing: 16, alignment: .top)],
          alignment: .leading,
          spacing: 24
        ) {
          ForEach(Array(space.legal.enumerated()), id: \.element) { index, variant in
            cell(number: index + 1, variant: variant)
          }
        }
      }
      .padding(16)
    }
  }

  private var header: some View {
    VStack(alignment: .leading, spacing: 4) {
      Text("\(space.legal.count) legal of \(space.total) examined. Seed \(space.seed). Order is shuffled, not ranked.")
        .font(.headline)
      ForEach(space.rejections) { rejection in
        Text("\(rejection.count) rejected: \(rejection.reason)")
          .font(.caption)
          .foregroundStyle(.secondary)
      }
    }
  }

  private func cell(number: Int, variant: Variant) -> some View {
    Button {
      onPick(variant)
    } label: {
      VStack(alignment: .leading, spacing: 8) {
        frame(variant)
          .frame(width: canvas.width, height: canvas.height)
          .scaleEffect(scale)
          .frame(width: thumbnail.width, height: thumbnail.height)
          .allowsHitTesting(false)
        Text("#\(number)  \(label(variant))")
          .font(.caption.monospaced())
          .foregroundStyle(.secondary)
          .frame(width: thumbnail.width, alignment: .leading)
      }
      .contentShape(.rect)
    }
    .buttonStyle(.plain)
  }
}
#endif

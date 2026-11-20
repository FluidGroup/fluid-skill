# Building in SwiftUI

Patterns and pitfalls for steps 6 and 7 on iOS, iPadOS and macOS. Check the project's
deployment target before using an API marked with a version below, and follow the project's own
coding guide and design system first; this file fills gaps. The code blocks here are
type-checked against the SDK by `tools/typecheck-snippets.py`; they were not run.

## Tokens first

Express the constraint sheet as Swift constants before writing views. Views use tokens and never
raw numbers.

```swift
import SwiftUI

enum Spacing {
  static let s1: CGFloat = 4
  static let s2: CGFloat = 8
  static let s3: CGFloat = 12
  static let s4: CGFloat = 16
  static let s6: CGFloat = 24
}

enum Corner {
  static let card: CGFloat = 24
  /// Concentric nesting on targets without `ConcentricRectangle`.
  static func inner(_ outer: CGFloat, inset: CGFloat) -> CGFloat { max(0, outer - inset) }
}

enum Motion {
  static let sheetSpring = Spring(duration: 0.45, bounce: 0.15)
  static let sheet = Animation.spring(sheetSpring)
  static let snap = Animation.snappy(duration: 0.3)
  static let stagger = 0.04
  static let dismissThreshold: CGFloat = 0.5
}

extension Font {
  static let rowTitle = Font.body.weight(.semibold)
  static let rowDetail = Font.footnote
}
```

- **Type and Dynamic Type.** Build the roles on text styles (`.title2`, `.body`, `.footnote`).
  Scale a brand face with `Font.custom(_:size:relativeTo:)` and any size that should grow with
  text with `@ScaledMetric`. "Three styles per screen" means three roles; they all scale.
- **Colour.** Hierarchical styles (`.primary`, `.secondary`, `.tertiary`), background styles
  (`.background`, `.background.secondary`, `.fill.tertiary`) and `.tint`. Custom colours come
  from the asset catalogue. No `Color(red:green:blue:)` in a view.
- **Margins and safe areas.** Let `List`, `Form` and `NavigationStack` supply their own insets.
  In a custom scroll view use `.contentMargins` (iOS 17) or `.scenePadding()`, and put
  backgrounds behind the safe area with `.ignoresSafeArea()` on the background only.
- **Concentric corners.** On OS 26 and later, declare the container's shape once and let nested
  shapes follow it. Earlier, compute `outer − inset` from the tokens. Always the continuous
  style.

```swift
struct RecordingCard: View {
  @ScaledMetric(relativeTo: .body) private var artwork: CGFloat = 56

  var body: some View {
    if #available(iOS 26, macOS 26, *) {
      card.containerShape(.rect(cornerRadius: Corner.card, style: .continuous))
    } else {
      card
    }
  }

  private var card: some View {
    HStack(spacing: Spacing.s3) {
      Image(systemName: "waveform")
        .frame(width: artwork, height: artwork)
        .background(.fill.tertiary, in: artworkShape)
      VStack(alignment: .leading, spacing: Spacing.s1) {
        Text("Morning notes").font(.rowTitle)
        Text("Today, 12 min").font(.rowDetail).foregroundStyle(.secondary)
      }
    }
    .padding(Spacing.s3)
    .frame(maxWidth: .infinity, alignment: .leading)
    .background(.background.secondary, in: .rect(cornerRadius: Corner.card, style: .continuous))
  }

  private var artworkShape: AnyShape {
    if #available(iOS 26, macOS 26, *) {
      AnyShape(ConcentricRectangle())
    } else {
      AnyShape(.rect(cornerRadius: Corner.inner(Corner.card, inset: Spacing.s3), style: .continuous))
    }
  }
}
```

Gate the container API as well as `ConcentricRectangle`; do not infer availability from the
installed SDK. For app-owned nested surfaces, derive the fallback from the actual outer shape
and inset, including borders. Restacking or resizing must preserve the relationship. System
controls and presentations retain their own geometry. Inspect the rendered corners as well as
the source values.

## Standard components first

`List`, `Form`, `NavigationStack`, `NavigationSplitView`, `TabView`, `.sheet`, `.toolbar`,
`.swipeActions`, `.searchable`, `ContentUnavailableView` and the system controls carry the
behaviour listed in `platform.md`. Start from them. Replacing `List` with `ScrollView` +
`LazyVStack` to get a custom row animation gives up swipe actions, edit mode, selection and
keyboard navigation; do it only when the user will feel the gain, and state what was lost.

- Style system controls with their own styles (`.buttonStyle(.borderedProminent)`,
  `.controlSize`, `.listStyle`, `.listRowBackground`) before writing a custom one.
- One prominent button per screen. On OS 26 and later that is `.buttonStyle(.glassProminent)`
  for a floating control; group floating glass controls in one `GlassEffectContainer`, and do
  not put glass on content.
- Empty, loading and error states: `ContentUnavailableView` (iOS 17), `ProgressView`,
  `.redacted(reason: .placeholder)`.
- On iPad, use `NavigationSplitView`, or a `TabView` with `.tabViewStyle(.sidebarAdaptable)`
  (iOS 18), so regular width gets a sidebar.

## Whole targets, pointer and keyboard

A row or card that opens something is a `Button` or `NavigationLink` wrapping the whole view,
never `.onTapGesture`: a button brings press feedback, the accessibility trait, keyboard and
pointer support. Controls are at least 44 by 44 points; enlarge small glyphs with a frame plus
`contentShape`, not by scaling the glyph.

```swift
struct RecordingRow: View {
  @Environment(\.dynamicTypeSize) private var typeSize
  let open: () -> Void

  var body: some View {
    Button(action: open) {
      // Side by side until the accessibility sizes, then stacked.
      let layout = typeSize.isAccessibilitySize
        ? AnyLayout(VStackLayout(alignment: .leading, spacing: Spacing.s1))
        : AnyLayout(HStackLayout(spacing: Spacing.s3))
      layout {
        Text("Morning notes").font(.rowTitle)
        Spacer(minLength: 0)
        Text("12:04").font(.rowDetail.monospacedDigit()).foregroundStyle(.secondary)
      }
      .frame(minHeight: 44)
      .contentShape(.rect)
    }
    .buttonStyle(.plain)
    .hoverEffect(.highlight)
  }
}

struct CloseButton: View {
  let close: () -> Void

  var body: some View {
    Button("Close", systemImage: "xmark", action: close)
      .labelStyle(.iconOnly)
      .frame(minWidth: 44, minHeight: 44)
      .contentShape(.rect)
      .keyboardShortcut(.cancelAction)
  }
}
```

On the Mac, also add the action as a menu command (see `appkit.md`, which covers SwiftUI Mac
apps too).

## Interruptibility

SwiftUI springs are interruptible by default: changing state inside `withAnimation` while a
previous animation runs retargets from the current value and keeps velocity. Design with that,
and avoid the things that defeat it:

- Use springs (`.spring(duration:bounce:)`, `.snappy`, `.smooth`, `.bouncy`, a named `Spring`)
  for state changes. `.easeInOut` and `.linear` restart from zero velocity when interrupted,
  which shows as a hitch.
- Do not gate input on completion. No `allowsHitTesting(false)` or `disabled(true)` "until the
  animation ends", and no logic that waits in a completion handler before the next tap is
  accepted.
- Drive gesture transitions from the gesture's **current value**, not from a boolean that flips
  at the end.
- Prefer animating layout-independent properties (`offset`, `scaleEffect`, `opacity`) for the
  signature, and let state changes carry everything else.

### Drag that hands off velocity

```swift
struct DismissibleCard: View {
  @State private var offset: CGFloat = 0          // settled position
  @GestureState private var drag: CGFloat = 0     // live translation; resets on end or cancel
  let travel: CGFloat                             // distance from open to dismissed

  var body: some View {
    RecordingCard()
      .offset(y: offset + drag)                   // follows the finger exactly: no animation here
      .gesture(
        DragGesture()
          .updating($drag) { value, state, _ in state = value.translation.height }
          .onEnded { value in
            let released = offset + value.translation.height
            let projected = offset + value.predictedEndTranslation.height   // position plus momentum
            let target: CGFloat = projected > travel * Motion.dismissThreshold ? travel : 0
            let distance = target - released
            let relativeVelocity = distance == 0 ? 0 : value.velocity.height / distance
            offset = released                     // keep the released position, then animate from it
            withAnimation(.interpolatingSpring(Motion.sheetSpring, initialVelocity: relativeVelocity)) {
              offset = target
            }
          }
      )
  }
}
```

Points that matter:

- The live translation is applied without animation, so the view stays under the finger.
- The settled offset is updated to the release position before animating, so there is no jump
  when `@GestureState` resets.
- The decision uses `predictedEndTranslation`, so a quick flick dismisses from anywhere.
  `value.velocity` is available from iOS 17.
- `@GestureState` also resets on cancellation, which covers the system taking the gesture.
- This release sketch alone does not implement a mid-settle re-grab: `offset` holds the target,
  not the presented position. For a custom gesture, use the presentation-tracking recipe in
  `ios-coding-aesthetics` when available, or the project's existing interaction primitive.
  Verify re-grab and cancellation in a running host before claiming interruptibility.
- Give the same change a non-gesture route (a button, an accessibility action).

### System transitions

```swift
@available(iOS 18, *)
struct RecordingsGrid: View {
  @Namespace private var zoom
  @State private var selection: Recording?

  var body: some View {
    ScrollView(.horizontal) {
      LazyHStack(spacing: Spacing.s3) {
        ForEach(0..<8, id: \.self) { id in
          Button { selection = Recording(id: id) } label: {
            RecordingCard().frame(width: 280)
          }
          .buttonStyle(.plain)
          .matchedTransitionSource(id: id, in: zoom)             // iOS 18
        }
      }
      .scrollTargetLayout()
    }
    .scrollTargetBehavior(.viewAligned)                           // iOS 17: native snap and momentum
    .contentMargins(.horizontal, Spacing.s4, for: .scrollContent)
    .scrollIndicators(.hidden)
    .sheet(item: $selection) { recording in
      Text("Recording \(recording.id)")
        .presentationDetents([.medium, .large])
        .navigationTransition(.zoom(sourceID: recording.id, in: zoom))   // iOS 18
    }
  }
}

struct Recording: Identifiable, Hashable { let id: Int }
```

- Prefer system presentations: `.sheet` with `presentationDetents`, `.navigationDestination`,
  `.popover`, `.inspector`. They are interruptible and accessible at no cost.
- For "the card grows into the detail", use the zoom navigation transition. Apply the
  transition source to the view whose shape should zoom, after its background and clip shape.
- For siblings inside a detail, use a paging container (`TabView` with the page style, or a
  horizontal `ScrollView` with `.scrollTargetBehavior(.paging)`).
- For a carousel, use `.scrollTargetLayout()` with `.viewAligned`. A hand-rolled `DragGesture`
  carousel loses momentum, rubber banding, trackpad and keyboard support, and conflicts with
  vertical scrolling.
- Scroll-linked effects read position (`scrollTransition`, `visualEffect`,
  `onScrollGeometryChange`); they never write it.
- A custom drag inside a scroll view competes with the scroll gesture. Restrict it to the other
  axis, give it a minimum distance, or attach it to a dedicated handle.

## Haptics, signature, Reduce Motion

```swift
struct LandingStack: View {
  @Environment(\.accessibilityReduceMotion) private var reduceMotion
  @State private var landed = false

  var body: some View {
    VStack(spacing: Spacing.s2) {
      ForEach(0..<4, id: \.self) { index in
        RecordingCard()
          .offset(y: landed ? 0 : Spacing.s6)
          .opacity(landed ? 1 : 0)
          .animation(
            reduceMotion ? .smooth(duration: 0.2) : Motion.sheet.delay(Double(index) * Motion.stagger),
            value: landed
          )
      }
    }
    .sensoryFeedback(.impact(weight: .light), trigger: landed)    // iOS 17: one state boundary
    .onAppear { landed = true }
  }
}
```

- Fire haptics at state boundaries only, tied to the state that changes.
- Use `PhaseAnimator` or `KeyframeAnimator` (iOS 17) for a short choreographed moment.
  Everything outside the signature uses the plain named springs.
- Read `accessibilityReduceMotion` wherever a spring overshoots or a view travels far.

## Dials in a debug build

```swift
#if DEBUG
@Observable final class Dials {
  static let shared = Dials()
  var sheetDuration = 0.45
  var sheetBounce = 0.15
  var dismissThreshold = 0.5
  var showGuides = false
  var showHitAreas = false
  var showState = false

  var summary: String {
    "spring.sheet: duration \(sheetDuration), bounce \(sheetBounce); dismiss.threshold: \(dismissThreshold)"
  }
}

struct DialsPanel: View {
  @Bindable var dials = Dials.shared

  var body: some View {
    Form {
      Section("spring.sheet") {
        LabeledContent("Duration \(dials.sheetDuration, format: .number.precision(.fractionLength(2)))") {
          Slider(value: $dials.sheetDuration, in: 0.15...1.0, step: 0.05)
        }
        LabeledContent("Bounce \(dials.sheetBounce, format: .number.precision(.fractionLength(2)))") {
          Slider(value: $dials.sheetBounce, in: 0...0.5, step: 0.05)
        }
      }
      Section("Structure") {
        Toggle("Layout guides", isOn: $dials.showGuides)
        Toggle("Hit areas", isOn: $dials.showHitAreas)
        Toggle("State readout", isOn: $dials.showState)
      }
      Text(dials.summary).font(.footnote.monospaced()).textSelection(.enabled)
    }
  }
}
#endif

enum Tuned {
  /// The one place a dial may override a token. Release builds read the constant.
  static var sheet: Animation {
    #if DEBUG
    .spring(duration: Dials.shared.sheetDuration, bounce: Dials.shared.sheetBounce)
    #else
    Motion.sheet
    #endif
  }
}
```

- Keep the dials type and the panel in their own file, entirely inside `#if DEBUG`. Models and
  business logic never read a dial; only the token accessors do.
- Present the panel from a debug-only entry point that is not part of the screen's own UI, in a
  sheet with a medium detent so the screen stays visible. Do not persist overrides that silently
  change what other previews and builds show.
- Structure toggles: draw the layout margins in an `.overlay`, outline hit areas with a debug
  modifier that strokes the content shape, and show a small text overlay with the interaction's
  state, progress and velocity.
- **Slow motion** for the four interruption tests: Simulator → Debug → Slow Animations.
- When values settle, copy them, write them into the constants and the constraint sheet, and
  remove nothing else.

## Variations

Generate the legal set from a variant value type and show it with `ContactSheet` from
`assets/swift/DesignPlayground.swift` (see `variations.md`): a debug-only screen for picking on
a device, or one `#Preview` for a screenshot.

## Checks before the gate

- Build it, or type-check the file against the SDK for the deployment target.
- Preview or run at the default and the largest accessibility text size, in light and dark, at
  the smallest and largest supported width.
- Run the four interruption tests with slow animations on, on a device if possible.
- VoiceOver reaches the primary action; custom gestures have an accessible alternative.
- Run `scripts/check_swift_ui.py` on the files you wrote.
- State in the report which of these were done and which were not.

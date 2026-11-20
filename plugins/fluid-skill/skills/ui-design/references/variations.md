# Variations: structured randomization and the contact sheet

Marvin Schwaibold's portfolio dates *Structural Dynamics in randomized Design* to 2019.
Its Component Randomizer lets content reorder when specified conditions hold. The prototype
shows maximum rows and columns and separate switches for body text and images. The designer
can choose both the grid and which elements participate. [Project and prototype](https://2022.marvinschwaibold.com/projects/structure-in-randomized-design/) · [Dated project index](https://2022.marvinschwaibold.com/)

In his 2026 demo Schwaibold describes revisiting a thesis he wrote in 2019. A column grid,
padding, safe space and an underlying pixel grid bound that demo's 180+ layouts. He scans
them to decide what to develop. Asked where to read the thesis, he said he was rewriting
it for republication. The guidance here draws on the public project and demo. Seeded replay,
point-based layout and the SwiftUI example are adaptations for this skill.
[Demo](https://x.com/MSchwaibold/status/2104640742861779151) · [Author's reply about the manuscript](https://x.com/MSchwaibold/status/2104677901887213839)

Use this step when the layout is the open question: an exploration, or a deliverable where the
user asked to see options. Skip it for a fix, when the project or the platform already dictates
the layout (a settings form, a standard list), and when the user asked for a finished screen:
there, choose the standard layout and deliver it.

**Keep the machinery out of the product.** The variant type, the rules and the contact sheet
live in a playground target, a preview, or a file wrapped in `#if DEBUG`. Once a variant is
picked, the product code contains that one layout, written plainly, with no variant parameter
and no branching left behind.

## Composition, not cosmetic permutations

State a composition hypothesis for each family: what becomes primary, how related actions are
grouped, and what moves into the background. Colour-only or radius-only changes do not count as
different design directions. Keep the fixture, operations and initial state equal.

Corresponding app-owned nested rounded surfaces must stay concentric at every sampled inset and
size: `innerRadius = max(0, outerRadius - inset)`. Derive radii rather than sampling them
independently. System-owned controls keep their platform geometry. Reject broken relationships
as illegal layouts; token names alone do not prove that rendered corners align.

Keep labels outside each variant's surface. Do not add an unrelated rounded comparison wrapper
that masks the silhouette, clips shadows or creates conflicting nested corners.

## Procedure

1. **Fix the comparison.** Use one content fixture, set of actions, viewport, text size and
   appearance. Draw the usable rectangle after the system bars and safe-area insets. Mark any
   additional protected space, including room to read a caption or reach a persistent control.
2. **Define the grid.** Within that rectangle choose the padding, number of columns and gutter
   from the constraint sheet. For usable width `W` after padding, `n` columns and gutter `g`,
   each column is `(W - (n - 1) * g) / n` wide. The same tracks position the actual views.
   Let text determine row height. Record how the grid changes at narrow widths and large type.
3. **Choose which blocks participate.** Only participating groups get placement choices.
   For a pass about artwork, pin the title to its current columns and row. For a pass about
   reading order, let both blocks move. Give movable groups allowed starts, spans and
   relationships. An artwork block can lead the title, follow it, or share its row. Keep
   navigation and system controls in the platform's own layout. Freeze styling for this pass
   so the silhouette and reading order account for the differences.
4. **Generate and filter.** Enumerate a small discrete space. For a large or continuous space
   use the kit's seeded sampler, draw only from declared ranges, and snap to the allowed steps.
   Reject out-of-bounds spans, forbidden overlaps, insufficient readable width and intrusions
   into protected space. Use the resolved placement as the variant identity so equivalent
   draws appear once. Track candidates examined and first-failing rules.
5. **Compare.** Show all retained candidates on one contact sheet with the seed and an ID or
   placement label. Use the same fixture and canvas throughout. Report the number sampled when
   sampling. If few layouts survive, show them and explain the limiting rule. Add a lever only
   when it opens a meaningful composition.
6. **Let the human steer.** Leave the sheet unranked. Record the selected placement and why,
   or translate feedback into a revised rule and rerun with the same fixture and seed. For
   example, “keep the title with the artwork” can constrain them to adjacent columns in one
   row. A new seed explores other draws under the same rules.

## Worked example

A scene preview has artwork, a title with a short description, and a persistent start button.
The example canvas is 384 pt wide inside the system safe area. With 16 pt padding on both sides
and three 16 pt gutters, each of four columns is 76 pt wide. Two columns give either block
168 pt, the minimum chosen for this fixture. The button occupies its own row outside the
scrollable content. It never participates in placement.

Use zero-based, upper-exclusive column ranges. For example, artwork in `0..<2` and text in
`2..<4` can share a row. Artwork in `0..<3` and text in `2..<4` would collide in column 2,
so that pair is legal only on separate rows. The six possible spans per block and three row
arrangements give 108 candidates. Of those, 74 survive. This is small enough to enumerate.

The example uses `VariantSpace` and `ContactSheet` from
[`DesignPlayground.swift`](../assets/swift/DesignPlayground.swift) in a debug target.
For larger spaces, pass the same rules to `VariantSpace.sample(count:rules:seed:draw:)` and use
the supplied generator for every draw. Record the seed, rules, fixture and canvas with the pick.

```swift
#if DEBUG
import SwiftUI

struct ScenePlacement: Hashable {
  enum Rows: CaseIterable { case artFirst, titleFirst, shared }
  let art: Range<Int>
  let title: Range<Int>
  let rows: Rows

  static let columnCount = 4
  static let gutter: CGFloat = 16
  static let padding: CGFloat = 16

  static let space: VariantSpace<Self> = {
    var spans: [Range<Int>] = []
    for start in 0..<(columnCount - 1) {
      for end in (start + 2)...columnCount {
        spans.append(start..<end)
      }
    }
    var candidates: [Self] = []
    for art in spans {
      for title in spans {
        for rows in Rows.allCases {
          candidates.append(Self(art: art, title: title, rows: rows))
        }
      }
    }
    return VariantSpace.enumerate(candidates, rules: [
      VariantRule("Artwork and text overlap in a shared row") {
        $0.rows == .shared && $0.art.overlaps($0.title)
      }
    ], seed: 2104)
  }()
}

struct ScenePreview: View {
  let placement: ScenePlacement
  @Environment(\.dynamicTypeSize) private var typeSize

  var body: some View {
    VStack(spacing: ScenePlacement.gutter) {
      GeometryReader { geometry in
        let gutter = ScenePlacement.gutter
        let count = CGFloat(ScenePlacement.columnCount)
        let track = (geometry.size.width - (count - 1) * gutter) / count
        ScrollView {
          if typeSize.isAccessibilitySize || 2 * track + gutter < 168 {
            VStack(alignment: .leading, spacing: gutter) {
              title
              artwork
            }
          } else {
            let artBlock = place(artwork, in: placement.art, track: track)
            let titleBlock = place(title, in: placement.title, track: track)
            switch placement.rows {
            case .artFirst:
              VStack(alignment: .leading, spacing: gutter) {
                artBlock
                titleBlock
              }
            case .titleFirst:
              VStack(alignment: .leading, spacing: gutter) {
                titleBlock
                artBlock
              }
            case .shared:
              ZStack(alignment: .topLeading) {
                artBlock
                titleBlock
              }
            }
          }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
      }
      Button("Start scene") { /* prototype action */ }
        .buttonStyle(.borderedProminent)
    }
    .padding(ScenePlacement.padding)
  }

  private func place(_ block: some View, in span: Range<Int>, track: CGFloat) -> some View {
    let stride = track + ScenePlacement.gutter
    return block
      .frame(width: CGFloat(span.count) * stride - ScenePlacement.gutter, alignment: .leading)
      .padding(.leading, CGFloat(span.lowerBound) * stride)
      .frame(maxWidth: .infinity, alignment: .leading)
  }

  private var title: some View {
    VStack(alignment: .leading) {
      Text("Dusk").font(.title)
      Text("An indigo sky warms at the horizon and fades slowly through the last light of the day.")
        .font(.body)
    }
  }

  private var artwork: some View {
    LinearGradient(colors: [.indigo, .orange], startPoint: .top, endPoint: .bottom)
      .aspectRatio(1.5, contentMode: .fit)
  }
}

#Preview("Scene placements") {
  ContactSheet(
    ScenePlacement.space, canvas: CGSize(width: 384, height: 640),
    label: { "\($0.rows) · art \($0.art) · text \($0.title)" }
  ) { ScenePreview(placement: $0) }
}
#endif
```

Inspect the real content at full size. Range checks prove track placement at the stated width.
Long translations, accessibility text and a different canvas can trigger the full-width stacked
layout. Check those conditions separately before adopting a placement.

## How to render the contact sheet

Thumbnails must be cheap enough to show dozens at once and true enough to compare.

- **Live frames** (default): `ContactSheet` draws the real layout view at the size of a real
  screen or window and scales it down, with real content. A frame cannot promise a layout the
  screen will not produce, because it is the same view.
- **Schematic frames:** when the real view is heavy (video, maps), give the layout view a
  placeholder mode that draws blocks for media and keeps real text metrics.
- **UIKit and AppKit layouts:** wrap the view or view controller in a representable and pass it
  to `ContactSheet`, or build the grid with a collection view. One implementation drives both
  the thumbnail and the prototype.
- **State the canvas.** Name the device or window size the frames show. If the screen also runs
  in regular width or in a resizable window, render a second sheet for that size; a variant that
  wins on a phone can fail on an iPad.
- **Check both appearances** and one large text size on the shortlist, not on all frames.
- **Look at it where it will be used.** Open the contact sheet as a debug-only screen on a
  device or in the simulator for the pick; a preview is enough for a screenshot in the report.
  Tapping a frame applies that variant to the prototype (`onPick`).

The header of the sheet states the numbers: how many candidates were examined, how many are
legal, how many each rule rejected, and the seed. This is evidence that the space was covered.

## After the pick

For shareable SwiftUI exports, follow [rendering.md](rendering.md): use the same comparison
View, fixed conditions and a repeatable command. `ImageRenderer` cannot capture every native
view, including some representable content. For UIKit/AppKit views it cannot render faithfully,
capture the real host instead; do not silently substitute a parallel image-only implementation.

1. Write the pick, its lever values, the reason and the seed in the design sheet.
2. Rewrite the product view as that one layout, with no variant parameter.
3. Leave the variant type and the contact sheet in the debug-only file, or delete them. They
   are not referenced from product code.

## Gate for this step

- Levers, fixed items, rules and the seed are written in the design sheet.
- The contact sheet shows every retained layout with counts and reproducible placement labels.
- No lever varies something the platform decides.
- No variant is marked as preferred by you. The pick, when made, has a recorded reason.

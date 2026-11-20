# The constraint sheet

Step 3 of the loop. The sheet defines the legal space. Variations explore inside it, the build
uses only its values, and feedback edits it. Write it before generating or implementing
anything, and keep it to one page: if it sprawls, it has not been decided yet.

**Existing systems win.** If the project has tokens, a theme, or a design system (a spacing or
typography file, colour assets, a component library), that is the sheet. Record what exists,
fill only the gaps, and flag conflicts to the human; do not introduce a parallel scale.

**The system is the default.** Where the project is silent, the value comes from the platform:
system margins, text styles, semantic colours, system control sizes. A custom value needs a
reason; a system value does not.

## Template

Copy this into the design sheet and replace the defaults deliberately. Mark where each value
came from: *project* (already in the codebase), *system* (the platform's own), *chosen* (decided
for this work, with a reason), or *default* (taken from this template unchanged).

```markdown
## Constraint sheet

### Platform
| Item | Value |
| --- | --- |
| Targets | iOS 17+, iPhone and iPad; or macOS 14+ |
| Framework | SwiftUI / UIKit / AppKit, as the project uses |
| Idiom | Tab bar + navigation stack / split view with sidebar / single window |
| Input | Touch; pointer and keyboard on iPad and Mac |
| Size range | Smallest and largest width the screen must hold (size classes, minimum window size) |

### Layout
| Item | Rule |
| --- | --- |
| Margins | System layout margins. Text columns stop at the readable width |
| Safe areas | Controls and text inside; backgrounds extend under bars and to the edges |
| Exploration grid (when comparing layouts) | Usable width, columns, gutter, padding owner and reserved regions for this canvas |
| Point grid | Every custom size is a multiple of 4. An odd value (13) is a bug |
| Spacing scale | 4 / 8 / 12 / 16 / 20 / 24 / 32 / 48 / 64, nothing else |
| Section spacing | One step clearly larger than in-section spacing |
| Corners | Continuous curve. Steps 8 / 12 / 16 / 24 / capsule, nothing else |
| Nested corners | Required for corresponding app-owned surfaces: innerRadius = max(0, outerRadius - inset); derive, never tune independently |
| Hit target | 44 by 44 points for touch. On the Mac, system control sizes |

### Type
| Role | Text style | Weight |
| --- | --- | --- |
| Title | title2 | semibold |
| Body | body | regular |
| Secondary | footnote | regular |
Limits: at most 3 text styles in the content of one screen (system bars not counted), 3 weights,
the system font unless the project has a brand face. Every style follows Dynamic Type.
At accessibility sizes: (which side-by-side layouts restack).

### Colour
| Token | Source | Use |
| --- | --- | --- |
| Text primary / secondary / tertiary | system label colours | … |
| Background / grouped background / fill | system background and fill colours | … |
| Separator | system separator | … |
| Accent | the app tint (AccentColor asset) | The one most important thing on a screen |
| (custom) | asset with light, dark and high-contrast values | … |
Destructive red and status colours are separate and do not count as the accent.

### Surfaces and symbols
| Item | Rule |
| --- | --- |
| Materials | Which floating surfaces use a material or glass. Content is opaque |
| Symbols | SF Symbols, one rendering mode, sized by the adjacent text style |

### Motion and haptics (named, all exposed on the dials panel)
| Name | Value | Used for |
| --- | --- | --- |
| spring.sheet | duration 0.45, bounce 0.15 | large transitions |
| spring.snap | duration 0.30, bounce 0 | selection, snapping, small state changes |
| spring.signature | … | the signature interaction only |
| drag.resistance | 0.35 | rubber band beyond an edge |
| dismiss.threshold | 0.5 | projected progress past which a release dismisses |
| haptic.(name) | impact light / selection / success | the state boundary that fires it |
Reduce Motion: (what each spring becomes).
```

## Why each limit exists

**4pt grid, closed spacing scale.** When every gap is drawn from nine values, siblings align by
construction and "a bit more space" has exactly one meaning: the next step up. Inventing 18 or
28 for one spot is how a layout drifts. System margins and system component metrics are not
overridden to fit the scale; the scale governs the space you add.

**Concentric corners are required.** When corresponding app-owned rounded surfaces nest with a
uniform inset, use `innerRadius = max(0, outerRadius - inset)`. With 24 outside and
an 8 inset, the inner radius is 16. With a 12 inset it is 12. If the result goes to 0 or below,
the inner element is square. On OS 26 and later the system computes this for you
(`ConcentricRectangle` and container shapes in SwiftUI, corner configurations in UIKit); on
earlier targets compute it from the tokens. Always use the continuous corner curve, which is
what the system's own shapes use. This one rule removes most "the corners look wrong" feedback.

Keep the relationship when spacing, size or accessibility layout changes. Measure the actual
gap, including borders, and inspect the rendered corresponding corners, not just the token
names. Derived radii need not be independent steps from the corner scale. For nonuniform insets
or different corner families, resolve the per-corner geometry or change the grouping; a single
subtraction is not proof. Leave system-owned controls and presentations under platform control.
Do not raise the deployment floor just because a newer SDK is installed; gate both the native
shape and its container API, or use the derived fallback.

**No double padding.** A padded container holding padded children pushes content off the edge
its siblings share. Decide which level owns the padding. In a system list or form, the system
owns the row insets.

**Three text styles per screen.** Title, body, secondary. A fourth is usually a symptom of
unresolved structure (go back to step 2), not a typographic need. Create emphasis with weight,
colour and space before size. Use text styles, never fixed point sizes: a fixed size ignores the
user's text size setting. Use a monospaced or monospaced-digit variant only for text read by
position: timecodes, numeric columns, counters that change in place.

**Semantic colours, one accent.** System colours adapt to light, dark, contrast settings and
the material behind them; a hard-coded RGB value does none of that. The accent marks the single
most important thing on a screen and is the app's tint, so system controls pick it up without
extra work. If the app has imagery or data, colour may follow the content (artwork behind a
player), as a background treatment, not as a second accent.

**Materials for floating layers only.** Bars, sheets and floating controls sit on a material or
glass so content shows through. Content itself is opaque. See `platform.md` for Liquid Glass.

**One motif, used once or twice.** A gradient animation that appears on three screens stops
being special at its second use. Treat a decorative motif as a signature.

**Named motion values.** Two or three springs for the whole app, each with a name, expressed as
duration and bounce so they read the same in SwiftUI, UIKit and Core Animation. A named spring
can be put on a dial and discussed; `0.3` and `.easeInOut` scattered through the code cannot.
Haptics are named the same way, each tied to one state boundary.

**Platform conditions belong on the sheet.** Deployment target, idiom, size range, Dynamic
Type behaviour, both appearances and Reduce Motion are constraints from the start, not later
fixes.

## Using the sheet

For layout exploration, add a row for each comparison canvas. Record its available content
bounds, column count, gutter, padding owner and reserved regions (for example, a playback bar
including its hit area). Give each movable block its allowed column spans and minimum readable
width. Derive track widths after subtracting padding and gutters. The point grid governs custom
spacing; fluid tracks can be fractional. Align hairlines to device pixels using the display
scale. System insets, text metrics and control sizes keep their native values.
See [the worked grid example](variations.md#worked-example).

- Implement the sheet as Swift constants first (a spacing namespace, corner steps, text style
  roles, colour assets, named springs), then write views only in terms of them. See the
  framework file for the form.
- Before using a value that is not on the sheet, add it with a reason. If you catch yourself
  typing a raw number in a view, stop and check the sheet.
- After tuning with dials, write the final values back here. The sheet is the record.

## Failure modes to check

- A custom size that is not a multiple of 4, or a gap not on the scale.
- An inner radius equal to the outer radius (should be smaller by the inset), or a circular
  corner curve beside the system's continuous ones.
- Padding applied at two nesting levels, or stacked on a list row's own insets.
- A fixed font size; more than three text styles in the content of one screen.
- A hard-coded colour; a custom colour with no dark value; state shown by colour alone.
- Accent used for several unrelated things on one screen.
- Touch targets under 44 by 44 points.
- A fixed-duration easing curve where a named spring belongs.

`scripts/check_swift_ui.py` finds several of these in source. Treat its output as leads.

## Gate for this step

- The sheet fits on one page.
- Every row is marked project, system, chosen or default.
- Every later value comes from the sheet, or the sheet was updated first.

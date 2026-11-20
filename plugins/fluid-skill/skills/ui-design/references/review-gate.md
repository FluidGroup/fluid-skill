# Review gate

Step 8 of the loop, and the whole job when asked to review existing UI. One critical failure
sends the work back. Praise is not a review: every item gets pass or fail with evidence.

## The gate

| # | Item | Passes when | Typical failure |
| --- | --- | --- | --- |
| 1 | One Thing | The subject and the primary action are clear within half a second | Several elements shout equally; the primary action is buried |
| 2 | Hierarchy | At most 3 text styles in the content of one screen; important information is in the content, not only in a header | Five sizes; key facts in a small header |
| 3 | Structure | The first screenful shows the content the screen is about; details are one push or sheet away; value comes before sign-in and permissions | Content hidden behind sheets or segments; a sign-in wall first |
| 4 | Interruptible | All four interruption tests pass | Input locked until an animation ends; rapid taps break state |
| 5 | Platform fit | Navigation, presentation and controls are the platform's own, or each deviation is justified; the back swipe, scrolling and sheet dismissal work; on the Mac every command is in the menu bar | A custom tab bar; a blocked back swipe; a Mac window with no menu commands |
| 6 | Targets and input | Whole rows and cards respond; touch targets are at least 44 by 44 points; pointer and keyboard work on iPad and Mac | Opens only from an icon; no hover or focus; mouse-only or touch-only |
| 7 | Adaptivity | Holds at the largest and smallest text size, in light and dark, with Reduce Motion, in every supported size class or window size; VoiceOver reaches and names the primary action | Truncated at large text; unreadable in dark; a gesture with no alternative |
| 8 | Colour and type | Semantic colours and text styles throughout; one accent; no decorative motif repeated; sheet limits hold | Hard-coded colours; fixed font sizes; the same animation reused everywhere |
| 9 | Signature | One signature interaction and one or two showstoppers are named and built | Uniformly "somewhat polished" with nothing memorable |
| 10 | Reduction | Every element can be justified in one sentence | Elements nobody can explain remain |

Also confirm the sheet-level checks from `constraint-sheet.md` (4pt grid, concentric corners, no
double padding) and the gate at the end of `platform.md`.
For corresponding app-owned nested rounded surfaces, verify the actual inset and derived radius
in the rendered result, including borders and adaptive layouts. Inspect concentric geometry, not
only names such as "inner" or "concentric" in source.

## How to check

Evidence has four levels. Name the level for every pass.

1. **Run on a device.** Required for a full pass of items 4 and 6 on anything touch-driven.
2. **Run in the simulator or as a Mac app.** Screenshots at the smallest and largest supported
   size, light and dark, default and largest accessibility text size. The four tests with slow
   animations.
3. **Built.** The code compiles for the deployment target. This proves availability, not design.
4. **Read only.** The source was inspected and nothing was built. Every item that needs a
   running app is "not verified".

- **Build it if a toolchain is there.** Use the project's scheme, or type-check a single file
  against the SDK. Say which. If there is no toolchain, say that the code was not compiled.
- **Measure, do not eyeball**, wherever a number exists. Run `scripts/check_swift_ui.py` on the
  files you wrote or reviewed (off-scale values, fixed font sizes, hard-coded colours,
  fixed-duration easing, input locks, tap gestures standing in for buttons). Its findings are
  leads to confirm in the code, not verdicts.
- A pass in your own table is a claim, not evidence. An item that was not measured is marked
  "not verified", never "pass".
- **Static exports are a separate evidence kind, not a runtime level.** Name the renderer,
  host, dimensions and environment; follow [rendering.md](rendering.md) for repeatable SwiftUI
  comparisons. A macOS `ImageRenderer` export is not an iOS Simulator screenshot or proof of
  iOS Dynamic Type, native-control behaviour, touch, VoiceOver, Reduce Motion or live playback.
- For new screens and explorations, name the composition decision that makes the visual
  hierarchy visible. A default control stack or colour-only variants are not a direction.
- For item 1, describe what you see first in the screenshot before reading the code. If your
  first description is not the One Thing, the item fails.
- For item 5, list every custom replacement of a system component with its gain and its losses.
  An empty list is the normal result.
- For item 7, use the environment overrides or preview variants; the Accessibility Inspector
  audits labels, contrast and target sizes.
- For item 10, list each element with its one-sentence reason. Anything without one is the
  fix list.

## Report format

```markdown
## Review gate

| # | Item | Result | Evidence |
| --- | --- | --- | --- |
| 1 | One Thing | pass | The list and the single prominent "Record" button are the only high-contrast elements (simulator screenshot, iPhone, light) |
| 2 | Hierarchy | fail | 4 text styles in the content: title2, headline, body, caption (row title uses headline) |
| 4 | Interruptible | not verified | Springs with velocity hand-off in source; not run |
| … | | | |

### Fixes
- Item 2: **correct**. Row title to body with semibold weight; remove the headline style.

### Deviations from system components
- None.

### Verified how
- Built: type-checked against the iOS SDK for the iOS 17 target.
- Simulator: screenshots at default and AX5 text size, light and dark.
- Source check: check_swift_ui.py, 0 findings.
- Not tested: a device, VoiceOver, iPad split view.
```

Each fix is one of three kinds: **remove** it, **correct** it (state the constraint and the
number, or the system component to restore), or **reorder** it.

## Presenting

When showing work on slides or a summary screen, keep each to seven lines of text. If it does
not fit, the structure is not finished.

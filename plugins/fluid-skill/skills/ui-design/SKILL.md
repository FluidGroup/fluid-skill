---
name: ui-design
description: >-
  Design, build, restyle, polish or review Apple-platform UI (iOS, iPadOS,
  macOS) in SwiftUI, UIKit or AppKit. Use for screens, view controllers,
  windows, components, sheets, lists, animation, gestures, transitions,
  layout explorations, or UI that feels generic, foreign or unpolished.
  Start from the HIG and the project's design system; decide the One Thing,
  navigation idiom, visual direction and constraints, sketch states, explore
  layouts by structured randomization on a fixed grid when options are requested, prototype
  interruptible interactions, expose tuning dials and review with evidence.
metadata:
  github-path: plugins/fluid-skill/skills/ui-design
  github-ref: refs/heads/main
  github-repo: https://github.com/FluidGroup/fluid-skill
---

# UI design for Apple platforms: constraints first, prototype first

A model asked to "make a nice screen" guesses. It guesses spacing, radius, type sizes, colour and
timing separately for every element, so the result looks plausible, generic and slightly foreign
to the platform, and each revision guesses again. This skill replaces guessing with a fixed order
of work:

1. decide what the screen is for,
2. take the platform's conventions as the starting rules, and write the rest down before drawing,
3. explore only inside those rules, in volume,
4. let the human choose,
5. build something that can be touched, and tune it by hand.

Two roles hold throughout. **You generate and implement. The human decides.** Output volume is
never the bottleneck; judgment is. So produce many options and lay them side by side, but do not
rank them, and do not present quantity as quality.

## Work with the coding skills

This skill owns composition, visual direction, navigation, interaction design, exploration and
design evidence. When available, apply `coding-aesthetics` and `ios-coding-aesthetics` alongside
it for API shape, ownership, state, concurrency, formatting and build conventions. Do not copy
those rules into a second design system. The examples here illustrate design mechanics; adapt
their code to the project's implementation conventions.

## The platform comes first

The Human Interface Guidelines and the system's own behaviour are the outermost constraint.
Everything in this skill happens inside them.

- **Order of authority:** the project's design system, then the platform's conventions, then
  this skill's defaults.
- **System components first.** Lists, navigation, sheets, toolbars, menus and controls carry
  behaviour that takes real work to rebuild. Replace one only for a reason the user will feel,
  say what was given up, and restore it.
- **Never break what the system gives the user:** the back swipe, scrolling, sheet dismissal,
  Dynamic Type, Dark Mode, keyboard shortcuts, the menu bar.
- **The signature lives in the content,** not in restyled system chrome.
- **Native behaviour is not default styling everywhere.** Give a new screen or exploration a
  concrete hierarchy and composition hypothesis, not an undifferentiated stack of controls.
  Do not manufacture identity with arbitrary cards, shadows or custom navigation.
- **Use the framework the project uses.** Do not add SwiftUI to a UIKit screen, or the reverse,
  as a side effect of a design task.

→ `references/platform.md`. Read it for any work larger than a fix.

## Size the work before starting

The process exists to make the result better, not bigger. First ask what is being asked for: **a
deliverable** (code that goes into the app) or **an exploration** (the design itself is the open
question). Then pick the smallest path that fits:

| Request | Path |
| --- | --- |
| A fix or tweak ("the gap is too big", "this animation feels slow") | Restate it as a constraint with a number, change the value, and say before → after and the rule in the reply. Use the project's tokens if it has them; do not introduce a token system, a design sheet file or new tooling for a two-value change. Verify only what you touched. |
| One component or one interaction | Steps 3 (only the values this component needs), 4, 6, and two or three dials from step 7. Check the gate items it touches. |
| A screen for the app ("build the settings screen", a code deliverable) | Steps 1 to 4, 6 and 8. **Decide the layout yourself** from the platform's standard patterns and deliver one finished screen. Run step 5 only if the user asks for options or says the layout is undecided. Add dials only if tuning is expected, in a separate debug-only file. |
| An exploration: a new screen concept, a prototype, "design this", "explore layouts" | All eight steps. |
| A review of existing UI | Step 8 only, then propose fixes as constraints. |

If the project already has tokens, a theme file or a design system, those are the constraint
sheet. Read them first and extend them; never run a second system beside them.

### Keep the deliverable the deliverable

- **Process artefacts stay out of the product.** Variation machinery, contact sheets, dials and
  overlays live in a playground target, a preview, or files wrapped in `#if DEBUG`. The shipped
  view takes no `variant` parameter, reads no value from a dial, and has no debug entry point in
  its own UI.
- **A code request gets one decided layout.** "The human decides" covers questions the human
  has opened, not a way to return unfinished work. If you were asked for a screen, choose, and
  note the choice as a one-line assumption.
- **The writing scales with the work.** A fix: two sentences in the reply. A component: a short
  section in the reply. A screen: a design sheet of about a page. An exploration: the full
  sheet.
- **Check the proportion before handing back.** If the supporting material is larger than the
  thing that was asked for, or the work took several times longer than building it directly
  would, cut the material.

## Working with the human

Three decisions belong to the human: the One Thing, which variation to build, and the final
"feel" values. Ask when asking is cheap and someone is there to answer. Offer a draft One Thing
sentence. For a layout pick, show the unranked sheet and ask which placement to develop.

When nobody can answer (a background run, or the user said to just build it), do not stall.

- **For a deliverable:** make the decision, and record it as a one-line **assumption** in the
  report.
- **For an exploration:** keep the choice open. Build on an unranked baseline, leave the contact
  sheet and the dials reachable, and say in the report which choices are still the human's.

## The loop

Each step produces something concrete. Keep the written parts in **one design sheet file** next
to the prototype (default `DESIGN_SHEET.md`; use the project's own spec location if it has one).

### 1. One Thing

Write one sentence: "The job this screen does is ___." Name the **single primary action**. Every
element must serve that sentence or become a candidate for removal. Two controls of equal visual
strength on one screen means the hierarchy has not been decided yet. The primary action must be
the action the sentence implies; if the sentence says "find a recording" and the loudest control
is "record", one of the two is wrong.
→ `references/structure.md`

### 2. Structure and navigation idiom

Inventory the content, weight it, and place it in the platform's own structure: which top-level
sections exist (tab bar on iPhone, sidebar on iPad and Mac), what is pushed, what is presented as
a sheet, and on the Mac which commands the menu bar holds. The first screenful shows the One
Thing; details are one push or one sheet away. Depth is for detail, not for hiding the content
the screen exists to show. Let people use the app before asking them to sign in.
Name what carries the visual character, what is deliberately quiet, and the composition decision
that makes the hierarchy visible. For a fix, preserve the established direction.
→ `references/structure.md`, `references/platform.md`

### 3. Constraint sheet

Before any layout, fix the legal space, starting from what the system provides: layout margins
and safe areas, a 4pt spacing scale, continuous corners with concentric nesting
(`innerRadius = max(0, outerRadius - inset)` for corresponding app-owned surfaces),
text styles (at most three in the content of one screen, all following Dynamic Type),
semantic colours with one accent (the app tint), materials, SF Symbols, the hit-target minimum,
and named springs. From here on, **a value that is not on the sheet does not get used.** If a new
value is needed, add it to the sheet with a reason first. This is what makes later feedback
cheap: a change is an edit to one number, not a new round of guessing.
→ `references/constraint-sheet.md` (template and defaults)

### 4. Sketch the states

Motion is specified by a state sketch, not by adjectives. For each main interaction draw plain
boxes and arrows: start state, end state, what the element does while a finger drags it, where
it lands on release, and **what happens when the user interrupts mid-animation**. If the
interruption arrows cannot be drawn, the interaction is not understood well enough to build.
→ `references/motion.md`

### 5. Explore layouts by structured randomization

When the layout is open, turn the constraint sheet into a grid for the app-owned content.
Fix the canvas, columns, gutters, padding and protected space around text, controls and
system chrome. Use points for layout and the display scale for pixel alignment where needed.
Keep the fixture, actions and typography constant for the comparison.

Choose which blocks can move for this comparison and pin the others in place.
Describe each candidate by where its content goes on that grid. Vary positions, spans and
relationships such as whether an image shares a row with its caption or leads a separate row.
Enumerate discrete placements or sample a large space with a recorded seed. Check the same
geometry the view uses and discard illegal placements before they reach the contact sheet.

Show the distinct surviving layouts together, unranked and labelled outside their surfaces.
The human can pick a layout or change a rule and regenerate the sheet. Record the choice and
reason. Until then, use an unranked baseline for the prototype. For shareable images, export
the same comparison View under fixed conditions. See `references/rendering.md`.
→ `references/variations.md`, `assets/swift/DesignPlayground.swift`

### 6. Build the prototype

Build in previews or a playground target, apart from production code, with real content. Build
**component by component**, starting with the one or two pieces that carry the screen (the
showstopper): they set the standard, and the rest becomes easy and quiet. Non-negotiable
behaviour:

- **Interruptible.** Every animation accepts input mid-flight and continues from the current
  position and velocity. No input is ever locked while something animates. A dragged element
  follows the finger exactly and hands its release velocity to the spring.
- **System scrolling and gestures.** Never reimplement inertia, intercept the scroll, or block
  the back swipe or the sheet's own dismissal.
- **Whole targets.** The entire row or card responds. On iPad and Mac the same action works by
  pointer and keyboard.
- **One signature.** Name one small interaction that gets disproportionate care (an organic,
  staggered, damped landing) and keep every other motion quiet around it.
- **Adaptive from the first build.** Dynamic Type, Dark Mode, size classes and window resizing
  are checked on the showstopper, not after the screen is finished.

→ `references/motion.md`, then `references/swiftui.md`, `references/uikit.md` or
`references/appkit.md`

### 7. Expose dials and structure

Do not tune by chat. Put every tunable value (springs, resistance, thresholds, blur, gaps) on a
debug panel, and add toggles that show the underlying structure (layout margins, hit areas, a
live state readout, slow motion). The human finds values by touch that they could not describe
in words, and hidden implementation mistakes become visible instead of being argued about. When
the values settle, **write them back to the constraint sheet**; the panel is a tool, not the
spec.
→ `references/dials.md`

### 8. Review gate

Check the result against the ten-item gate and report pass or fail per item with evidence (the
element, the measured number, the setting it was checked under). Run the bundled source check
where it applies. A failed item is fixed by removing, correcting or reordering, and "everything
is evenly somewhat polished" is itself a failure of item 9.
→ `references/review-gate.md`

## Feedback is a constraint, not a feeling

When the user (or you) says "cleaner", "it feels off" or "more native", find the number or the
convention behind it before changing anything: which spacing step, which radius, which text
style, which damping, which system component was replaced. "Inner radius should be 16 because
the outer is 24 with an 8 inset" can be applied once and stays applied. "Make it cleaner"
produces a different guess every time. If the result is still wrong after two attempts, stop
adjusting the wording of the request and follow the stuck protocol in `references/dials.md`.

## What to hand back

Scale this to the path chosen above.

- The thing that was asked for, with nothing in it that the user would have to delete before
  using it.
- For a screen or an exploration, the design sheet: One Thing and primary action, structure and
  navigation idiom, constraint sheet, state sketch, and the review-gate result. For an
  exploration it also holds the variation levers, rules and seed, the pick (or "open") with its
  reason, and the final dial values.
- A short report: what was built, the assumptions made, each deviation from a system component
  and what it cost, which gate items were verified and how (built, run in the simulator, run on
  a device, or read only), and what was not tested. For a fix, this is the whole written output.

## Reference files

Read only what the current step needs.

| File | Read when |
| --- | --- |
| `references/platform.md` | Any work larger than a fix: HIG conventions per platform, system-first rule, adaptivity, materials |
| `references/structure.md` | Steps 1 and 2: One Thing, navigation idiom, disclosure, anti-patterns |
| `references/constraint-sheet.md` | Step 3: the template, system defaults, concentric corners, colour and type limits |
| `references/variations.md` | Step 5: column placement, legality checks, seeded exploration and human selection |
| `references/rendering.md` | Shareable SwiftUI comparisons: repeatable exports from the real View, conditions and evidence limits |
| `references/motion.md` | Steps 4 and 6: interruptibility, springs, presentations, scroll, the four tests |
| `references/dials.md` | Step 7, and whenever you are stuck |
| `references/review-gate.md` | Step 8: the gate table and report format |
| `references/swiftui.md` | Building in SwiftUI |
| `references/uikit.md` | Building in UIKit |
| `references/appkit.md` | Building in AppKit, or any Mac window |

Bundled code: `assets/swift/DesignPlayground.swift` (seeded generator, variant enumeration and
sampling, contact sheet view; debug only) and `scripts/check_swift_ui.py` (source check for
off-scale values, fixed font sizes, hard-coded colours, fixed-duration easing and input locks).
Use them instead of rewriting them.

## Credit

The approach follows Marvin Schwaibold's public account of how he works: structured
randomization inside strict rules, layered disclosure, interruptible interaction, exposing
parameters instead of prompting, and designing key widgets first to set the standard. The
"state feedback as a constraint" and "component by component" framing and the concentric radius
rule are shared with Adam Perlis's `design-constraints` skill, which draws on the same account.
The platform conventions follow Apple's Human Interface Guidelines. The specific defaults, checks
and pitfalls here come from applying the process.

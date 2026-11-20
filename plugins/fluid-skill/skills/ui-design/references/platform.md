# Platform conventions: working inside the HIG

Read this for any work larger than a fix. The Human Interface Guidelines describe what people
already expect from an app on each device. A screen that ignores them costs the user effort
before they reach the content, however good it looks. This skill's own rules (One Thing, closed
scales, interruptibility) are applied inside these conventions, not instead of them.

## Order of authority

1. The project's design system and existing screens.
2. The platform's conventions: the HIG and the behaviour of the system components.
3. This skill's defaults.

When two levels disagree, the higher one wins, and the report says so in one line.

## Check the HIG, do not recite it

The HIG changes with every OS release. When a decision depends on it (which presentation to use,
where an action belongs, how a component behaves), read the current page for that component or
pattern under `https://developer.apple.com/design/human-interface-guidelines/` and cite the page
you read. If you cannot read it, say that the point comes from memory. Never state an exact
figure from the HIG that you did not just read.

Also read the project's deployment targets before proposing anything. A design that needs an API
from a newer OS than the target is not a design for this project.

## System components first

Start every screen from the system's parts. Each one carries behaviour the user relies on and
that a custom replacement silently drops.

| Component | What comes with it |
| --- | --- |
| List, table or collection list | Swipe actions, edit mode, selection, reordering, separators, keyboard navigation, Dynamic Type layout |
| Navigation stack and bars | Back swipe, back-button menu, large titles, scroll-edge appearance, state restoration |
| Sheets and popovers | Detents, interactive dismissal, adaptation between size classes, focus handling |
| Tab bar and sidebar | Adaptation between iPhone, iPad and Mac, customisation, badges |
| Toolbars and menus | Overflow, keyboard shortcuts, pointer and focus behaviour, the Mac menu bar |
| System controls | Accessibility traits, states, sizes, haptics, right-to-left layout |

**Deviation rule.** Replace a system component only when all three hold, and write them in the
report:

1. the gain is something the user will feel, stated in one sentence;
2. the behaviours given up are listed;
3. each one is either rebuilt (accessibility, keyboard, pointer, Reduce Motion) or accepted as a
   stated loss.

A screen built from standard parts with good tokens and good springs usually beats a custom one.

## What the system gives the user, and a design never takes away

- The back swipe from the leading edge, and the back button.
- Scrolling with the system's speed, inertia and rubber banding, including tap on the status bar
  to scroll to top.
- A sheet's own swipe-to-dismiss, unless there is unsaved input, in which case confirm.
- Text size, Bold Text, Dark Mode, Increase Contrast, Reduce Motion, Reduce Transparency.
- Text selection and system edit menus in text the user may want to copy.
- On iPad and Mac: pointer hover, keyboard focus, standard shortcuts.
- On Mac: the menu bar, window resizing, closing, minimising and full screen, undo.
- Safe areas. Controls and text stay inside them; backgrounds extend beyond them.

## Idioms by platform

Design for the idiom, not the device model. Size classes and window sizes change at runtime (iPad
multitasking, window resizing, iPhone apps on iPad and Mac).

| | iPhone | iPad | Mac |
| --- | --- | --- | --- |
| Top-level sections | Tab bar, two to five peers | Sidebar, or a tab bar that adapts to one | Sidebar in a split view |
| Hierarchy | Push in a navigation stack | Split view: sidebar, content, detail | Split view, with an optional inspector |
| A self-contained task | Sheet | Sheet or popover | Sheet on the window, popover, or a new window |
| Where commands live | Navigation bar and toolbar; context menus as a shortcut | The same, plus keyboard shortcuts | Menu bar first; toolbar for the frequent ones; context menus as a shortcut |
| Primary action | One prominent control in easy reach, or the trailing bar item | The same | Default button (Return) or a toolbar item, and always a menu command |
| Input | Touch | Touch, pointer, keyboard, Pencil | Pointer and keyboard |
| Targets | 44 by 44 points minimum | 44 by 44 points minimum | System control sizes; denser is expected |
| Density | One column, generous | Columns appear with regular width | Dense, several panes, resizable |
| Settings | In the app or the Settings app | The same | A Settings window on Command-comma |

Points that are easy to get wrong:

- **A tab bar is navigation, not a control.** It switches between peer sections and stays
  visible. It does not trigger actions and does not change with the current screen. For views of
  the same content, use a segmented control.
- **A sheet is a task with an end** (compose, pick, edit). Use a push for moving deeper into
  content. Do not put navigation that the user cannot get out of inside a sheet.
- **A context menu is a shortcut,** never the only route to an action.
- **A Mac app is not a wide iPhone app.** Every command is in the menu bar with a shortcut,
  windows resize to useful minimums, and hover and focus states exist. See `appkit.md`.
- **An iPad app is not a stretched iPhone app.** In regular width, use the space for a second
  column; do not centre a phone layout.

## Adaptivity is part of the layout

These are conditions of the design from the first build, not a later pass. The constraint sheet
records each one.

- **Dynamic Type.** All text uses text styles or scaled metrics. At the accessibility sizes,
  side-by-side layouts restack vertically and nothing truncates the main content.
- **Light and dark, and Increase Contrast.** Every colour is semantic or an asset with both
  appearances.
- **Reduce Motion.** Replace overshoot, parallax and large zooms with a cross-fade or a spring
  with no bounce. The interaction model stays the same.
- **Reduce Transparency.** Materials become opaque; check that contrast holds.
- **Differentiate Without Colour.** State is never carried by colour alone: add a symbol or text.
- **VoiceOver and Voice Control.** Every control has a label; a custom gesture has an accessible
  alternative (an accessibility action, or a visible control).
- **Right-to-left and long strings.** Use leading and trailing, never left and right. Layout
  survives a label twice as long.
- **Size classes and window sizes.** Check the smallest and largest width the screen can have.

## Type, colour, symbols

- **Type.** The system font, through text styles. A second family is a brand decision that the
  project has already made; scale it relative to a text style.
- **Colour.** Semantic system colours for text, backgrounds, fills and separators. One accent:
  the app's tint. Red is for destructive actions. Custom colours live in the asset catalogue with
  light, dark and high-contrast values.
- **Symbols.** SF Symbols, sized by the text style beside them. Check the meaning of a symbol
  before reusing one that the system uses for something else.

## Materials and Liquid Glass

On OS versions with Liquid Glass (26 and later):

- Glass belongs to the **control and navigation layer** that floats above content: bars,
  toolbars, tab bars, sheets, floating controls. Content is not glass.
- Let the system bars supply it. Remove custom bar backgrounds, hard separators under bars and
  opaque overlays that were added for older designs; content scrolls under the bars.
- Use custom glass for a few floating controls, grouped in one glass container so they blend
  correctly. Never stack glass on glass.
- Nested shapes are concentric with their container, down to the corners of the device or window.
- Tint glass only to mark the primary action.

On earlier targets, use the system materials for the same layer and keep content opaque. Guard
newer APIs with availability checks, and give the fallback the same layout.

## Where this skill's limits meet the system

- **"At most three text styles per screen"** counts the content. The navigation title, tab bar
  and toolbar are the system's and are not counted.
- **"One accent"** is the app tint. Destructive red and status colours are separate.
- **"One primary action"** means one prominent control. Toolbar items are quiet by default; give
  the prominent style to one at most.
- **"One signature interaction"** lives in the app's own content and transitions. Do not
  restyle or re-time system bars, sheets or the back gesture to make it.

## Gate for this file

- Each top-level structure is the idiom for its platform, or the deviation is in the report.
- Every replaced system component has its gain, its losses and its restorations written down.
- Nothing in the list of what the system gives the user is blocked.
- The adaptivity list was checked, and the report says under which settings.

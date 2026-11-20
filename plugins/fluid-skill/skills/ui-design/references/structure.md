# Structure: the One Thing and the navigation idiom

Steps 1 and 2 of the loop. Do this in words before any pixels; it takes minutes and removes most
later rework.

## The One Thing

Write these down in the design sheet:

- **One Thing sentence.** "The job this screen does is ___." One sentence. If it needs "and",
  there are two screens or the priority is undecided.
- **Primary action.** Exactly one prominent control per screen. A second control of the same
  visual strength is a design error, not a variant. Secondary actions exist, but they are
  visibly quieter (a plain bar item, a row, a menu).
- **The half-second check.** Could a first-time user say within half a second where to look
  first and what to do next? If not, there is no hierarchy yet.

The One Thing is concrete enough that an element can fail to serve it: "see today's recordings
and start a new one", not "manage audio".

Things that break the One Thing:

- Listing every stakeholder's feature at equal weight. Decide each feature's place by its
  contribution to the sentence.
- Asking for sign-in, an account or a permission before the user has experienced the value. Let
  them make, touch or play first. Ask for a permission at the moment the feature needs it, and
  for an account at the moment they want to save or sync.
- Two names for the same destination, or a tab that only leads to a sign-in wall.

## Give the composition a direction

For a new screen or exploration, write a concrete hypothesis: what carries the visual character,
which element gets the strongest emphasis, how content is grouped, and what stays quiet. For
example, make the timeline the main surface and keep transport controls compact, or separate
primary playback from editing tools. These are composition decisions, not decoration presets.

Native behaviour does not require default styling everywhere. Use system navigation and input
behaviour while making hierarchy visible through alignment, scale, density, imagery and surface
grouping. Adding cards, shadows or ornaments without a content reason is not a direction.

## Place the content in the platform's structure

1. **Inventory** all content and features. Weight each by importance to the app and interest to
   the user.
2. **Top-level sections.** If the app has peer areas, they are tabs on iPhone and a sidebar on
   iPad and Mac. Two to five on a phone. If there are more, the grouping is wrong; do not add a
   "More" tab or a hamburger menu.
3. **Hierarchy.** Moving deeper into content is a push. Each row or card on a screen is the
   entrance to one deeper screen.
4. **Tasks.** A self-contained task with an end is a sheet (or a popover or window on larger
   screens). It has a clear way to finish and a clear way to cancel.
5. **Commands.** Frequent commands go in the bar or toolbar; the rest go in a menu. On the Mac,
   every command is also in the menu bar.
6. **Order within a screen.** Most important first. People scroll, but attention falls with
   depth.

See `platform.md` for the idiom table per device.

## Disclosure adds depth; it does not hide the screen's job

- **Level 0:** the first screenful shows the One Thing and the content it is about. A list
  screen shows the list, not a banner and a button that leads to the list.
- **Level 1:** details, one push or one sheet away.
- **Deeper:** settings, long explanations, rarely used options.

Easy to over-apply. A screen that tucks its main content behind sheets and disclosure groups
looks tidy and feels empty.

- **Everything the brief states is reachable without hunting.** List the facts and features the
  user gave you. Each one is on the screen, or one obvious tap away with a label that names it.
- **Show, do not describe.** If the screen is about adjusting colour, the working control is on
  the screen. A row of text that mentions a feature is a description of a screen.
- **Quiet is not empty.** Parts that are not the showstopper are calm, but they carry the same
  care (the same spacing, type and colour world) from top to bottom.
- **Empty, loading and error states are part of the structure.** Decide them now. An empty list
  says what will appear there and offers the primary action.

## Anti-patterns

- **The screen's job behind a segmented control or a disclosure.** Treat what sits behind the
  second segment as unseen. If it matters, show it, or make it its own section.
- **A custom navigation scheme** (hamburger menu, floating tab bar with different behaviour,
  gesture-only navigation) where the platform has a standard one.
- **Mile wide, inch deep.** Showing everything at once at the same shallow weight.
- **Decoration standing in for content.** Abstract illustration and looping motion do not
  explain a feature. A small motion earns its place only if it explains something.
- **A header added to avoid writing the row.** Put the important information in the content.
  Extra header levels are how a screen ends up with five text styles.
- **An alert for something that is not urgent.** Alerts interrupt. Use them for decisions that
  cannot wait, and inline messages for everything else.

## Showstopper and quiet

Choose one or two components that are meant to take all the attention: the live content, an
object the user can manipulate, the thing the app is for. Everything else is deliberately quiet
and standard. A screen where every part shouts has no One Thing.

## Gate for these steps

- No element contradicts the One Thing sentence.
- The first screenful shows the content the screen is about.
- Top-level structure uses the platform idiom (`platform.md`).
- Every fact in the brief is on the screen or one labelled tap away.
- Sign-in and permissions come after value, at the moment they are needed.
- Empty, loading and error states are decided.
- Every remaining element can be justified in one sentence. If it cannot, remove it.

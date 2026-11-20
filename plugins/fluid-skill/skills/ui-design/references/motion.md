# Motion and interaction

Steps 4 and 6 of the loop. The standard is simple to state: the user's thought can be
interrupted at any moment, so the UI must be interruptible at any moment. A UI that makes the
user wait for its animation has failed, however good the animation looks. This is how the
system's own interface behaves: the Home gesture, sheets and scroll views can all be caught and
redirected mid-flight, and an app that cannot feels foreign beside them.

Gesture, animation and haptics are features with the same standing as any other feature, not
finishing touches.

## Sketch states before building

For each main interaction, draw plain boxes and arrows. No visual design. The sketch must show:

- the start state and the end state,
- what the element does while it is being dragged,
- where it lands on release, for both a slow and a fast release,
- what happens on an interruption: a tap elsewhere mid-animation, a reverse mid-animation, a
  second touch mid-animation,
- on iPad and Mac, how the same change is made by pointer and by keyboard.

Example in words: tap the mini player, it expands; while it collapses after a swipe down, tap
it again; it expands from wherever it currently is. A typical expanding panel has five states
(collapsed, expanding, expanded, dragging, collapsing), and **every arrow keeps the current
position and velocity**. Put the sketch in the design sheet (a Mermaid state diagram or ASCII
boxes). The same picture is readable by the human and by an agent, which is why it beats a
paragraph of adjectives.

For complex visuals (shaders, particles, physics), do not generate the final look in one step.
Build an intermediate representation of the structure first, confirm it, then build on top.

## Interruptibility

Rules:

1. Every animation accepts input while it runs. Input lock time is zero. Never disable a
   control, turn off hit testing or user interaction, or keep an "isAnimating" guard to hold the
   user out until an animation completes.
2. A new target starts from the **current** position and velocity. Cancelling does not jump to
   the start or the end.
3. A dragged element follows the finger with no lag (set the position directly; do not animate
   toward the finger). On release it keeps the release velocity.
4. Nothing is queued. Twenty rapid taps end in the state of the last tap, with no animations
   replaying afterwards.

The mechanism that gives all four is the same in every framework: **animate with springs whose
state is (position, velocity, target), and express every change as a new target.** Fixed-duration
easing curves fail rule 2 because they have no velocity to continue from. Completion handlers are
for cleanup, never for unlocking the UI.

Decide where a release lands from the **projected** end position (position plus momentum), not
the position at release, so a quick flick commits from anywhere.

Continuity when the reference changes: if an animated element is defined relative to something
that can change mid-flight (a detail that grows out of card A, and the user taps card B while it
is closing), a naive switch teleports the element. Start the new transition from the element's
presented frame at that moment.

How each framework does this: `swiftui.md`, `uikit.md`, `appkit.md`.

### The four tests

Run all four on every interactive transition. All must pass.

1. **Interrupt tap.** While it opens, tap something else. The other thing responds at once.
2. **Reverse.** While it closes, trigger open again. It turns around smoothly: no jump, no
   restart from the beginning.
3. **Drag reversal.** Drag part of the way, then drag back. The element stays under the finger
   the whole time; no animation takes it away.
4. **Rapid taps.** Hammer the trigger. State stays consistent and nothing replays later.

Run them by hand with slow animations on (Simulator: Debug → Slow Animations), and on a device
before calling item 4 of the gate a pass: touch and a simulator pointer differ. A screen
recording at slow speed is the evidence. Report the result of each test and where it was run. If
nothing was run, the result is "not verified".

## Prefer the system's transitions

The system presentations are already interruptible, gesture-driven and accessible. Use them
before building a custom one.

- **Sheets** with detents for a task or a detail that sits above the content. The user resizes
  and dismisses them by drag.
- **Push** for moving deeper, with the back swipe.
- **Zoom transitions** (iOS 18 and later) when a card or thumbnail becomes the detail. They can
  be dragged back and reversed.
- **Paging scroll views** for moving between siblings inside a detail, so nobody closes and
  reopens to see the neighbour.
- Offer every natural way out: swipe, the back or close control, and Escape or Command-W with a
  keyboard.

Build a custom transition only for the showstopper, and then give it the same properties: it
tracks the finger, it can be reversed, and it has a non-gesture route.

## Scroll

Use the system scroll view unchanged. No reimplemented inertia, no altered deceleration except
the system's own options, no blocked rubber banding. Effects may read the scroll position; they
never write it. A custom drag that shares a scroll view's axis must yield to the scroll: give it
the other axis, a dedicated handle, or a gesture relationship.

## Carousels and paging

Build them on a scroll view with the system's snapping (view-aligned or paging), not on a drag
gesture. That gives momentum, rubber banding, trackpad and keyboard support, and no conflict
with vertical scrolling. Show part of the next item so the row reads as scrollable. An optional
signature candidate: on landing, pass a small staggered impulse to neighbouring cards.

## Targets and feedback

- The **whole row or card** is the target. A card that opens only from a small icon fails.
- Press feedback appears on the first frame of touch-down, not on release.
- On iPad and Mac, pointer hover and keyboard focus show which element will act.
- Any effect that needs the user to wait to understand it will be missed. If one moment
  matters, show only that moment: cut the lead-in and the aftermath.

## Haptics

Fire feedback at state boundaries only: a detent snap, a landing, a threshold crossed during a
drag, a success or failure. Never continuously while dragging, and never as decoration. Prepare
the generator before the moment so there is no delay. Use the system's patterns for their
meanings (selection, impact, notification). Mac trackpads have alignment and level-change
feedback for snapping.

## Signature and showstopper

- Choose **one signature micro-interaction** per app: the small landing or reaction people
  would remember. It gets dedicated effort. The test is organic physics: does it look alive?
  Uniform speed and uniform spacing look mechanical. Use a stagger (tens of milliseconds per
  element) and a decaying amplitude.
- Choose **one or two showstoppers** per screen. Every other motion is quiet, uses the plain
  named springs, and exists to support them.
- This detail is evidence of quality, not decoration. It is the last thing to cut.

## Reduce Motion

Respect the setting: replace springs that overshoot with ones that do not, replace large zooms
and slides with a cross-fade, drop ripples and parallax, and do not autoplay. The interaction
model and the interruptibility stay the same; only the flourish goes.

## Performance is part of the design

Launch time, first-transition time and dropped frames during the signature interaction are
design properties. Measure them on the oldest supported device when one is available, and treat a
regression as a design bug.

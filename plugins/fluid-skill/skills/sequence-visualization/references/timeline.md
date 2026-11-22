# Timeline and player

## Scenario data

```js
const opening = [
  {text: 'Start at A'},
  {text: 'Move A → B', edge: 'AB'},
];
const finish = {text: 'Move B → C', edge: 'BC'};
const SCENARIOS = {
  direct: {steps: [...opening, finish]},
  return: {steps: [
    ...opening,
    {text: 'Wait at B', wait: true},
    {text: 'Return B → A', edge: 'BA'},
    opening[1],
    finish,
  ]},
};
```

Define steps as data that `build()` interprets. Keep movement directions in the edge
definitions and reuse steps shared by multiple scenarios.

## Mapping source order to motion

For a real implementation, use its event order and intermediate states to set the
animation order. If a label covers several actions, append those phases in sequence.
For example, start the arrival highlight when the dot reaches the destination. Run
changes at the same timeline position when they should be visible together.

## build(key)

1. Kill the old timeline and any seek tween; reset `svg.innerHTML` with the `<defs>`
   (gradients, grain filter using the current tuning values).
2. Draw the static frame.
3. **Create moving dots and wire highlights before appending tweens.** Set their
   starting positions and visibility so `tl.seek(t)` renders the same state from
   either direction.
4. `tl = gsap.timeline({paused: true, onUpdate: sync, defaults: {ease: C.ease}})`.
5. For each step:
   ```js
   const t0 = tl.duration();
   starts.push(t0);
   tl.addLabel('s' + i, t0);
   // ...append tweens for this step...
   ends.push(tl.duration());
   tl.to({}, {duration: C.gap});   // breathing pause after every step
   ```
6. Seek to points during motion and at rest from both directions. Compare the
   dot positions, visibility, wire highlights and active step.

The example extends the visible wire path into the cards and passes it as SVG path
data to `motionPath`. The dot can travel all the way between its resting positions
while the visible arrow keeps its clearance from the cards. Fade the highlight in at
departure and out at arrival.

## Player

- `sync()` finds the active step as the last `starts[i] < t`. Update the row's highlight
  and `aria-current`, scroll it into view if needed, and sync the scrubber, time and
  Play/Pause/Replay controls.
- Next: `goTo(completed + 1)` where `goTo(i)` = `tl.tweenTo(ends[i])` scaled by speed.
- Prev: if mid-step, seek to the end of the previous completed step; else one more back.
- Clicking a step in the list calls `goTo(i)`.
- Scrubber: `tl.progress(value / 1000)`; speed select: `tl.timeScale()`.
- Keys: ← → step and space play/pause. Let inputs, selects and buttons handle their
  native keyboard controls.
- Open at `tl.progress(1)` so the finished state is readable before anyone presses Play.

## Pitfalls already hit

- **`'<'` position after a gap**: the first tween of a step that uses `'<'` points into the
  previous step's gap tween. Use the explicit `t0` for the step's first tweens.
- **GSDevTools does not fire `onUpdate`** on your timeline when it scrubs. Keep the UI in step
  with a ticker: `gsap.ticker.add(() => { if (tl.time() !== lastT) { lastT = tl.time(); sync(); } })`.
- Mojibake when serving locally: put `<meta charset="utf-8">` first (artifacts add their own).
- `gsap.set` on an element *before* it appears in the timeline sets its resting position;
  later tweens animate from there. Use it for start positions of hidden objects.

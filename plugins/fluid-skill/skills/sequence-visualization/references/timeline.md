# Timeline and player

## Scenario data

```js
const SCENARIOS = {
  before: { insert: 'front', steps: [
    {kind: 'commit', text: 'Commit v1'},
    {kind: 'deliver', to: '1A', text: 'Deliver v1 to sink A'},
    {kind: 'inner', text: 'Sink A commits v2'},
    ...
    {kind: 'verdict', text: 'B and C receive v2 before v1'},
  ]},
  after: { insert: 'back', steps: [...] },
};
```

Define steps as data that `build()` interprets. Share common opening steps and
represent variation with scenario data such as `insert: 'front' | 'back'`.

## Mapping source order to motion

Start from the real entry point and trace each scenario through the code. Record the
order, direction, and visibility of each change. When a label covers several related
actions, model them as ordered phases inside the step. A phase can pair a movement with
a state change at arrival, or change state by itself. Append each phase's tweens before
starting the next one. Use simultaneous tweens for changes the source exposes together.

In a lazy dependency graph, for example, a write can mark a direct edge pending and
propagate invalidation to downstream nodes. A later read can then recalculate upstream,
replace the dependencies read during the calculation, and compare the old and new
values. Show dependency reads in the reader-to-source direction and returned values in
the opposite direction. Draw an outgoing pending update only on the branch where the
comparison changes the value. Show the cached downstream value on the equal branch.

Check these intermediate states with a focused runtime trace where possible. Then seek
to the corresponding phases in the animation and check both paths through the timeline.
Matching final values alone misses errors such as a downstream update appearing before
the comparison that triggers it.

## build(key)

1. Kill the old timeline and any seek tween; reset `svg.innerHTML` with the `<defs>`
   (gradients, grain filter using the current tuning values).
2. Draw the static frame.
3. **Create every dynamic object up front, hidden (`opacity:0`)** — event dots, one mover per
   delivery, received dots, delivery-order dots and the feedback dot. Build them before
   playback, including any allocated while appending tweens. The same `tl.seek(t)`
   must render the same state from either direction.
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
6. Track model state in plain JS while building (queue order, counts per receiver, highest
   version seen) and derive visuals from it — e.g. a received dot is "wrong" when its
   version is lower than the highest that receiver has already seen.

Useful tween shapes:
- travel along a wire: `tl.to(dot, {motionPath: {path: wireEl, align: wireEl, alignOrigin: [0.5, 0.5]}, duration: C.travel})`
- departure nudge: `{scale: 1.12, yoyo: true, repeat: 1, duration: 0.14, ease: 'sine.inOut'}`
- pop in: `fromTo(el, {opacity: 0, scale: 0.5}, {opacity: 1, scale: 1, duration: C.pop, ease: C.popEase})`
- queue re-layout: tween each item's `x` to its slot and opacity to 1 (head) or `C.pausedOpacity`
- "cut in line" emphasis: small vertical yoyo (`y: -5, repeat: 3`)
- verdict: pulse the wrong marks (`scale 1.15, yoyo, repeat 3`); if none, an empty 0.6s tween

Always set `transformOrigin: '50% 50%'` when scaling SVG groups.

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

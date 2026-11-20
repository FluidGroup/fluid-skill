# Dials: expose parameters and structure

Step 7 of the loop, and the place to come when stuck. Tuning by conversation is slow and lossy:
"a bit snappier" becomes a guess, the guess is rebuilt, and the human compares it from memory.
Put the values on a panel and let the human move them while watching the result, on a device.

## The panel

Build it as soon as the first interaction works, not at the end.

- **Debug only, and separate.** It lives in a playground target or in its own file wrapped in
  `#if DEBUG`. It never ships. The app's views and models never read from it directly: they read
  token accessors that a debug build may override in one place. The product UI has no control
  that opens it. Previews and tests use the constants, not persisted dial overrides.
- **Every tunable value has a name** that matches the constraint sheet (`spring.sheet`
  duration and bounce, `drag.resistance`), a range, a step and a visible current value.
- **Changes apply live**, with no rebuild.
- **Copy values.** One control copies all current values as text, so they can be pasted back
  into the sheet.
- **Reset.** One control returns to the sheet's values.

Open it from outside the screen's own UI: a shake, a debug menu the project already has, a
separate window or menu item on the Mac, or a dedicated preview. Present it as a sheet with a
medium detent or in an inspector, so the interaction being tuned stays visible beside it.

What to expose (choose per project):

| Group | Values |
| --- | --- |
| Motion | duration and bounce per named spring, drag resistance, dismiss threshold, projection factor, stagger interval, ripple amplitude and decay |
| Visual | blur radius, background scale and opacity, shadow strength and offset, how strongly a background follows content |
| Layout | gap, padding, image share, snap threshold |

The framework files show the form: `swiftui.md`, `uikit.md`, `appkit.md`.

## Structure toggles

The second purpose of the panel is to **show what is underneath**, because a generated
implementation can look right while being wrong. Add toggles for:

- **Layout guides:** the layout margins, the readable width and the safe area drawn over the
  screen.
- **Hit areas:** every interactive target outlined, so small or overlapping targets show.
- **State readout:** a live text display of each interaction's state machine (state name,
  progress, velocity, target). This is what makes an interruption bug obvious in one look.
- **Slow motion:** run animations at about 0.2× so reversals and hand-offs can be watched.
- Anything domain-specific: the collision shapes, the layer stack, the path a gesture took.

The system's own tools show the rest without code: the view hierarchy debugger, the Accessibility
Inspector, the environment overrides for text size and appearance, and the simulator's slow
animations and colour-blended-layer options.

## Closing the loop

When the human settles on values:

1. Copy them from the panel.
2. Write them into the constraint sheet, replacing the old ones, and into the token constants.
3. Fold the panel away.

Do not finish with the panel acting as the only record of the design.

## When stuck

If the result does not match the intent, do not answer with a stronger prompt. Suspect these in
order:

1. **A replaced system component.** "It does not feel native" usually means a standard
   component, transition or gesture was rebuilt. Put the system one back and compare.
2. **The underlying structure.** Turn on the structure toggles and look. Is the layout, the
   state machine or the hit area actually what was intended?
3. **A missing dimension in the instruction.** A state that was never specified, the release
   velocity, the appearance, the text size. Models fill unspecified dimensions with the average.
4. **A decomposition that is too coarse.** Split the task into parts that can each be judged
   alone and do them one at a time.

**Second-agent diagnosis.** If still stuck, give a different agent the source material and a
screenshot or recording of the current output, and ask only: "Why do you think the implementing
agent does not understand this? Which dimension of the instruction is missing?" Ask for
diagnosis, not code. Rewrite the instruction from the answer.

**Copy to learn.** When an interaction feels wrong and you cannot say why, rebuild an excellent
existing one (a system app's sheet, a card transition) to find out how it works. Record it at
slow speed and step through the frames. Many attempts are normal. Keep a one-line log of what
each attempt changed, so no attempt is repeated.

## Minimum for a small task

Even for one component: expose its two or three motion values and a state readout. That is
enough to tune by hand and to see interruption bugs.

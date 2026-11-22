# Tuning panel

The user tunes feel by hand; don't iterate timing through chat. Every duration, ease, size,
opacity and effect strength lives in one object:

```js
const DEFAULTS = {
  travel: 0.9, commitTravel: 1.0, gap: 0.45, shift: 0.45, pop: 0.35,
  ease: 'power2.inOut', popEase: 'back.out(2.5)',
  eventSize: 16, moverSize: 11, recvSize: 13,
  pausedOpacity: 0.4, glow: 0.22, grain: 0.16,
  devtools: false,
};
const C = Object.assign({}, DEFAULTS);
try { Object.assign(C, JSON.parse(localStorage.getItem('<page-id>-tuning') || '{}')); } catch (e) {}
function saveConfig() { try { localStorage.setItem('<page-id>-tuning', JSON.stringify(C)); } catch (e) {} }
```

`build()` reads only from `C`. Nothing in the timeline uses a literal that someone might want
to tune (small fixed nudges like 0.14s are fine).

## lil-gui

- Mount in the side column: `new lil.GUI({container: document.getElementById('tune'), title: 'Tuning'})`.
- Folders: **Timing (seconds)**, **Easing** (dropdown of named eases), **Look** (sizes, opacity,
  glow, grain). Give every control a plain-language `.name()`.
- `gui.onFinishChange(rebuild)` where `rebuild()` keeps the current progress:
  `const p = tl.progress(); build(scenario); tl.timeScale(speed); tl.progress(p); sync(); attachDevtools(); saveConfig();`
- Extra buttons: GSDevTools toggle, **Copy settings as JSON** (clipboard, falling back to a
  read-only textarea that is revealed and selected), **Reset to defaults**.
- Theme it with lil-gui's CSS variables to the page tokens (surface background, raised
  widgets, green number/slider fill, 12px font, 16px panel radius).

When the user pastes JSON back, write those values into `DEFAULTS` so they become the
shipped defaults.

## GSDevTools

Optional, off by default (it covers the bottom of the page):

```js
dev = GSDevTools.create({animation: tl, globalSync: false, persist: false, paused: true, css: {zIndex: 60}});
document.body.style.paddingBottom = '96px';
```

Kill and re-create it after every rebuild, since the timeline object changes.

## Artifact vs whiteboard

Publish as a normal HTML artifact. Canvas/whiteboard-style artifact types cannot run these
scripts, so they cannot host the timeline or the tuning panel.

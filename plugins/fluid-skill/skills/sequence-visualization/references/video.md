# Video export

Screen-recording a GSAP page drops and duplicates frames. Instead, `scripts/render.mjs`
pauses the timeline and calls `tl.seek(t)` for every frame, screenshots `#frame`, and pipes
the frames to ffmpeg. The output is frame-exact at any fps and resolution.

## Setup (once, in a work folder outside the skill)

```bash
cp <skill>/scripts/render.mjs <skill>/scripts/package.json .
npm install
npx playwright install chromium
```

Known trouble:
- npm may block `ffmpeg-static`'s install script; run `node node_modules/ffmpeg-static/install.js`.
- If `playwright install` hangs while extracting, unzip the downloaded
  `playwright-download-chromium-*.zip` from `$TMPDIR` into a folder and pass
  `CHROMIUM=<path to the Chromium executable>`. Do not try to strip macOS quarantine
  attributes; serve the page over `http://localhost` instead of `file://`.

## Run

Serve the page (e.g. `python3 -m http.server 8731`), then:

```bash
NAME=my-sequence node render.mjs http://localhost:8731/page.html 60
```

Arguments: `<url> [fps=60] [subframes=1] [shutterDegrees=180] [maxSeconds]`.
Env: `NAME` (file prefix), `OUT_DIR` (default `./out`), `CHROMIUM`.

What it does:
- viewport 1280×900 at deviceScaleFactor 1.5, so the video is 1920px wide; the height
  follows the frame's content
- adds `export render` to `<html>`, so only `#frame` is laid out, at exactly 1280px and
  without its dashed outline, then screenshots that element for every frame
- renders each key of `SCENARIOS` (clicking `#sc-<key>`), holds the first frame 0.5s and
  the last 2s, encodes H.264 (crf 16, yuv420p, faststart), then concatenates all
  scenarios into `<NAME>.mp4` alongside `<NAME>-<key>.mp4`
- `maxSeconds` limits each scenario for quick test renders

Use "Preview video frame" in the page to see what will be recorded before rendering.

## Motion blur

Pass `subframes > 1`: each output frame averages that many renders spread over the shutter
interval (180° = half a frame, like film). ffmpeg does the averaging:
`tmix=frames=N,select='eq(mod(n+1,N),0)'`. Files get a `-mb` suffix.

```bash
NAME=my-sequence node render.mjs http://localhost:8731/page.html 60 8 180
```

- Stronger blur: raise the shutter angle to 270–360.
- Visible stepping/ghosting on fast moves: raise subframes to 16 (render time doubles).
- Static elements stay sharp; only moving dots smear along their path.

Check a few frames (`ffmpeg -ss 7.2 -i out.mp4 -frames:v 1 f.png`) before handing over, and
say which parts you did not watch.

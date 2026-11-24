# Video and GIF export

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
- To use an installed ffmpeg, set `FFMPEG_BIN` to its executable path.
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
- uses a 1280×900 browser viewport at deviceScaleFactor 1.5 and captures the starter's
  1280×720 frame at 1920×1080
- adds `export render` to `<html>` to hide the page controls and remove the scale
  and dashed outline, then screenshots `#frame` for every frame
- renders each key of `SCENARIOS` (clicking `#sc-<key>`), holds the first frame 0.5s and
  the last 2s, encodes H.264 (crf 16, yuv420p, faststart), then concatenates all
  scenarios into `<NAME>.mp4` alongside `<NAME>-<key>.mp4`
- `maxSeconds` limits each scenario for quick test renders

Use “Preview video frame” to inspect the same 16:9 composition before rendering.
For a short test export, check the encoded width and height with `ffprobe`.

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

## GIF export

Use gifski (on macOS, `brew install gifski`). Export one GIF per scenario at 1280 × 720
(16:9), targeting 24 fps. Average four temporal samples per frame with a 180° shutter
(half a frame, about 20.8 ms). Keep the first frame visible for 0.5 s and the last for
2 s, then loop indefinitely. Start at gifski quality 90.

Run the bundled renderer at 24 fps to generate the numbered PNG sequences in
`gif-render/frames-<scenario>-mb/`. Feed those PNGs directly into gifski to preserve
the render quality. The holds are added below because the PNG sequences contain
the timeline frames only.

```sh
OUT_DIR=gif-render node render.mjs http://localhost:8731/page.html 24 4 180

for frames in gif-render/frames-*-mb; do
  (
    set -- "$frames"/*.png
    first=$1
    for last do :; done

    for i in $(seq 12); do set -- "$first" "$@"; done
    for i in $(seq 48); do set -- "$@" "$last"; done

    scenario=${frames##*/frames-}
    gifski --fps 24 --width 1280 --height 720 --quality 90 --repeat 0 --no-sort \
      --output "gif-render/${scenario%-mb}.gif" "$@"
  )
done
```

Inspect a moving frame and the last held frame in each GIF. If the shutter interval
straddles an instant label, step, or receipt change and makes it look doubled, adjust the
capture to use only the center sample for that frame. Verify 1280 × 720, timing and
looping on the encoded GIFs. GIF delays use 10 ms units, so 24 fps is represented by
a mix of 40 ms and 50 ms delays during motion. Identical frames can share a longer delay.

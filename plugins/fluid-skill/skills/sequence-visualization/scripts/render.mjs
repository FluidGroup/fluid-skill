// Renders a sequence-visualization page's GSAP timeline frame by frame and encodes MP4s.
// usage: node render.mjs <page-url> [fps] [subframes] [shutterDegrees] [maxSeconds]
// env: OUT_DIR (default ./out), NAME (file prefix, default "sequence"),
//      CHROMIUM (executable path; default: Playwright's bundled browser)
// page contract: globals `tl`, `sync`, `SCENARIOS`; buttons `#sc-<key>`; a `#frame` element holding
// everything the video shows, styled for the `html.export.render` classes (fixed 1280px, no outline).
//   subframes > 1 adds motion blur: each output frame averages that many renders
//   spread across the shutter interval (180 deg = half a frame, like a film camera).
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import ffmpeg from 'ffmpeg-static';

const url = process.argv[2];
const FPS = Number(process.argv[3] || 60);
const SUB = Number(process.argv[4] || 1);
const SHUTTER = Number(process.argv[5] || 180);
const MAX_SECONDS = Number(process.argv[6] || Infinity);
const SUFFIX = SUB > 1 ? '-mb' : '';
const HOLD_START = 0.5;  // seconds on the first frame
const HOLD_END = 2.0;    // seconds on the final frame
const OUT = path.resolve(process.env.OUT_DIR || 'out');
const NAME = process.env.NAME || 'sequence';
mkdirSync(OUT, { recursive: true });

function run(args) {
  return new Promise((resolve, reject) => {
    const p = spawn(ffmpeg, args, { stdio: ['ignore', 'ignore', 'pipe'] });
    let err = '';
    p.stderr.on('data', d => { err += d; });
    p.on('close', code => (code === 0 ? resolve() : reject(new Error(err.slice(-2000)))));
  });
}

const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: path.resolve(process.env.CHROMIUM) } : {});
const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1.5 });
await page.goto(url, { waitUntil: 'networkidle' });

// The page marks the recorded area as #frame. Render mode fixes it at 1280px wide and hides the rest.
await page.evaluate(() => document.documentElement.classList.add('export', 'render'));

const scenarios = await page.evaluate(() => Object.keys(SCENARIOS));
const parts = [];
for (const key of scenarios) {
  const dur = await page.evaluate((key) => {
    document.getElementById('sc-' + key).click();
    tl.pause(); tl.seek(0); sync();
    return tl.duration();
  }, key);

  const dir = path.join(OUT, 'frames-' + key + SUFFIX);
  rmSync(dir, { recursive: true, force: true });
  mkdirSync(dir, { recursive: true });
  const el = await page.$('#frame');
  const total = Math.ceil(Math.min(dur, MAX_SECONDS) * FPS);
  const open = (SHUTTER / 360) / FPS;   // seconds the virtual shutter is open
  // subframes are piped straight into ffmpeg, which averages each group of SUB into one frame
  const mix = spawn(ffmpeg, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS * SUB), '-i', '-',
    '-vf', SUB > 1 ? `tmix=frames=${SUB},select='eq(mod(n+1,${SUB}),0)'` : 'null',
    '-fps_mode', 'passthrough', '-start_number', '0', path.join(dir, '%05d.png')], { stdio: ['pipe', 'ignore', 'inherit'] });
  const done = new Promise((res, rej) => mix.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg mix failed')))));
  const write = buf => new Promise(res => (mix.stdin.write(buf) ? res() : mix.stdin.once('drain', res)));
  for (let f = 0; f <= total; f++) {
    for (let k = 0; k < SUB; k++) {
      const offset = SUB > 1 ? ((k + 0.5) / SUB - 0.5) * open : 0;
      const t = Math.max(0, Math.min(f / FPS + offset, dur));
      await page.evaluate((t) => { tl.seek(t); sync(); }, t);
      await write(await el.screenshot({ type: SUB > 1 ? 'jpeg' : 'png', quality: SUB > 1 ? 95 : undefined }));
    }
    if (f % FPS === 0) process.stdout.write(`${key} ${f}/${total}\n`);
  }
  mix.stdin.end();
  await done;

  // hold first and last frame, then encode
  const list = [];
  list.push(`file '${path.join(dir, '00000.png')}'`, `duration ${HOLD_START}`);
  for (let f = 0; f <= total; f++) list.push(`file '${path.join(dir, String(f).padStart(5, '0') + '.png')}'`, `duration ${1 / FPS}`);
  list.push(`file '${path.join(dir, String(total).padStart(5, '0') + '.png')}'`, `duration ${HOLD_END}`);
  list.push(`file '${path.join(dir, String(total).padStart(5, '0') + '.png')}'`);
  const listFile = path.join(OUT, `list-${key}.txt`);
  writeFileSync(listFile, list.join('\n'));
  const mp4 = path.join(OUT, `${NAME}-${key}${SUFFIX}.mp4`);
  await run(['-y', '-f', 'concat', '-safe', '0', '-i', listFile, '-vf', `fps=${FPS},scale=trunc(iw/2)*2:trunc(ih/2)*2`,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4]);
  parts.push(mp4);
  console.log('wrote', mp4);
}
await browser.close();

// all scenarios back to back in one file
const both = path.join(OUT, `${NAME}${SUFFIX}.mp4`);
const inputs = parts.flatMap(p => ['-i', p]);
const chain = parts.map((_, i) => `[${i}:v]`).join('') + `concat=n=${parts.length}:v=1[v]`;
if (parts.length > 1) await run(['-y', ...inputs, '-filter_complex', chain, '-map', '[v]',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', both]);
if (parts.length > 1) console.log('wrote', both);

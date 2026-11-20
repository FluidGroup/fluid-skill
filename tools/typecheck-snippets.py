#!/usr/bin/env python3
"""Type-check bundled Swift and reference snippets against the Apple SDKs; nothing is run.

Usage: python3 tools/typecheck-snippets.py
Requires macOS with full Xcode selected via xcode-select (or DEVELOPER_DIR).
"""
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "plugins/fluid-skill/skills/ui-design"
KIT = SKILL / "assets/swift/DesignPlayground.swift"
ARCH = platform.machine()
IOS = ("iphonesimulator", f"{ARCH}-apple-ios17.0-simulator")
MAC = ("macosx", f"{ARCH}-apple-macos14.0")

# Reference, platforms, include the bundled kit.
CASES = [
  ("swiftui.md", [IOS], False),
  ("uikit.md", [IOS], False),
  ("appkit.md", [MAC], False),
  ("variations.md", [IOS, MAC], True),
  ("rendering.md", [IOS, MAC], False),
]


def swift_blocks(markdown: str) -> list[str]:
  return re.findall(r"```swift\n(.*?)```", markdown, flags=re.S)


def assemble(blocks: list[str]) -> str:
  imports: list[str] = []
  body: list[str] = []
  for line in "\n".join(blocks).splitlines():
    if re.fullmatch(r"import \w+", line.strip()):
      if line.strip() not in imports:
        imports.append(line.strip())
    else:
      body.append(line)
  if "import SwiftUI" not in imports:
    imports.append("import SwiftUI")
  return "\n".join(imports) + "\n" + "\n".join(body) + "\n"


def typecheck(source: Path, others: list[Path], sdk: str, target: str, debug: bool) -> tuple[bool, str]:
  command = ["xcrun", "--sdk", sdk, "swiftc", "-typecheck", "-target", target, "-parse-as-library"]
  if debug:
    command += ["-D", "DEBUG"]
  command += [str(source), *map(str, others)]
  result = subprocess.run(command, capture_output=True, text=True)
  return result.returncode == 0, result.stderr


def main() -> int:
  failed = False
  with tempfile.TemporaryDirectory() as directory:
    runs = [
      (f"{KIT.name} ({'DEBUG' if debug else 'release'})", KIT, [], sdk, target, debug)
      for sdk, target in (IOS, MAC) for debug in (True, False)
    ]
    for name, platforms, with_kit in CASES:
      blocks = swift_blocks((SKILL / "references" / name).read_text(encoding="utf-8"))
      if not blocks:
        print(f"FAIL  {name}: no Swift blocks found")
        failed = True
        continue
      source = Path(directory) / (Path(name).stem + "_snippets.swift")
      source.write_text(assemble(blocks), encoding="utf-8")
      for sdk, target in platforms:
        runs.append((f"{name} ({len(blocks)} blocks)", source, [KIT] if with_kit else [], sdk, target, True))
    for label, source, others, sdk, target, debug in runs:
      ok, errors = typecheck(source, others, sdk, target, debug)
      print(f"{'ok  ' if ok else 'FAIL'}  {label}  {target}", flush=True)
      if not ok:
        failed = True
        print(errors)
  return 1 if failed else 0


if __name__ == "__main__":
  sys.exit(main())

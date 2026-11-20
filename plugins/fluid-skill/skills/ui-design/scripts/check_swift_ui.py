#!/usr/bin/env python3
"""Source check for Apple-platform UI code (SwiftUI, UIKit, AppKit).

Reads Swift files and reports lines that break the constraint sheet or the interaction rules.
The findings are leads, found by pattern matching; confirm each one in the code. A clean run
does not prove the design is right.

Usage:
  python3 check_swift_ui.py <file-or-directory>... [--scale 4,8,12,16,20,24,32,48,64] [--json]

Suppress one line with a trailing comment:  // design-check: ignore
Exit status is 1 when there are findings, 0 otherwise.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_SCALE = "4,8,12,16,20,24,32,48,64"

SPACING_CALL = re.compile(
    r"\.(?:padding|contentMargins|listRowSpacing|scenePadding)\(([^()]*)\)"
    r"|\b(?:spacing|interGroupSpacing|interItemSpacing|minimumLineSpacing|minimumInteritemSpacing)\s*[:=]\s*(-?\d+(?:\.\d+)?)"
)
RADIUS_CALL = re.compile(r"\b(?:cornerRadius|cornerSize)\s*[:=(]\s*(-?\d+(?:\.\d+)?)")
NUMBER = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])")
INSETS = re.compile(r"\b(?:NSDirectionalEdgeInsets|UIEdgeInsets|NSEdgeInsets|EdgeInsets)\(([^()]*)\)")

LINE_RULES = [
    ("fixed-font-size",
     re.compile(r"\.font\(\s*\.system\(size:|\bFont\.system\(size:|\b(?:UIFont|NSFont)\.systemFont\(ofSize:\s*\d|\.systemFont\(ofSize:\s*\d|Font\.custom\([^)]*size:\s*[\d.]+\s*\)"),
     "Fixed font size. Use a text style, or scale it (relativeTo:, @ScaledMetric, UIFontMetrics)."),
    ("hard-coded-colour",
     re.compile(r"\b(?:Color|UIColor|NSColor)\(\s*(?:\.sRGB\s*,\s*)?(?:red|white|hue|displayP3Red|srgbRed|calibratedRed|deviceRed|hex)\s*:|#colorLiteral\("),
     "Hard-coded colour. Use a semantic system colour or an asset with light and dark values."),
    ("fixed-duration-easing",
     re.compile(r"\.(?:easeInOut|easeIn|easeOut|linear)\b(?:\(duration:)?|\b(?:UIView\.animate|UIView\.transition)\(withDuration:(?![^\n]*usingSpringWithDamping)|CAMediaTimingFunction\(name:"),
     "Fixed-duration easing cannot continue from the current velocity. Use a named spring for interactive changes."),
    ("input-lock",
     re.compile(r"\.allowsHitTesting\(\s*!?\w*[aA]nimat\w*\s*\)|\.disabled\(\s*!?\w*[aA]nimat\w*\s*\)|isUserInteractionEnabled\s*=\s*false|\bis[A-Z]\w*Animating\b|\bisAnimating\b|ignoresMouseEvents\s*=\s*true"),
     "Possible input lock during an animation. Input must never wait for an animation to finish."),
    ("tap-gesture-as-button",
     re.compile(r"\.onTapGesture\s*(?:\{|\(perform:)"),
     "A tap gesture has no press state, accessibility trait or keyboard support. Use a Button for actions."),
    ("screen-size-layout",
     re.compile(r"UIScreen\.main\b|UIDevice\.current\.userInterfaceIdiom"),
     "Layout from the screen or the device idiom breaks in multitasking and on other devices. Use size classes or the container's size."),
    ("left-right",
     re.compile(r"\b(?:leftAnchor|rightAnchor)\b|\.padding\(\.(?:left|right)\b"),
     "Left and right do not flip for right-to-left languages. Use leading and trailing."),
    ("circular-corner",
     re.compile(r"style:\s*\.circular\b|cornerCurve\s*=\s*\.circular"),
     "Circular corner curve beside the system's continuous corners."),
]

OPENS_SPRING = re.compile(r"springDuration|usingSpringWithDamping|UISpringTimingParameters|\.spring|\.snappy|\.smooth|\.bouncy")


def strip_comment(line: str) -> str:
    return re.sub(r"//.*$", "", line)


def off_scale(value: float, scale: set[float]) -> bool:
    return value != 0 and abs(value) not in scale


def check_file(path: Path, scale: set[float]) -> list[dict]:
    findings = []

    def add(number: int, rule: str, message: str, text: str) -> None:
        findings.append({"file": str(path), "line": number, "rule": rule, "message": message, "source": text.strip()})

    for number, raw in enumerate(path.read_text(errors="replace").splitlines(), start=1):
        if "design-check: ignore" in raw:
            continue
        line = strip_comment(raw)
        if not line.strip():
            continue

        for match in SPACING_CALL.finditer(line):
            arguments = match.group(1) if match.group(1) is not None else match.group(2)
            for value in NUMBER.findall(arguments or ""):
                if off_scale(float(value), scale):
                    add(number, "off-scale-spacing", f"{value} is not on the spacing scale. Use a spacing token.", raw)
        for match in INSETS.finditer(line):
            for value in NUMBER.findall(match.group(1)):
                if off_scale(float(value), scale):
                    add(number, "off-scale-spacing", f"{value} is not on the spacing scale. Use a spacing token.", raw)
        for match in RADIUS_CALL.finditer(line):
            value = float(match.group(1))
            if value % 4 != 0:
                add(number, "off-grid-radius", f"Corner radius {match.group(1)} is not a multiple of 4.", raw)

        for rule, pattern, message in LINE_RULES:
            if not pattern.search(line):
                continue
            if rule == "fixed-duration-easing" and OPENS_SPRING.search(line):
                continue
            if rule == "fixed-font-size" and re.search(r"relativeTo:|scaledFont|UIFontMetrics|ScaledMetric", line):
                continue
            add(number, rule, message, raw)
    return findings


def swift_files(arguments: list[str]) -> list[Path]:
    files: list[Path] = []
    for argument in arguments:
        path = Path(argument)
        if path.is_dir():
            files += sorted(p for p in path.rglob("*.swift") if ".build" not in p.parts and "DerivedData" not in p.parts)
        elif path.suffix == ".swift" and path.exists():
            files.append(path)
        else:
            print(f"skipped: {argument} (not a Swift file or a directory)", file=sys.stderr)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--scale", default=DEFAULT_SCALE, help="comma-separated spacing scale in points")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    options = parser.parse_args()

    scale = {float(value) for value in options.scale.split(",")}
    files = swift_files(options.paths)
    if not files:
        print("No Swift files found.", file=sys.stderr)
        return 2
    findings = [finding for path in files for finding in check_file(path, scale)]

    if options.json:
        print(json.dumps({"files": len(files), "findings": findings}, indent=2))
    else:
        for finding in findings:
            print(f"{finding['file']}:{finding['line']}: [{finding['rule']}] {finding['message']}")
            print(f"    {finding['source']}")
        counts: dict[str, int] = {}
        for finding in findings:
            counts[finding["rule"]] = counts.get(finding["rule"], 0) + 1
        summary = ", ".join(f"{rule} {count}" for rule, count in sorted(counts.items())) or "none"
        print(f"{len(files)} file(s) checked. Findings: {len(findings)} ({summary}).")
        print("Findings are leads from pattern matching. Not checked: concentric corners, text-style count, target sizes, anything at runtime.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

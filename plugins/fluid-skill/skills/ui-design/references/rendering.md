# Repeatable SwiftUI comparison images

Use when a comparison needs shareable images or repeated exports, not for every spacing fix.
Render the actual comparison View and its deterministic fixtures. Do not recreate its styling
in a second SwiftUI tree, HTML, drawing code or an image editor. Keep the same implementation
behind exports, previews and full-size interactive cases.

Render shared, non-scrolling comparison content. A `ScrollView` or lazy grid may capture only
its viewport or instantiated children, not the entire contact sheet. Arrange an exportable eager
grid from the same variant views, reuse it in the live comparison, and verify that every expected
label and frame is present. Do not claim a complete export from image dimensions alone.

## Persist the small path

In the consuming app repository, keep a small exporter and a command using its existing task
runner (for example, a mise task where mise is already used). Compile the relevant SwiftUI
sources with the exporter or use the existing module; do not copy them into the tool. A macOS
CLI is useful only when those sources support macOS. Do not port an iOS-only feature or add
another app target just to export images; use the existing preview/Simulator host instead.

Fix these inputs explicitly: fixture and variant order, logical width, scale, appearance,
locale, layout direction and Dynamic Type environment. Compare Light/Dark separately. Width
and scale below are export conditions, not production layout constants. The core of an
exporter can be this function; pass the existing comparison View with its fixed fixture:

```swift
import SwiftUI

@available(iOS 16, macOS 13, *)
@MainActor
func renderComparison(_ comparison: some View, scheme: ColorScheme) -> CGImage? {
  let width: CGFloat = 1040
  let scale: CGFloat = 2
  let content =
    comparison
    .environment(\.colorScheme, scheme)
    .environment(\.displayScale, scale)
    .environment(\.locale, Locale(identifier: "ja_JP"))
    .environment(\.layoutDirection, .leftToRight)
    .environment(\.dynamicTypeSize, .large)
    .frame(width: width)
    .background(scheme == .light ? Color.white : Color.black)

  let renderer = ImageRenderer(content: content)
  renderer.proposedSize = .init(width: width, height: nil)
  renderer.scale = scale
  return renderer.cgImage
}
```

The CLI should fail on a missing image or PNG encoding error, create its output directory,
write deterministic Light/Dark filenames, and support an explicit output path. Do not let
an image-writing failure exit successfully. Keep generated images, temporary executables
and render metadata out of Git unless the repository explicitly versions visual baselines.
Clean up temporary executables; never delete unrelated output-directory contents.

Write a small manifest alongside the images: renderer and host platform, all fixed inputs,
actual pixel dimensions, OS/Xcode/Swift versions, Git revision and dirty status, and hashes
of the relevant source files. A commit ID alone does not identify uncommitted UI changes.
Re-run the command to check regeneration, including a path containing spaces. Reproducibility
means the source and conditions can be recovered, not guaranteed pixel equality across OS,
SDK or font updates.

## Inspect and label the evidence

Open the generated images. Check for missing text, placeholder/incorrect platform-backed
controls, clipping and altered geometry; successful encoding and expected image dimensions
do not prove visual correctness. SwiftUI's [ImageRenderer](https://developer.apple.com/documentation/swiftui/imagerenderer)
does not capture every platform-backed view. If the real content cannot be rendered, report
the limitation and use a supported app-host capture; do not quietly substitute an image-only UI.

Label a macOS export **SwiftUI ImageRenderer on macOS — not an iOS Simulator screenshot**.
Setting a Dynamic Type environment on macOS does not establish iOS font scaling. Static
exports also do not prove touch targets, VoiceOver, Reduce Motion, navigation, native-control
behaviour, playback or integration with a live model. Those need the relevant host and checks
in the [review gate](review-gate.md). Do not present a grid of mock states as an interaction test.

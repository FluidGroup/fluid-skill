# Packages

Read when creating or reshaping a Swift package or module: names, manifest,
files, previews, samples, tests, and README. Keep a single-purpose package's
public surface and documentation proportional to the problem it solves.

## Avoid a Package Bigger Than Its Idea

| Size | Shape |
| --- | --- |
| One concept (a wrapper, a property wrapper, a utility) | One source file named after the module or primary type, nested helpers, a `#if DEBUG` sample or preview at the bottom, a README of 10–30 lines |
| One component (a control, a modifier) | One or two source files, previews at the bottom, a README with one example per use case, well under 60 lines |
| A family of features | One product per independently useful feature, each small; a `Development` app for demos |

- Avoid public style or configuration types for visual constants (bar widths,
  insets, tick counts); keep them literal until a caller needs to change one.
- Avoid one file or one extension per conformance in a small package; list
  conformances on the declaration and implement them in the body.
- Split files only when a file holds independent concepts; name extension
  files `Type+Feature.swift`.

## Avoid Names That Need Explaining

- Repository and `Package(name:)`: lowercase slug, `swiftui-<feature>` for
  SwiftUI and `swift-<feature>` otherwise. Product, target, and module: the
  primary type's name without the prefix (`PageIndicator`); test target
  `<Module>Tests`.
- Full domain words (`RemoteImageLoader`, not `RILoader`); a short spelling is
  a typealias, nested in the protocol and bound to `Self` when the alias
  refers to a generic type specialized on the conformer.
- A wrapper's payload is `raw`, `base`, or `value`, not a borrowed tuple label;
  `rawValue` means real `RawRepresentable`.
- Presets are named for behavior (`.firm`, `.unlimited`, `.disabled`), not
  `.default` when a behavioral name exists. A process-wide instance is
  `static let shared`.
- Methods label their closure parameter (`enqueue(work:)`); a free `withX`
  function takes `_ body`; a debugging `label` defaults to `""`.
- A custom control labels its options with the plain nouns of its own
  description (`direction:`, `speed:`, `stride:`, a `…Range` for bounds) and
  borrows a system control's labels only when it stands in for that control.
  Older SwiftUI packages prefixed the module (`SwiftUIPageIndicator`); keep
  that only where a package already does it.

## Avoid a Hand-Tuned Manifest

Start from `swift package init --type library`, re-indented to two spaces, and
fill in real values. Keep its stock comments; add no rationale comments.

```swift
// swift-tools-version: 6.0
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
  name: "swift-retry-policy",
  platforms: [
    .iOS(.v16),
    .macOS(.v13),
  ],
  products: [
    // Products define the executables and libraries a package produces, making them visible to other packages.
    .library(
      name: "RetryPolicy",
      targets: ["RetryPolicy"]
    ),
  ],
  targets: [
    // Targets are the basic building blocks of a package, defining a module or a test suite.
    // Targets can depend on other targets in this package and products from dependencies.
    .target(
      name: "RetryPolicy"
    ),
    .testTarget(
      name: "RetryPolicyTests",
      dependencies: ["RetryPolicy"]
    ),
  ],
  swiftLanguageModes: [.v6]
)
```

- Platforms, one per line even when there is one: a SwiftUI or UIKit
  component lists only iOS unless asked; a framework-neutral utility lists the
  Apple platforms it supports. Use the lowest version the chosen APIs need and
  gate newer APIs per declaration with `@available(iOS 17, *)` instead of
  raising the package.
- Dependencies: the smallest product of another package, versions with
  `from:`, native APIs before project-specific helpers, official packages
  (swift-collections, swift-atomics, `os` locks, `os_log`) before hand-rolled
  primitives, and a copied ten-line helper before a grab-bag dependency.
- No cross-platform branches for Apple-only code.

## Avoid Ceremony Around Verification

- A SwiftUI file ends with its previews:

  ```swift
  #if DEBUG

  private struct BookBadge: View {

    @State var count: Int = 3

    var body: some View {
      VStack {
        Badge(count: count)
        Button("Add") {
          count += 1
        }
      }
    }
  }

  #Preview {
    BookBadge()
  }

  #endif
  ```

- Demo views are the smallest real use: one model, one view, one interaction,
  named `Book<Topic>`, `Demo`, or a plain scenario noun. Declare a demo's model
  and views side by side as `private` file-scope types, not nested in one
  another; each owns its `@State` (no `@Previewable`). Demo types gated with
  `@available` gate their `#Preview` the same way. Use labelled
  `#Preview("Name")` only for distinct configurations; no narrating comments.
- A type-level library without real tests ends with a compile-only
  `#if DEBUG` sample (a placeholder `MyItem`, a `private func _run()`); a
  SwiftUI-facing utility gets one small `#Preview` per usage variant, guarded by
  `#if canImport(SwiftUI)`.
- Tests: logic (concurrency, collections, algorithms, macros) gets a few
  end-to-end Swift Testing scenarios per public type (`@Suite` struct, `@Test`,
  `#expect`) that check final order or values; infrastructure also checks call
  counts, event order, cancellation, and no-op suppression, and backs
  performance claims with `measure`. Views, modifiers, property wrappers, and
  small UI utilities keep the template's placeholder test; a tiny type-level
  library may have none. Avoid fixture-heavy suites and custom synchronization
  helpers.
- A larger UI package adds a `Development` app whose root list links to the
  `Book…` screens.

## Avoid a README That Documents Instead of Shows

````markdown
# Badge

A count badge that pops when the number changes.

<img width=250 src="…" />

```swift
Badge(count: unreadCount)
```
````

- Title in plain words, one to three sentences, an image or GIF for anything
  visual, then one example per use case (a component may use an `## Examples`
  section of bold-titled snippets separated by `---`).
- Link the motivation when there is one (a WWDC session, a forum thread, a
  proposal) instead of explaining it; a package that replaces a common
  workaround may show it in a short `## Motivation` followed by `## Usage`.
- Avoid badges, feature lists, installation and requirements sections, API or
  behavior reference, how-it-works sections, and design rationale.

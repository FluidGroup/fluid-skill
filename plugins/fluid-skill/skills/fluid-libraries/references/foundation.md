# Foundation Utilities and Testing

Read when the need is a small non-UI utility or a testing aid. Most of these
are a few dozen lines; the rule in `SKILL.md` about copying a fragment applies
most often here. Repositories are under `https://github.com/FluidGroup/`
unless a row says VergeGroup.

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| Reading loosely shaped JSON by path, with errors that say which key failed and why | `JAYSON` | `JAYSON`: `JSON`, `json.next("id").getString()`, dynamic member lookup | none | `Codable` is the default for a known schema. Use this for exploratory or partially trusted payloads |
| Buffering items and delivering them in batches (analytics events, logs) with memory or file buffers | `Bulk` | `Bulk`, `BulkLogger` | iOS 16, macOS 11 | The app supplies the target that sends each batch |
| Color literals from hex, checked and expanded at compile time | `swift-macro-hex-color` | `HexColorMacro`: `#hexColor("#BA43F1")`, `#hexUIColorSRGB`, `#hexUIColorP3` | iOS 13 | Brings swift-syntax into the build. An asset catalog is the default for a design system's palette |
| Colors from a hex string or integer at run time | `swiftui-color` | `SwiftUIColor`: `Color(hexString:)`, `Color(hexInt:)` | iOS 13 | A few lines; copy rather than depend when it is the only use |
| String literals that should not appear verbatim in the binary | `Obfuscate` | `Obfuscate`: `#Obfuscate("…")` | iOS 13 | Hides strings from casual inspection only; not a way to protect secrets |
| Comparing a tuple of `Equatable` values as one value | `swift-equatable-box` | `EquatableBox`: `EquatableBox(a, b)` | none | Useful as an `onChange` or `task(id:)` key |
| Timing a block during development | `swift-stopwatch` | `Stopwatch`: `Stopwatch(name:)`, `end()` | none | For measurement before an optimization; signposts are the tool for anything kept |
| Method-chain style `do`, `map`, and `filter` on any value | `swift-operator-wrap` (VergeGroup) | `Wrap`: `value&>.do { … }` | none | A custom operator; only where the project already uses it |

## Testing

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| Unit-testing a `DynamicProperty` struct whose `@State` properties need real SwiftUI storage | `swiftui-dynamic-property-testing` | `DynamicPropertyTesting`: `withDynamicProperty(_:) { state in … }` | iOS 16, macOS 13 | Add to the test target only. Works with Swift Testing and XCTest |

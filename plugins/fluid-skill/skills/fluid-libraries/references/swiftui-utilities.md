# SwiftUI Utilities

Read when the need is one small SwiftUI building block. Each of these is a
single concept; check that the project's deployment target does not already
provide it. Repositories are under `https://github.com/FluidGroup/`.

## State

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| An alert or confirmation that describes a value (an error, the item being deleted) without a separate `Bool` and payload | `swiftui-alert-state` | `SwiftUIAlertState`: `@AlertState`, `$state.present(_:)`, `.alert(_:state:)` | iOS 18, macOS 15 | Keeps the value during the dismissal animation |
| A component usable both self-contained and driven by a caller's `Binding` | `swiftui-abstract-state` | `SwiftUIAbstractState`: `@AbstractState` | iOS 13 | |
| A reference object created once and kept for the view's lifetime on iOS 16 and earlier | `swiftui-object-edge` | `ObjectEdge`: `@ObjectEdge` | iOS 13 | From iOS 17, `@State` holding an `@Observable` object is the native form |
| Re-running a closure every time an `@Observable` read changes, outside a view | `swift-observation-continuous-tracking` | `ObservationContinuousTracking`: `withContinuousTracking` | iOS 17 | Untagged. `Observations` replaces it where the floor allows |

## Layout and Content

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| Children that wrap onto new lines (tags, chips) | `swiftui-WrapLayout` | `WrapLayout`: `WrapLayout { … }` | iOS 16 | A `Layout`; do not measure with `GeometryReader` instead |
| A callback the first time a view becomes visible on screen (impression logging) | `swiftui-on-visible-modifier` | `OnVisibleModifier`: `.onVisible { … }` | iOS 16 | Fires once per view lifetime; `onScrollVisibilityChange` is the native form on iOS 18 when repeated changes are needed |
| `ForEach` with an index without building an array | `swift-indexed-collection` | `IndexedCollection`: `IndexedCollection(items)` | iOS 13 | Replaces `Array(items.enumerated())` and `zip(items.indices, items)` |
| A button style from a closure or a `ViewModifier`, with a processing state | `ButtonStyleModifier` | `ButtonStyleModifier`: `.buttonStyle(ButtonStyleModifier { label, state in … })` | iOS 16 | |
| An image that loads several resolutions and shows the best one for its size | `swiftui-async-multiplex-image` | `AsyncMultiplexImage`, or `AsyncMultiplexImage-Nuke` for the Nuke downloader | iOS 17 | `AsyncImage` is enough for a single URL without caching needs |
| Iterating the subviews of a `Group` before iOS 18 | `swiftui-group-backport` | `swiftui-group-backport`: `VariadicForEach` | iOS 15 | Untagged. `Group(subviews:)` is native on iOS 18 |

## Bridging and Miscellany

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| SwiftUI content inside a UIKit view or cell that sizes itself correctly | `swiftui-Hosting` | `SwiftUIHosting`: `SwiftUIHostingView`, `SwiftUIHostingViewController` | iOS 17 | `UIHostingConfiguration` covers collection and table cells |
| Work that must run just before the current `CATransaction` commits | `swift-with-prerender` | `WithPrerender`: `withPrerender { … }` | iOS 13 | |
| Assorted helpers: size measurement, `onChangeWithPrevious`, corner styles, variadic roots | `swiftui-support` | `SwiftUISupport` and its smaller products (`SwiftUISupportSizing`, `SwiftUISupportLayout`, `SwiftUISupportBackport`, …) | iOS 16 | An unorganized grab bag by its own description. Use it when the project already depends on it; otherwise write or copy the one helper |
| Compiling a function with local `@State` into a `View` struct | `swiftui-functional-component-macro` | `FunctionalViewComponent`: `@ViewComponent` | iOS 13 | Experimental style; only where the project already uses it |

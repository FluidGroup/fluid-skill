# SwiftUI

Read when building a SwiftUI view, modifier, gesture, property wrapper, bridge,
or app screen. Package proportion is in [packages.md](packages.md); ownership
contracts are in `state-and-concurrency.md` of `coding-aesthetics`, with the
Swift mechanisms in [state-and-concurrency.md](state-and-concurrency.md).

## Choose the Entry Point by What the Caller Holds

| What it is | Shape |
| --- | --- |
| A control or piece of UI with its own appearance | A public `struct X: View` |
| A configurable behavior for any view (dragging, snapping) | A public `struct XModifier: ViewModifier`, applied as `.modifier(XModifier(...))` |
| A presentation-like or one-shot behavior | A `View` extension over a private modifier, shaped like the nearest SwiftUI API (`.drawer(isPresented:onDismiss:content:)` beside `.sheet`) |
| State that lives with a view's identity | A `@propertyWrapper` conforming to `DynamicProperty`, built on `@State` |

Avoid sugar over a public modifier unless it mirrors a SwiftUI spelling, and
avoid offering a container-specific modifier on every `View` (scope it with
`extension ScrollView`).

## Avoid a Surface the Caller Does Not Use

- Store what the initializer receives as `private let`, and the caller-owned
  value as `@Binding private var value`; assign `self._value = value`.
- One initializer: the parameter that decides structure first (a mode, a
  `direction` even when typed `Axis`), then the binding, then defaulted
  options, then any required callback; one parameter per line.
- Nested option types sit at the top of the body with a `public init` and
  behavior-named presets; small helper subviews may sit at the bottom under
  `// MARK: - nested types`. Extensions hold only conformances, constrained
  members, and `View` conveniences.
- "Unbounded" or "fully rounded" is a sentinel of the parameter's own type
  (`.greatestFiniteMagnitude`), not a public enum.
- A callback the component cannot work without is an initializer closure; one
  that decides an outcome returns it (an end-of-gesture callback receives
  velocity as `inout` plus position and returns where to settle). Optional
  event callbacks attach modifier-style (`.onDragStart { }`) as chainable
  `consuming func` copies, not no-op closure parameters or a `Handler` struct.
- Hooks that replace a standard behavior (copy, read, draw) are optional
  closures in an owner-scoped `Handlers` struct whose absence means the
  standard behavior; the closure receives the component instead of capturing
  it.
- A closed set of modes is an enum; an open set, or one with an
  availability-gated payload, is a protocol with concrete structs and
  `extension Mode where Self == Concrete` static members. A parameter set that
  may gain alternatives can be a single-case enum with a named preset
  (`case spring(response:dampingFraction:)`).
- Optional configuration is a chainable copy
  (`public consuming func showsIndicators(_ value: Bool) -> Self`); a
  screen-sized component nests `Options` and `LocalizedStrings` with empty
  `public init()`s; behavior-only strategies are a struct wrapping a closure
  with static factories; imperative commands go through a reader/proxy pair
  like `ScrollViewReader`; contexts handed to content closures are small
  structs with internal initializers; environment actions follow
  `DismissAction`; custom environment values use `@Entry` with a default.

## Avoid State With Two Owners

- A value the parent may drive or animate is a `Binding` (an internal-state
  convenience is only a thin wrapper); a per-gesture snapshot is an optional
  `@GestureState` set on the first `.updating` call so it resets on end or
  cancellation.
- Measured size or position goes through `onGeometryChange` into private
  `@State`; `GeometryReader` only where the floor cannot use it.
- A long-lived gesture callback that must read a live flag takes
  `Binding<Bool>`, not a captured `Bool`.
- Use the lightest mechanism that provides the lifetime (plain `@State`, even
  of a small reference box, before `StateObject`); `@Observable` for models,
  owned with `@State`, `@Bindable` only when bindings are needed. Data that
  must not trigger rendering is an unobserved field of an owned object.
- Keep gesture state flat; `DispatchQueue.main.async` or a `DispatchGroup`
  joining two completions is fine, a state machine or generation counter for an
  ordinary drag is not.
- Add `@MainActor` or `nonisolated` to views, property wrappers, or models
  (demo models included) only where the compiler or a real cross-isolation use
  requires it.

## Avoid Motion That Breaks Under the Finger

1. Track relative to the start snapshot, immediately or with an interactive
   spring, rubber-banding past limits like a scroll view.
2. On release, ask the caller for the destination and animate each axis with
   its own spring seeded from velocity relative to the remaining distance,
   guarding a near-zero distance:

   ```swift
   let distance = CGSize(
     width: targetOffset.width - currentOffset.width,
     height: targetOffset.height - currentOffset.height
   )

   let mappedVelocity = CGVector(
     dx: velocity.dx / distance.width,
     dy: velocity.dy / distance.height
   )
   ```

3. Keep the presented value observable during animation (a `GeometryEffect`
   reporting `animatableData`) so a moving view is caught where it is.
4. When another gesture cancels the drag without `onEnded`, notice the
   `@GestureState` reset and settle the view, with a comment saying why.
5. Respect layout direction for edge activation; give haptic feedback on touch
   down and up or when crossing a step; prefer named animation presets
   (`.bouncy`, `.smooth`, `.snappy`, `.interactiveSpring()`) and critically
   damped springs (`dampingFraction: 1`) for navigation. Literal thresholds
   stay inline.
6. Springs drive interactive and state-driven motion; cross-fade and matched
   geometry are the starting points for transitions; easing fits fixed-time
   choreography, keyboard-synchronized motion, and infinite loops. Define the
   start, update, completion, interruption, and cancellation outcomes; whether
   cancellation calls completion is the component's contract.

## Avoid Re-implementing SwiftUI

- Compose stock views (stacks, spacers, framed shapes, `ForEach`) before a
  custom `Shape`; a `Path`-only primitive is a `Shape`, and `Canvas` is for
  many drawing operations or pixel work.
- When a container almost fits, adjust its backing view through an
  introspection hook instead of rebuilding it. Drop to UIKit, AppKit, or Core
  Animation only for a missing capability (native momentum, gesture
  arbitration, layer callbacks): keep the public type SwiftUI, nest the bridge
  privately, gate per declaration with `@available`, and offer a SwiftUI
  fallback below the floor. Name the workaround with its source URL.
- A bridge translates layout, lifecycle, and events; the native component owns
  its mechanics. Classify creation-only configuration, live inputs, rebound
  callbacks, and stable session identity; keep options in a nested
  `Configuration` with defaults (keeping the caller's drawing and interaction
  choices) and apply anything changeable, callbacks included, in
  `updateUIView`, not only at creation. Give semantically different settings
  distinct names, check the update contract where a setter echoes into
  observed state (deferring to a later turn is not a fix by itself), preserve
  restoration order on teardown, and keep same-module bridges `internal`,
  removing `public` from related members too.
- Fit media with `aspectRatio(_:contentMode: .fit)` beside intrinsically sized
  controls instead of subtracting guessed heights; fixed sizes belong to the
  component that owns them.
- A row or card that owns its surface keeps background, corners, and border
  out of its content; controls pinned to a scroll edge use `safeAreaInset`; a
  HUD that must escape clipping is declared at the source and presented by a
  root target that accepts generic `@ViewBuilder` content (any `AnyView`
  erasure stays inside the bridge), keeps the feature's progress, message, and
  cancel action instead of a Boolean, and defines a single-overlay contract.
- New apps use SwiftUI and SwiftData (no parallel SQLite authority). On macOS
  start from `NavigationSplitView` and `HSplitView`/`VSplitView`, write
  one-use layout containers in `body`, and bridge only the `NSWindow` setting a
  `Settings` scene cannot reach, verified in a real window.
- A small view that already takes cheap inputs stays together. When services
  make a screen hard to preview, keep the screen as the host (reading its live
  model in `body`) and nest a `ContentView` that takes final display values,
  bindings, and actions and constructs no services; do not add a view model
  just for the split or turn every input into a primitive. Each concrete view
  keeps its own `#Preview` in its file.

## Body

- Write gesture handling inline in the chain: start state and begin feedback
  in `.updating`, the value in `.onChanged`, the finish in `.onEnded`.
- Build `body` from private computed properties (`private var dragGesture:
  some Gesture`), keep each modifier chain together with one modifier per
  line, and separate sibling views with blank lines.
- Branch views with `if` or `switch`; a simple ternary is fine for a modifier
  argument or small value, `if`/`switch` once it stops being trivial.
- Name coordinate spaces with a private `enum _CoordinateSpaceTag: Hashable`;
  use `Button`, `ControlGroup`, or accessible controls for actions, gestures
  for direct manipulation; UI action closures are `@MainActor @Sendable (...) -> Void`.
- Keep I/O and image decoding out of `body`; load in `.task(id:)` and publish
  results through state.

---
name: ios-coding-aesthetics
description: Apply coding style guidelines to Swift, SwiftUI, UIKit, and AppKit code, including new Swift packages, reusable components and modifiers, state and concurrency utilities, and their manifests, READMEs, previews, and tests. Builds on coding-aesthetics, which holds the language-neutral principles (apply both); adds their Swift and Apple-platform form, touch interaction and motion, package layout, Swift formatting and semantic whitespace grouping, and Apple build specifics; incorporate Swift coding-style feedback when asked.
metadata:
    github-path: plugins/fluid-skill/skills/ios-coding-aesthetics
    github-ref: refs/heads/main
    github-repo: https://github.com/FluidGroup/fluid-skill
---
# Swift and Apple Platforms

This skill adds Swift and Apple-platform specifics to `coding-aesthetics`,
which states the general principles, the reasons behind them, and the
language-neutral references; apply both. Each item below is the Swift form of
the general principle with the same name.

For screen composition, visual direction, native navigation, layout exploration
and design evidence, also apply `ui-design`. This skill keeps ownership of
Swift API shape, state, concurrency, formatting and build conventions; the
design process does not replace them.

Before building an app feature or component from scratch, check
`fluid-libraries` for an existing FluidGroup or VergeGroup package.

## The Principles in Swift

1. **Structure Before Need**: no `where` constraints, conformances or
   attributes (`Equatable`, `Sendable`, `Codable`,
   `CustomDebugStringConvertible`, `@frozen`), or hand-written overrides of
   default requirements that no current use requires. Besides the general
   reasons, a protocol earns its place for a variant whose payload is gated by
   `@available`, which an enum cannot express.
2. **A Wider Surface Than the Caller Needs**: a view keeps what its initializer
   receives in `private let` (its surface is the initializer, `body`, and
   modifiers); classes are `public final` unless designed as a base, and never
   `open` without that design; supporting types nest as `Owner.Option`; no
   `public extension`; `private` by default, `@_spi(Internal)` or `package` for
   cross-module internals.
3. **Re-inventing the Platform**: name an API after what it wraps or stands in
   for (`task(priority:operation:)`, `.sheet(isPresented:)`-like
   presentations); use the native API once the floor allows
   (`onGeometryChange`, `@Entry`, `#Preview`, named animation presets);
   hand-tune a spring only where no named preset fits; adjust the backing view
   when a container almost fits; use UIKit or Core Animation only for a missing
   capability, behind a SwiftUI surface, never for what SwiftUI can do.
4. **Two Authorities for One Fact**: caller-driven values arrive as `Binding`;
   per-gesture snapshots live in an optional `@GestureState`; nothing writes
   back on every gesture tick.
5. **Work That Changes Nothing**: `Equatable` de-duplication, old/new snapshots
   (`ifChanged`), no I/O or decoding in `body`, and a measurement before
   `@inlinable`.
6. **Concurrency by Annotation**: no `@MainActor`, `nonisolated`, or
   `@unchecked Sendable` added to silence the compiler. Screen work uses the
   project's task owner or a structured lifetime (`.task(id:)`, a stored
   `Task`); an `actor` orchestrates async work that needs an orchestrator
   (callers `await` to enqueue); `@MainActor` covers main-thread utilities; a
   lock is `OSAllocatedUnfairLock` around one `private struct State`, only for
   synchronous shared state.
7. **Motion That Breaks Under the Finger**: the start snapshot is an optional
   `@GestureState` set on the first `.updating` call, so it resets on end or
   cancellation; release velocity seeds per-axis springs (in UIKit,
   `UIViewPropertyAnimator` with velocity divided by the remaining distance).
   The recipes are in [swiftui.md](references/swiftui.md) and
   [uikit.md](references/uikit.md).
8. **Words That Repeat the Code**: the role summary is `///`, or `/** */` when
   it holds a short sample; no `- Parameters:` boilerplate.
9. **Visual Noise**: two spaces; blank lines just inside type and extension
   braces and between meaningful groups, never everywhere or nowhere;
   multi-line `guard`s and function bodies; a ternary only in simple SwiftUI
   view expressions; trailing closures, not the labeled forms code completion
   leaves; `.init(...)` where the type is inferable; `self.x = x` in
   initializers; one parameter per line when a signature wraps; one modifier
   per line; no `MARK` ceremony in small files.

## Concrete Defaults

Read only what the task touches, together with the matching
`coding-aesthetics` reference where one is named.

| Task | Reference |
| --- | --- |
| A package or module: names, manifest, files, previews, tests, README | [packages.md](references/packages.md) |
| A SwiftUI view, modifier, gesture, property wrapper, or app screen | [swiftui.md](references/swiftui.md) |
| A UIKit view, controller, gesture behavior, or transition | [uikit.md](references/uikit.md) |
| Swift names, types, protocols, ownership modifiers, macros, logging, doc syntax | [swift-api.md](references/swift-api.md), with `design.md` |
| Swift state, observation, tasks, isolation, locks, state containers | [state-and-concurrency.md](references/state-and-concurrency.md), with the general `state-and-concurrency.md` |
| Swift whitespace, wrapping, and small syntax choices | [formatting.md](references/formatting.md) |
| Apple build inputs, compiler gates, Xcode sessions, test setup | [build-and-verification.md](references/build-and-verification.md), with `verification.md` |

Capturing feedback or revising this skill follows `maintenance.md` in
`coding-aesthetics`.

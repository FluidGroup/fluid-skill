# Swift State and Concurrency

Read for Swift and SwiftUI state, observation, tasks, isolation, locks, and
state-container libraries, together with `state-and-concurrency.md` in
`coding-aesthetics`, which holds the language-neutral rules and contracts.

## Avoid Choosing a Container Before the Lifetime

- The noncopyable form is `~Copyable`, where the toolchain and storage allow
  (registrations, input sessions); it does not prove `Sendable`.
- A host passes a value document as a `Binding`.

## Avoid Broken Observation

- Use `@Observable` for models on OSes that have it, aligned with the view's
  actor; no new `ObservableObject` without an older-OS requirement. A view that
  owns a model holds it in `@State`; others take a plain reference; use
  `@Bindable` only for bindings. AppKit and UIKit presentation observes the
  same models with an owned, cancellable observation task.
- No file checks, reads, or image decoding in `body`; load in `.task(id:)` and
  publish results. Per-item decoding that outlives lazy cells runs on a
  dedicated actor.
- Reusable monitoring with the view's lifetime is a modifier writing to the
  caller's `@State` through a `Binding` (`.monitorOnlineStatus($isOnline)`).
- A property wrapper may fill a small cache lazily on first read, since
  SwiftUI serializes that creation.

## Avoid Unplanned Overlap

- A screen's structured lifetime is `.task(id:)` or a stored `Task`;
  operation-local cleanup uses `defer`.
- An async orchestrator (in a library that provides one) is an `actor` whose
  methods callers `await` to enqueue, and each submission returns a `Task`;
  the shared submission shape is a defaulted debug `label`, routing arguments,
  `priority`, a generic result, and a `@discardableResult` `Task`.
- Prefer a documented async API to a `__` backing declaration, and use
  `@concurrent` when background execution is required.

## Avoid Synchronization That Misses the Invariant

- Main-thread-only code is `@MainActor` with no lock. Shared synchronous state
  is a `final class` (`@unchecked Sendable` is acceptable there) holding one
  `private struct State` in `OSAllocatedUnfairLock` accessed through
  `withLock`, or
  `NSRecursiveLock` when reentrancy is part of the contract; keep
  `OSAllocatedUnfairLock` rather than raising an iOS 17 floor for `Mutex`.
  Name any other escape hatch for what it is (`UnsafeSendableBox`), and
  document who guards non-`Sendable` values that escape a lock.
- The caller's isolation is inherited through an
  `isolation: isolated (any Actor)? = #isolation` parameter,
  `@_inheritActorContext` on escaping operations, and `sending` across
  boundaries.
- A cross-platform lock owns state and primitive in one stable allocation
  that copied handles share (never copy-on-write), keeps synchronous and
  manual lock, unlock, and try-lock contracts, and is validated as described
  in [build-and-verification.md](build-and-verification.md).

## State-Container Shapes

- The single mutation entry point is
  `commit { (inout State) throws -> Result } rethrows`.
- UIKit subscribers compare snapshots with `state.ifChanged(\.name) { … }`; an
  unused event channel is typed `Never`.
- Derived values use static pipeline members (`.select(\.count)`) with
  `Equatable` overloads that drop unchanged output.
- Subscriptions are `sink…` methods returning cancel-on-deinit handles,
  delivering on the main actor by default with an explicit background
  overload.

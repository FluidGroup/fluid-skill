# State, Data, and Concurrency

Read when the app needs state that outlives a view, shared entities,
persistence with sync, or orchestration of async work. Repositories are under
`https://github.com/VergeGroup/` unless a row says FluidGroup.

A state library is an architecture choice that spreads through the app. View
state stays in `@State`, and a screen model can be a plain `@Observable`
class; follow the project's established container before proposing a new one.

## State Containers

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| State held outside views with derived values that recompute only when their inputs change, observed from SwiftUI and UIKit | `swift-state-graph` | `StateGraph`: `@GraphStored`, `@GraphComputed`, `withGraphTracking` | iOS 17 | The current recommendation for new code. Compatible with `@Observable` observation, so views read properties directly |
| A value persisted in `UserDefaults` that participates in the same dependency tracking | `swift-state-graph` | `StateGraph`: `@GraphUserDefault("key")` | iOS 17 | Prefer over a hand-written `UserDefaults` wrapper plus manual notification |
| Entities stored once and referenced by identifier across screens | `swift-state-graph` | `StateGraphNormalization` | iOS 17 | For apps on Verge, the `Normalization` package |
| An existing app built on a unidirectional store | `swift-verge` | `Verge`: `Store`, `@Tracking` state, `StoreReader`, `@Reading` | iOS 16 | Stabilizing; its README directs new work to `swift-state-graph`. Keep using it where it is established, do not introduce it into a new app |
| A struct whose property reads and writes are tracked, with copy-on-write storage | `swift-macro-state-struct` | `StateStruct`: `@Tracking` | iOS 16 | The mechanism under Verge; rarely needed directly |

Do not mix two containers for the same state, and do not migrate a working
Verge app to StateGraph as a side effect of another task.

## Identity and Stored Values

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| Identifiers that cannot be confused between entity types | `swift-typed-identifier` | `TypedIdentifier`: `TypedIdentifiable`, `TypedID` | iOS 13 | Prefer over passing raw `String` or `UUID` identifiers between layers |
| An immutable snapshot of selected `UserDefaults` keys to embed in state | `UserDefaultsSnapshot` | `UserDefaultsSnapshotLib`: `UserDefaultsObject`, `@Property`, `@OptionalProperty` | iOS 13 | With StateGraph, `@GraphUserDefault` is simpler |

## Persistence and Sync

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| The app's own SwiftData models synchronized with CloudKit private and shared databases, where saves and their CloudKit changes are queued in one transaction and local storage works offline | `swift-cloud-kit-stack` | `CloudKitData` (model macros such as `@CloudSynced`, schema), `CloudKitDataStack` (stores and transport) | iOS 17, macOS 14 | Untagged, pre-1.0; pin a revision as its `Documentation/Integration.md` describes. SwiftData's built-in CloudKit option is enough for a private database with automatic sync and no sharing |

## Async Work

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| User-triggered async work grouped by key, where a new request either cancels the running one or queues behind it (search-as-you-type, a save button tapped twice) | `swift-concurrency-task-manager` | `ConcurrencyTaskManager`: `TaskManager`, `task(key:mode:)` with `.dropCurrent` or `.waitInCurrent` | iOS 16 | `.task(id:)` is enough when the work belongs to one view's lifetime |
| A hard time limit on an awaited operation that continues even if the operation ignores cancellation | `swift-async-timeout` (FluidGroup) | `swift-async-timeout`: `withTimeout(_:)` | iOS 13 | |
| User-initiated work that should keep running after the app enters the background | `swift-continued-background-task` (FluidGroup) | `ContinuedTaskManager`: `ContinuedTaskManager`, `submit(title:subtitle:)`, `Job` | iOS 17, macOS 14 | Wraps `BGContinuedProcessingTask` on iOS 26 and runs as an ordinary task elsewhere or when the system rejects the request, so call sites need no availability branch but continuation is not guaranteed; the work must tolerate suspension. Follow its README for the Info.plist identifiers |

Confirm the mode names against the package before writing a call; the policy
for overlapping work is the decision that matters, and it should be visible at
the call site.

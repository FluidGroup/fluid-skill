# State and Concurrency

Read for state, observation, lifetime, overlapping work, captures,
synchronization, and state-container libraries in any language. The items
marked as contracts protect behavior and are not traded for taste. A domain
skill adds the platform's mechanisms; for Swift, read
`state-and-concurrency.md` in `ios-coding-aesthetics` as well.

## Avoid Choosing a Container Before the Lifetime

Ask what must survive a render, row reuse, dismissal, or relaunch:

| Requirement | Owner |
| --- | --- |
| Results matter only while the screen is visible | The screen owns the query and task and stops with it |
| A submission must finish after dismissal | A longer-lived workflow owns it, its identity, and where completion is reported |
| It must survive process termination | A persistence and recovery contract; an in-memory task is not enough |

- A screen can own its state and view-lifetime work; an async call or retry
  alone does not justify a view model. Keep the established architecture
  unless the change needs a new boundary.
- Source, subscription, and projection have separate lifetimes; keeping a
  projection alive need not retain its source.
- Work that owns resources for one run is an instance that holds its ID,
  streams, stop signal, and destination; callers start, stop, and await it.
  Do not thread one run's state through a chain of static stages; pure
  transformations and factories stay static, and a parameter-only `Context`
  is not an owner.
- Group fields that share an owner, lifetime, or invariant under a small
  domain name (`cropSurface.scrollView`) instead of flattening them; for
  single-owner state whose copies would be meaningless, consider a
  noncopyable type first where the language and storage allow one, and a
  reference type when identity, sharing, or callbacks call for it. Neither
  choice replaces a lifetime design.

## Avoid Two Authorities for One Value

- Keep one authority for mutable state; prefer cheap computed values
  (`canSubmit`) to writable copies, and final display values to chains of
  field-copying models.
- A persistent, undoable document keeps semantic data and identity in
  serializable values, live resources with runtime owners, earlier values
  independent of later edits, and multi-step edits transactional.
- The host owns a value document and passes it as a binding; the component
  writes back once per completed operation, never per gesture tick or during a
  view update, compares by value, and drops equal writes. "Off" is a `nil`
  member or an omitted step; declaration order is evaluation order. A library
  owns no storage format and offers validating initializers instead.
- A text surface with continuous selection across content kinds shares one
  editing authority between the native editor and the document, translates
  ranges at that bridge, keeps selection and native Undo, rebuilds edits from
  semantic metadata, never rewrites the document for a presentation change,
  and defers updates during marked-text composition.
- Contract: observing work does not own it. Read a snapshot, then subscribe
  without a gap, reject events from replaced subscriptions, and separate
  latest-only display from lossless events. Leaving a screen ends its
  observation, not the work; a source without notifications may still need
  polling.

## Avoid Broken Observation

- Contract: read live model state where the UI framework tracks the read (the
  render function or a tracked wrapper); a setup-time snapshot cannot replace
  it, and an early return must still read the dependency that should trigger
  the next update.
- Imperative presentation observes the same models with an owned, cancellable
  observation; values that must survive view recreation belong to the owner
  with that lifetime.
- Fixed snapshots are deliberate (pure display, share, export, preview); an
  operation that outlives row reuse takes only its own value, such as a stable
  deletion ID. External changes that do not mutate the model need an explicit
  invalidation signal.
- Name the sources, cache lifetime, and invalidation of an expensive
  projection, and suppress work there, never updates that change observable
  behavior. Per-item state that must survive lazy-cell recreation moves to the
  screen, keyed by stable identity and invalidated on source revision (an
  identity match alone is not freshness), owning started work across
  scrolling, with decoding isolated to a dedicated background owner and
  bounded image retention; keep it local when recreation is cheap.
- Initialize lock-protected or frequently read owner state eagerly when
  laziness would add a lock or a branch to those reads. One-time creation that
  the UI framework or the owner already serializes may stay lazy.

## Avoid Unplanned Overlap

| Required behavior | Policy |
| --- | --- |
| Only the newest result matters | Cancel the earlier request; reject its stale result and cleanup |
| A second tap must not duplicate work | Admit one operation and ignore overlap |
| Later callers want the same in-flight result | Share it deliberately, including cancellation |
| Every accepted action must run | Keep each one; serialize when order matters |

- Use the project's task owner or a structured lifetime; a scheduler
  dependency is not required.
- Contract: cancellation is cooperative. Check operation identity or
  cancellation before committing a result, inside the owner's isolation, and
  recheck assumptions after each suspension.
- Clean up operation-local resources on every exit path; guard shared-state
  cleanup so an old operation cannot clear a newer one's state. State which
  outcomes call completion.
- An async orchestrator in a library that provides one is isolated, and its
  callers await to enqueue; when work is grouped (key, lane, queue), give an
  explicit policy enum with a one-line doc per case; return a handle for each
  submission, give sibling schedulers one submission shape, and never leak a
  continuation. A store cancels its tasks when it ends; a standalone scheduler
  may let in-flight work finish.
- Bound shared hardware work explicitly; priority is not backpressure.

## Avoid Incidental Retention

- Capture the dependency an operation needs, not the whole owner. A stored
  observer may need a weak owner; a finite operation may hold its dependency
  strongly. Weak capture never replaces stopping work, and a fallback object
  in a capture list silently changes identity.
- Create a weak handle before scheduling when the scheduled closure must not
  extend the owner, and check whether promoting it holds the owner across an
  indefinite await.
- Deinit cancellation only works if the owner can deinitialize; a task that
  retains its owner needs a separate stop event.
- Stored UI handlers capture their owner weakly when it owns the component,
  receive the component as an argument, and are replaced on removal.

## Avoid Synchronization That Misses the Invariant

- Fields forming one invariant change under one boundary. Isolated feature
  state stays in its isolation; a synchronous low-level API keeps its lock and
  protects the whole invariant.
- Main-thread-only code is confined to the main thread with no lock. Shared
  synchronous state keeps one private state value behind one lock, or a
  recursive lock when reentrancy is part of the contract. Name any other
  escape hatch for what it is, and document who guards unsafe values that
  escape a lock.
- Contract: compute the transition under the lock, then unlock before external
  callbacks, cancellation, or releases that can reenter; never suspend while
  holding a lock; avoid new framework lock-order dependencies; keep ordering
  that registration-before-read requires (an eager helper allows
  `register outside → read under`; a lazy one needs
  `initialize under → register outside → read under`).
- Inherit the caller's isolation instead of hopping.

## State-Container Shapes

- State is a value inside a reference owner: synchronous reads, and one
  mutation entry point that emits nothing when nothing changed.
- Subscribers receive old/new snapshots so the UI updates only what changed;
  volatile events travel on a separate channel.
- Derived values are memoized and chosen through static pipeline members,
  dropping unchanged output where it can be compared and always emitting
  otherwise.
- Equality stays cheap: identity for reference owners, version markers before
  deep comparison.
- Subscriptions return handles that cancel when released, delivering on the
  main thread by default with an explicit background option.

# Verification

Read when changing a build boundary, platform support, verification strategy,
or a development surface, alongside the repository's own build instructions. A
domain skill adds platform specifics; for Apple platforms, read
`build-and-verification.md` in `ios-coding-aesthetics` as well.

## Avoid Build Outputs Maintained by Hand

- Declare special inputs and outputs in a build plugin or rule instead of
  regenerating and committing binaries or compiling source at runtime.
- In a generated workspace, declare package versions once in the shared
  manifest and consume them from targets; follow the repository's chosen
  build tool rather than introducing one.

## Avoid Scope Creep in Compatibility Changes

- Disabling a component on a platform changes compile-time gates and the
  dependency boundary only; the working platform's gestures, thresholds,
  animations, and callbacks stay as they are, and redesign is a separate
  proposal.

## Avoid Losing Behavior With an Implementation

- Before deleting an implementation or state machine, list the public behavior
  its tests protected and move those checks to the replacement; keep a
  regression test that fails safely rather than disabling it.
- Isolate checks that can crash or deadlock the runner in a separate process.
- Async tests use continuation-based signals; never block a cooperative
  executor with a semaphore. A deliberately blocking callback needs an
  OS-thread handoff and its own release gate; keep async signals and blocking
  gates as separate types, and treat a timeout as a failure bound, not
  progress.
- A passing unit test says nothing about release performance. A hot lock
  replacement needs a race-detector run and release measurements of single
  calls and of whole operations, separating short-lived allocation wins from
  allocations real owners retain; add optimization attributes only where
  measurements show the need.

## Avoid Surprises in Development Surfaces

- When opening local web UI, use the host's inline browser (suppressing a
  CLI's own launch), falling back to an external browser only when asked or
  needed, and never open the same page twice.
- Share environment values according to the repository's visibility and the
  team's mechanism; one publishable token does not make neighboring values
  safe to commit; never copy secrets or publish anything on the strength of
  another repository's history.

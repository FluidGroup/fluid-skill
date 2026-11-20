# Apple Build and Verification

Read when changing an Apple build boundary, platform support, runtime adapter,
or test setup, together with `verification.md` in `coding-aesthetics`, which
holds the language-neutral rules, and the repository's own build instructions.

## Avoid Build Outputs Maintained by Hand

- Compile Metal through the build system (a resource bundle loads its library
  with `makeDefaultLibrary(bundle:)`) instead of regenerating and committing
  binaries or compiling source at runtime.
- Enable library evolution only for a binary distributed independently
  (an XCFramework, a binary cache, an internal SDK); keep
  `BUILD_LIBRARY_FOR_DISTRIBUTION` off for first-party modules built from the
  same checkout.

## Avoid Scope Creep in Compatibility Changes

- Where the minimum compiler and SwiftSyntax support it (Swift 6.3 or later),
  use `ModuleName::Declaration` for a lookup that must bind to a module, as in
  generated macro code that client declarations could shadow; never raise an
  existing package's compiler requirement for it.

## Avoid Taking Over the User's Xcode Session

- Build and test with `xcodebuild`, using a task-specific `-derivedDataPath`
  when the user may be building concurrently; leave the user's scheme,
  destination, windows, and build database alone. Automate the Xcode UI only
  when asked or when `xcodebuild` cannot expose the state, explaining first;
  the host's tool requirements win.

## Avoid Losing Behavior With an Implementation

- Isolate checks that can crash or deadlock the runner with Swift Testing exit
  tests where available.
- For a hot lock replacement, the race detector is Thread Sanitizer; measure
  same-module and cross-library calls, reject runs distorted by actor executor
  checks, and add `@inlinable` only where measurements show the need.

## Avoid Exposing Private Runtime Dependencies

- Where a component already depends on private runtime identifiers (class
  names, selectors, keys, key paths), keep them encoded with the
  Unicode-scalar-shift approach, decode inside the runtime boundary once and
  share the result, keep the helper private and non-inlined, and never repeat
  the plain identifiers in comments, diagnostics, or tests; check the Release
  artifact too. Document that the dependency exists and what it assumes;
  encoding does not make a private API supported. Public API names and
  app-defined identifiers are outside this rule.

# Swift API Shape

Read for Swift names, types, protocols, access control, ownership modifiers,
macros, logging, and documentation syntax, together with `design.md` in
`coding-aesthetics`, which holds the language-neutral rules. Formatting is in
[formatting.md](formatting.md).

## Avoid Names and Members That Mislead

- A deliberate `lazy var` for one-time construction is the Swift form of that
  exception; it never hides I/O or consumption behind a getter.
- Avoid an enum case named `none` where `Optional.none` could be confused;
  use a domain word (`unselected`, `empty`).
- App-wide platform adapters and SwiftUI extensions use an `app` prefix
  (`appInlineNavigationTitle()`); domain APIs keep domain names.
- Readable diagnostic identity covers key paths shown by `_printChanges()`.

## Avoid Ambiguous Types

- Typed identifiers keep raw `UUID` persistence fields and expose a computed
  `typedID`.
- A container that cannot inspect opaque content's IDs takes
  `Binding<ScrollPosition>` and lets the caller choose
  `ScrollPosition(idType:)`.
- Same-shaped presets are `struct` constants; choose `struct` or `class` by
  requirement, not by ranking.
- `@unknown default` is for non-frozen SDK or resilient-module enums; never add
  it to an app-owned enum to avoid a decision.
- Provide an inherited protocol requirement as a default in a plain protocol
  extension, not pinned with a `where` clause, so conformers can still supply
  their own; refer to associated types through the generic parameter
  (`Base.Index`) and let inference supply them instead of public forwarding
  typealiases.

## Avoid Abstractions Without a Stable Responsibility

- When a large owner's file is split, its nested types stay defined in an
  `extension Owner`.
- Initialization-only grouping is a `do` block or local closure; a `do` block
  scopes; it does not run once.
- Add an optional framework conformance additively behind
  `#if canImport(Combine)` instead of changing public types.

## Avoid Unshaped Infrastructure APIs

- An open family of behaviors: a protocol (often with a primary associated
  type), concrete generic structs in a caseless `enum` namespace, static
  factories through `where Self == Concrete`, and an `Any…` closure-backed
  conformer when erasure is needed.
- Use `consuming`, `borrowing`, `~Copyable`, and complementary mutating/consuming operations
  (`sort()`/`sorted()`) where ownership is meaningful, such as a wrapper taking
  its stored payload (`init(_ raw: consuming Raw)`); leave closures and
  ordinary parameters unannotated. Capture `#file`/`#line` defaults
  when a call site's identity aids debugging. Scoped operations are `withX { }`
  free functions; raw C callback registration hides in a private caseless enum
  returning a token.
- Macros: one `public struct XMacro` with a nested `enum Error`, one extension
  per role, syntax built by string interpolation, user mistakes reported as
  diagnostics on the node, `fatalError` only for impossible input; test with
  `assertMacro` and keep `#if DEBUG` samples in the library target.
- Logging, when present, is an `enum Log` of `os.Logger` categories disabled
  in release; signposts are DEBUG-only behind an environment flag; an opt-in
  sanitizer reports misuse through a callback.

## Avoid Documentation That Restates

- The primary type's role summary is `///`, or `/** */` holding a short
  sample. An `@Entry` value documents its meaning and ownership, and a stored
  type-erased token is typically an `ObjectIdentifier`. DocC symbol links
  (``SwiftUI/View/offset``) are welcome where they help.

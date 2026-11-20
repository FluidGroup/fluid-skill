# Design

Read for names, types, abstractions, dependencies, errors, and documentation in
any language. A domain skill adds the language's concrete forms; for Swift,
read `swift-api.md` in `ios-coding-aesthetics` as well.

## Avoid Names and Members That Mislead

- Booleans read as state: `is`, `has`, `can`, `should`.
- Properties are cheap, side-effect-free reads; actions, mutations, async or
  throwing work, and parameterized operations are functions. A getter never
  consumes or mutates observable state (`consumeNextItem()`, not a mutating
  read); a deliberate lazily initialized property for one-time construction is
  the exception and never hides I/O or consumption.
- Fresh construction is an operation (`makeDefault()`), not a property that
  implies a stable instance.
- Make diagnostic identity readable: an identifier that appears in logs or
  debugging output should show stable type and property meaning, not an object
  address.

## Avoid Ambiguous Types

- Express consequential units and coordinate spaces through types and argument
  labels; document what the declaration cannot show.
- Distinguish same-shaped IDs from different domains with model-scoped typed
  identifiers in app APIs; keep raw persistence fields, expose a computed typed
  ID, and unwrap only at predicates, serialization, and other storage or
  transport boundaries. Display values inherit the model's ID.
- Distinguish value equality from occurrence identity; object addresses never
  replace durable IDs.
- Derive a payload from its owning generic parameter (`Loader.Payload`) rather
  than a second parameter, and keep one authority per axis or option (a mode
  does not repeat an axis another parameter owns).
- When a mode changes how stored values are interpreted, make it part of
  equality, cache identity, and persistence; existing documents keep their
  meaning, and only implemented choices are exposed.
- Choose by requirement, not by a value-versus-reference ranking: same-shaped
  presets are value constants; alternatives with different payloads or
  behavior are an enum with exhaustive handling; an immutable recipe with
  temporary execution resources is a value plus an execution owner.
- Put type safety where the boundary can enforce it: a container that cannot
  inspect opaque content's identifiers lets the caller choose their type.
- Handle app-owned enums exhaustively, without a catch-all that hides a newly
  added case. When unknown persisted values are possible, represent them with
  a domain case at the decoding boundary.
- Declare an engine's supported setting choices and default once, as typed
  capabilities that both UI candidates and runtime checks use; keep static
  support distinct from present availability.
- Require only the constraints a boundary needs. Erase types only at a
  deliberate boundary, binding creation and recovery to one contract.

## Avoid Abstractions Without a Stable Responsibility

- Begin with a concrete dependency; introduce an interface for real
  substitution, a useful test double, external conformance, or a stable
  extension point, including a concrete upcoming need. Injection does not
  require an interface per parameter, and a platform type that already offers
  the operation needs no broader interface.
- For known variants, use the smallest mechanism that represents the
  difference: constrained members or initializer overloads for a generic
  parameter's concrete type, an enum for differing payloads, overloads or
  factories for construction paths, an interface for an intentionally open
  contract.
- Inject services, navigation, storage, and environment explicitly; features
  depend on lower layers, never the reverse; session-sensitive dependencies
  have one origin, not a fallback constructed in a capture.
- Nest supporting types under their single owner (`Player.Configuration`,
  never `Player.PlayerConfiguration`); do not nest a type with an independent
  lifetime.
- Similar code is not reason to share: keep components with different reasons
  to change separate, extract a concept whose change should affect every use,
  and reconsider an abstraction that collects flags and exceptions. External
  sync with its own lifetime composes an in-memory primitive from an owner
  instead of hooking inside it.
- Keep the member surface small and add no member only to shorten one caller:
  initialization-only grouping is a scoped block or local closure, a repeated
  local transformation is a local function, a named action or endpoint is a
  method even with one caller, a retained helper with no instance dependency
  is static, and a one-use calculation stays local. Keep a setter's
  initialization and update paths readable inside it rather than in a
  `Bool`-returning helper.
- Analytics definitions are values (event name and typed attributes) built by
  named factories; sending stays separate.
- Remove a dead compatibility layer, but keep an API consumers still use; keep
  accepted debt local with its reason and repayment, not a bare TODO.

## Avoid Errors and Checks That Hide Contracts

- Typed error enums translate low-level failures into domain cases, keeping an
  underlying error when it helps diagnosis; a wrapper that translates nothing
  does not earn its place.
- Validate external input; never paper over an impossible internal state with
  a silent fallback. Assertions expose real lifecycle or threading violations;
  decorative validation does not fix it.
- Do not re-validate in presentation a format the database already guarantees;
  handle states the display can actually see, such as a missing value.

## Avoid Documentation That Restates

- A primary type gets one or two sentences of role; add only what the
  declaration cannot show: ownership, lifetime, units, coordinate space,
  isolation, callback outcomes, the origin of erased identity. Internal types
  with such contracts get the same; expect about one doc line per ten lines of
  code.
- Document a method when its operating contract helps (framework overrides,
  delegates, input and async boundaries): who calls it and when, required
  state, side effects. Distinguish a framework guarantee from this
  implementation's choice.
- A stored type-erased token documents its source type, where it is created,
  and who keeps the original alive.
- Implementation comments explain a workaround, a required ordering, or
  accepted debt; a `SAFETY` comment names the actual invariant.

# UIKit

Read when building a UIKit view, view controller, gesture behavior, or
transition. The interaction recipe is shared with [swiftui.md](swiftui.md).

## Avoid Construction Paths Nobody Should Use

- Build views and controllers in code: a designated initializer with defaulted
  optional collaborators, and the coder initializer fenced:

  ```swift
  @available(*, unavailable)
  public required init?(coder: NSCoder) {
    fatalError("init(coder:) has not been implemented")
  }
  ```

- Mark inherited API that would break the component's invariants
  `@available(*, unavailable)` instead of documenting "do not call".
- Classes are `public final` unless designed as a base (`open class …Base`);
  non-public classes are always `final`. A thin public type may wrap a private
  implementation view.

## Avoid Scattered State and Delegate Sprawl

- Nest `Configuration` (public `var`s with defaults), contexts, and
  identifiers under the owner; large nested types may live in a bottom
  `extension Owner {}` under `// MARK: - Nested types`.
- Keep mutable view state in a `private struct State: Equatable` applied from
  `didSet` only when it changed (`guard state != oldValue else { … }` written
  over multiple lines).
- Report events through a `Handlers` struct of closures with no-op defaults
  instead of a delegate protocol; hide a required Objective-C delegate in a
  private proxy or behind `@_spi(Internal)`.
- Attach a behavior to an existing view through an extension method backed by
  a small coordinator, returning a token or coordinator that cleans up when
  released. Prefix every extension member on a UIKit type with the module's
  short name; give a type the module prefix only when it replaces a UIKit
  counterpart.

## Avoid Behavior Hierarchies

- An open-ended behavior such as a transition is a struct wrapping a
  `@MainActor` closure with a `name` defaulting to `"\(#file),\(#line)"`, and
  presets as `static var` or `static func` in extensions grouped by family
  (`AnyPresentation+fade.swift`). A renamed preset keeps a deprecated alias.
- An async UI operation receives a `@MainActor final class …Context` that owns
  its participants, exposes an idempotent `notifyCompleted()`, can be
  invalidated when interrupted, and reports a completion event enum. Offer the
  completion-handler API first and a `@discardableResult … async` overload on
  top.

## Avoid Motion That Cannot Be Caught

- Use `UIViewPropertyAnimator`, typically critically damped
  (`dampingRatio: 1`, 0.4–0.6 s), and
  `UISpringTimingParameters(mass:stiffness:damping:initialVelocity:)` for a
  fling, with velocity divided by the remaining distance and guarded against
  zero, NaN, and infinity.
- Start interactions from `layer.presentation()`, scrub `fractionComplete`
  while tracking, and finish with `continueAnimation` or a reversed animator.
- Rubber banding is one shared pure function.

## Avoid Indirection in Layout and Long Methods

- Plain anchors in `NSLayoutConstraint.activate([...])`, one per line, or frame
  plus autoresizing mask for full-bleed children; KVO and closures instead of a
  reactive framework for internal wiring.
- Build debuggability in: creation-site accessibility identifiers in DEBUG,
  per-module logging off unless enabled, and `assert` on main-thread and caller
  contracts at entry points.
- Section long gesture or layout methods with labeled `do` blocks
  (`began: do {`) or local functions instead of many one-caller methods;
  `fallthrough` from `.began` into `.changed` is fine.

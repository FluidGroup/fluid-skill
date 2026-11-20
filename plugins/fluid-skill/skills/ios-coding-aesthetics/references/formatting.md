# Formatting

Read when the shape of Swift code matters: whitespace, wrapping, and small
syntax choices. These are style preferences, not claims that other syntax is
wrong; generated and tool-required files keep their format. Two-space
indentation applies to every language (`coding-aesthetics`); the rest of this
file is Swift-specific.

## Avoid Blank Lines Without Meaning

- Treat a blank line as a boundary between groups: just inside a type's or
  extension's opening and closing braces, between property groups and the
  initializer, and between methods. Only a tiny nested helper (one or two
  stored properties) may open directly into its first member.
- Inside a method, separate preconditions, value preparation, updates, and the
  result; keep statements serving one purpose together. A multi-group body,
  `var body: some View {`, and a multi-statement closure may open with a blank
  line.
- Keep a SwiftUI modifier chain together, one modifier per line; separate
  sibling views with blank lines.

```swift
/// Stores a value advanced in fixed increments.
struct Counter {

  private(set) var value: Int
  private let step: Int

  init(value: Int, step: Int) {
    self.value = value
    self.step = step
  }

  mutating func advance(times: Int) -> Int {
    guard times > 0 else {
      return value
    }

    let change = step * times
    let nextValue = value + change

    value = nextValue

    return nextValue
  }

}
```

## Avoid Packing

- Break after the opening brace of functions, getters, and control flow, even
  for one statement; never a one-line `guard` or function body. A short
  predicate or transform closure may stay compact.
- Put long signatures and calls one parameter per line with the closing `)`
  on its own line; no semicolons.

## Avoid Syntax That Adds Nothing

- Outside SwiftUI view code, use `if`/`else` or `switch` (statements or
  expressions) rather than the ternary operator; in SwiftUI view code a simple
  ternary for a modifier argument or small value is fine.
- Use trailing closures and name unused parameters `_`, not the labeled form
  code completion inserts.
- Use implicit members where the type is inferable (`.init(...)`,
  `= .init()`), `self.value = value` in initializers, `self._value = value`
  for wrapped storage, and an explicit type with an implicit-member default
  (`@State private var cache: Cache = .init()`).
- Omit `return` in single-expression bodies unless a multi-line expression
  reads better with it; write `== false` where a leading `!` is easy to miss.
- Write availability tersely per declaration (`@available(iOS 17, *)`), and
  give a type that is printed or logged its readable form through
  `CustomStringConvertible`, even for debugging.
- Inside a plain `extension Type {`, mark each public member `public` instead
  of `public extension`; declare unconditional conformances on the type and
  use extensions for conditional ones.
- Use exhaustive `switch` for enum-driven behavior, nesting switches for
  multi-axis branches instead of tuple patterns.
- Keep one-off setup literal: constants at the call site with a short comment,
  and a bare `do { }` block around a multi-statement step.
- Keep generic parameter names short and unconstrained until the
  implementation needs a constraint (`Wrapper<Value>`, not
  `Wrapper<Value: AnyObject>` just because callers will pass objects); keep
  file-local helpers `fileprivate` and near their use.

## Avoid Navigation Ceremony

- Use `// MARK:` to label protocol groups (`// MARK: Hashable`) or the
  sections of a larger type (lifecycle, public API, nested types); a small
  file needs none.

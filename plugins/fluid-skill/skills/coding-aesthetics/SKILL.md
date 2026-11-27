---
name: coding-aesthetics
description: Apply coding style guidelines in any language when writing, refactoring, reviewing, or discussing code. Use for the scope of a change, abstraction level, API surface, naming, ownership and lifetime, overlapping work and synchronization, documentation density, indentation, and verification across implementation changes; incorporate coding-style feedback when asked. For Swift and Apple platforms also apply ios-coding-aesthetics; for web UI also apply web-coding-aesthetics.
metadata:
    github-path: plugins/fluid-skill/skills/coding-aesthetics
    github-ref: refs/heads/main
    github-repo: https://github.com/FluidGroup/fluid-skill
---
# Coding Style

This style is defined by what it avoids. Each principle below names a failure,
its cost, and an alternative. When a case is not covered, ask which of these
failures a choice would cause, and take the option that causes none.

The goal behind all of them: few concepts to keep in mind, with meaning,
ownership, and lifetime visible where the code is used.

These principles hold in every language. A domain skill states their concrete
form and adds the domain's own principles: `ios-coding-aesthetics` for Swift
and Apple platforms, `web-coding-aesthetics` for web UI. Apply the matching
domain skill together with this one.

## Scope

- Current user instructions and established local patterns win over these
  defaults. Inspect nearby code and callers before deciding what to change, and
  keep edits scoped; a style preference is not permission to reformat a
  repository.
- Two-space indentation applies to all hand-authored source and tests, in any
  language, including files being changed that used four; never tabs. Other
  whitespace and syntax rules are language-specific: a domain skill states
  them, and elsewhere the language's conventions and the project's formatter
  decide. Generated files and tool-required formats keep their format.
- A style preference chooses among valid forms. A design default holds under
  stated conditions. A correctness contract protects behavior, isolation, or
  lifetime and is never traded for taste; explain a real conflict instead.
- The project's own names, paths, and product requirements never become
  general rules; examples here are synthetic.

## Question the Premise

- Treat requested patches, inherited plans, and your own earlier plans as
  hypotheses, not proof that their premises are sound. State the actual
  requirements and inspect the responsible component, its callers, and
  contracts.
- Ask what design would best serve the component if built afresh under those
  requirements. Compare it with the current plan; revisit that comparison when
  new evidence changes a premise instead of layering steps or exceptions onto
  the prior plan.
- Prefer bounded redesign only when evidence warrants it; otherwise explain why
  a local change fits. Preserve required behavior and compatibility, keep
  unrelated cleanup out, and follow an explicitly required mechanism unless it
  conflicts with correctness or a contract that needs clarification.

## What to Avoid

### 1. Structure Before Need

- **Avoid**: interfaces or protocols, generic parameters and their
  constraints, configuration types, wrapper layers, and conformances,
  attributes, or hand-written overrides of default behavior that no current
  use requires; defensive validation of values the type already constrains;
  features, modes, logging hooks, and platform branches nobody asked for;
  helper types extracted only to unit-test; several files or targets for one
  idea.
- **Because**: every concept costs each reader now, and the next real
  requirement reveals the right shape better than a guess.
- **Instead**: the smallest complete shape. One primary type with its helpers
  nested inside, plain stored properties, one initializer with defaults,
  literal constants inline, and a short `// TODO:` for a known refinement. A
  closed set is an enum; an interface earns its place through real
  substitution, a useful test double, external conformance, a stable extension
  point (including a concrete upcoming need), or a variant an enum cannot
  express.

### 2. A Wider Surface Than the Caller Needs

- **Avoid**: public stored properties on views and controllers, classes open to
  subclassing that were not designed for it, top-level types that serve a
  single owner, options for values nobody needs to change, and internals made
  public for convenience.
- **Because**: every public symbol is a promise and one more thing to learn.
- **Instead**: a UI component keeps what it receives private (its surface is
  its construction, its rendering, and its configuration methods); classes are
  closed to subclassing unless designed as a base; supporting types nest under
  their owner with presets named for behavior; private by default, with the
  language's narrowest mechanism for internals shared across modules.

### 3. Re-inventing the Platform

- **Avoid**: inventing vocabulary or mechanisms the platform already has; an
  own helper where a native API exists; rebuilding a control the platform
  almost provides; hand-rolled locks or queues; hand-tuned animation where a
  named preset fits; dropping to a lower-level framework for what the
  high-level one can do; borrowing a system API's labels for something that
  does not stand in for it.
- **Because**: platform names and behavior are already in the reader's head,
  and they improve without your effort.
- **Instead**: name an API after what it wraps or stands in for; use the native
  API once the minimum platform allows; adjust the backing view when a
  container almost fits; use a lower layer only for a missing capability,
  behind the high-level surface; port a proven technique faithfully, keeping
  its comments and its type name minus any vendor prefix, under
  `// from <project> <URL>`.

### 4. Two Authorities for One Fact

- **Avoid**: copies synchronized by hand; a component and its caller both
  owning a value; a setup-time snapshot standing in for a tracked read; writing
  back on every tick of a continuous interaction; an identifier plus an
  `isEnabled` flag; hidden fallback instances; a library owning the host's
  storage format.
- **Because**: copies drift, and the drift becomes the bug.
- **Instead**: one owner chosen by the lifetime the state needs. Caller-driven
  values arrive as a binding to the caller's state, per-interaction snapshots
  reset when the interaction ends or is cancelled, derived values are
  computed, a document is written once per completed operation with equal
  writes dropped, and "off" is an absent value.

### 5. Work That Changes Nothing

- **Avoid**: emitting or re-rendering for equal values, I/O or decoding while
  rendering, copying state to detect change, synchronization on hot reads to
  save a rare allocation, and optimization attributes without a measurement.
- **Because**: unchanged values should not trigger downstream work; unmeasured
  tuning only adds noise.
- **Instead**: equality-based de-duplication, old/new snapshots, memoized
  derived values, lifecycle tasks for I/O, eager owner state, and a measurement
  before an optimization attribute.

### 6. Concurrency by Annotation

- **Avoid**: isolation annotations, unchecked thread-safety escape hatches, or
  a lock added to silence the compiler; a lock where isolation suffices; a
  synchronous facade over async orchestration; external callbacks or
  suspension inside a lock; a continuation that can leak.
- **Because**: an annotation hides the ownership decision instead of making it.
- **Instead**: decide where the work lives. Screen work uses the project's task
  owner or a structured lifetime tied to the screen; an isolated orchestrator
  (an actor where the language has one) runs async work that needs one, and
  callers await to enqueue; main-thread utilities are confined to the main
  thread; and a lock around one private state value protects only synchronous
  shared state. Inherit the caller's isolation and state how operations may
  overlap as an explicit policy.

### 7. Motion That Breaks Under the Finger

Applies to any directly manipulated UI: touch, pointer, or trackpad.

- **Avoid**: a jump when a touch begins, an animation that cannot be grabbed,
  discarded release velocity, hard stops at limits, eased curves for
  interactive motion, controls without feedback, and gestures that strand state
  when the system cancels them.
- **Because**: these products are about fluid, physical interaction.
- **Instead**: track relative to a start snapshot, rubber-band past limits,
  hand release velocity to per-axis springs, keep the presented value
  observable so a moving view can be caught, recover on cancellation, give
  haptic feedback at meaningful moments, and use critically damped springs for
  navigation.

### 8. Words That Repeat the Code

- **Avoid**: doc comments that restate members, initializers, or private
  helpers; parameter-list boilerplate; type essays; comments that narrate code,
  previews, tests, or manifests; README installation, requirements, badges,
  feature lists, and API reference.
- **Because**: prose that restates code goes stale and buries the one note that
  matters.
- **Instead**: one or two sentences of role on the primary type; a one-line doc
  comment on a member, enum case, or callback only when it carries a contract
  the signature cannot show; a comment only for a workaround, an ordering, or a
  platform quirk (with its URL); and a README that is a title, a few
  sentences, an image, and examples.

### 9. Visual Noise

- **Avoid**: tabs or four-space indents in hand-authored source, and one
  language's whitespace rules applied mechanically to another language or to
  generated code.
- **Because**: the shape of the code should be readable before its words.
- **Instead**: two spaces in every language; within a language, the domain
  skill's formatting rules or, without one, the language's conventions and the
  project's formatter.

## Concrete Defaults

Read only what the task touches. Each reference is organized by the same
failures.

| Task | Where |
| --- | --- |
| Names, types, abstractions, errors, documentation | [design.md](references/design.md) |
| State, lifetime, observation, overlapping work, captures, synchronization, state containers | [state-and-concurrency.md](references/state-and-concurrency.md) |
| Build inputs, compatibility scope, tests across implementation changes, measurement, development surfaces | [verification.md](references/verification.md) |
| Long-term change costs, reversibility, accepted debt, deciding what to do now or defer | the `long-term-maintainability` skill |
| Capturing feedback or revising these skills | [maintenance.md](references/maintenance.md) |
| Swift, SwiftUI, UIKit, AppKit, Swift packages | the `ios-coding-aesthetics` skill |
| Web UI, CSS, loading, accessible controls, client/server authority | the `web-coding-aesthetics` skill |

## Showing the Judgment

- Implementation: express these choices in the code and mention only material
  tradeoffs or deviations.
- Design discussion: recommend one concrete shape and name the requirement that
  would change it; a small before/after beats a list of architecture labels.
- Review: report behavior and contract failures first, then design, then style;
  label a preference as a preference without inflating it or inventing a
  performance reason, and do not rewrite unless asked.
- Propose a skill change only when a task reveals a new preference,
  contradiction, or gap, and edit the skill only when the user asks.

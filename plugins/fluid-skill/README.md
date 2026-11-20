# fluid-skill

Apple UI design, coding style and long-term maintainability in one plugin:
principles that hold in any language, their Swift and Apple-platform form,
web UI specifics, native interface design and judgment about the cost of
evolving software. One install brings all six skills; each activates when
the task needs it.

## Skills

| Skill | Scope |
| --- | --- |
| `coding-aesthetics` | Any language: nine failures to avoid, each with why it costs something and what it leaves |
| `ios-coding-aesthetics` | Swift, SwiftUI, UIKit, AppKit, and Swift packages; the Swift form of each principle |
| `web-coding-aesthetics` | Web UI: components and catalogs, CSS, loading, accessible controls and client/server boundaries |
| `ui-design` | Apple UI: composition, visual direction, native navigation, constraints, exploration, prototypes and design evidence |
| `long-term-maintainability` | Design, implementation, and review: balance present complexity against the cost of changing decisions later |
| `fluid-libraries` | App features: when to adopt an existing FluidGroup or VergeGroup package instead of building from scratch |

The domain skills build on `coding-aesthetics` and tell the agent to apply it
with them. The nine failures are structure before need, a wider surface than
callers need, re-inventing the platform, two authorities for one fact, work
that changes nothing, concurrency by annotation, motion that breaks under the
finger, words that repeat the code, and visual noise.

`long-term-maintainability` adds a separate review aspect for software expected
to keep evolving. It distinguishes code that is small because it only fits
today's circumstances from equally small code whose concepts are chosen with
continued evolution in mind. It grounds that judgment in the meaning, spread,
and reversibility of assumptions, then recommends keeping, adjusting, or deferring a decision
with a concrete reason. It uses the coding skills' existing defaults without
duplicating them.

`ui-design` owns the design process for SwiftUI, UIKit and AppKit. It applies
the project's design system and platform conventions first, with a concrete
composition direction, concentric nested surfaces and honest review evidence.
For open layouts it explores a fixed column grid through structured randomization
and presents the legal placements together for human selection.
Use it alongside the coding skills, which retain API, state, concurrency,
formatting and build guidance. A small fix does not require a full exploration.

`fluid-libraries` keeps an app from re-implementing what FluidGroup and
VergeGroup already publish. When a feature is still a plan, it checks the
platform first, then the project's existing dependencies, then a catalog of
packages for sheets, lists, chat, camera, image editing, gestures, visual
effects, state, sync and async work. It states each package's floor and
caveats (private API, no tagged release) and says when a few copied lines or
hand-written code are the better answer.

## References

`coding-aesthetics` holds the language-neutral defaults:

- `references/design.md`: names, types, abstractions, errors, and
  documentation.
- `references/state-and-concurrency.md`: lifetime, authority, observation,
  overlap, retention, synchronization, and state-container shapes.
- `references/verification.md`: build inputs, compatibility scope, tests across
  implementation changes, measurement, and development surfaces.
- `references/maintenance.md`: how to evaluate feedback and revise these skills.

`ios-coding-aesthetics` holds the Swift defaults:

- `references/packages.md`: package proportion, names, manifest, previews,
  tests, and README.
- `references/swiftui.md`: entry points, surface, state, interaction, bridges,
  and app screens.
- `references/uikit.md`: construction, state, behaviors, motion, and layout.
- `references/swift-api.md`: Swift names, protocols, ownership modifiers,
  infrastructure API shape, macros, logging, and documentation syntax.
- `references/state-and-concurrency.md`: observation, tasks, actors, locks,
  isolation, and state-container shapes in Swift.
- `references/formatting.md`: Swift blank-line grouping, wrapping, and small
  syntax choices.
- `references/build-and-verification.md`: Metal, library evolution, compiler
  gates, Xcode sessions, Swift Testing, and private runtime dependencies.

`web-coding-aesthetics` is a single `SKILL.md`.

`ui-design` holds the design loop in `SKILL.md`, focused platform/framework
references, repeatable SwiftUI comparison-export guidance, the DEBUG-only
`assets/swift/DesignPlayground.swift` and `scripts/check_swift_ui.py`. The
export guidance uses the actual comparison View; macOS `ImageRenderer`
output is not iOS Simulator or runtime accessibility evidence.

`long-term-maintainability` holds the judgment procedure in `SKILL.md` and
synthetic contrasting cases in `references/contrasting-cases.md`.

`fluid-libraries` holds the decision procedure and a need-to-package table in
`SKILL.md`, with the product, entry point, floor and caveats of each package in
`references/`: `components.md`, `interaction.md`, `swiftui-utilities.md`,
`state-and-data.md`, `foundation.md` and `uikit-legacy.md`. The catalog is a
snapshot; the package's own README and manifest are the authority.

# fluid-skill

FluidGroup's seven skills cover coding, native Apple UI design, maintainability,
animated sequence visualizations and reuse of FluidGroup and VergeGroup packages.
Install the plugin or select individual skills.

| Skill | When to use it |
| --- | --- |
| [coding-aesthetics](plugins/fluid-skill/skills/coding-aesthetics/SKILL.md) | Decide API shape, state ownership, concurrency and verification in any language. |
| [ios-coding-aesthetics](plugins/fluid-skill/skills/ios-coding-aesthetics/SKILL.md) | Apply those principles to Swift packages, SwiftUI, UIKit and AppKit. |
| [web-coding-aesthetics](plugins/fluid-skill/skills/web-coding-aesthetics/SKILL.md) | Design web components, loading states and client/server boundaries. |
| [ui-design](plugins/fluid-skill/skills/ui-design/SKILL.md) | Design native Apple interfaces and compare legal layouts on a fixed grid. |
| [long-term-maintainability](plugins/fluid-skill/skills/long-term-maintainability/SKILL.md) | Review what a change makes easier or harder to maintain. |
| [sequence-visualization](plugins/fluid-skill/skills/sequence-visualization/SKILL.md) | Animate how events and state move between components, step by step, and export video. |
| [fluid-libraries](plugins/fluid-skill/skills/fluid-libraries/SKILL.md) | Use an existing FluidGroup or VergeGroup package before building a feature from scratch. |

## Install

**Claude Code** — run these in the chat:

```text
/plugin marketplace add FluidGroup/fluid-skill
/plugin install fluid-skill@fluid-skill
```

**Codex** — from a local clone:

```sh
codex plugin marketplace add "$PWD"
codex plugin add fluid-skill@fluid-skill
```

**Skills CLI** — install all seven, or omit `--skill '*'` to choose:

```sh
npx skills add FluidGroup/fluid-skill --skill '*'
```

For clients that load a [portable plugin](https://agent-plugins.org/specification)
directly, use [plugins/fluid-skill](plugins/fluid-skill) as the plugin root.
The [UI evaluation guide](evals/ui-design/README.md) describes the repository-only
fixtures and how to type-check the bundled Swift examples.

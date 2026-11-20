# UI-design evaluations and checks

These cases are repository-only development material, not installed skills or measured results.

| Case | Scope |
| --- | --- |
| [swiftui-spacing-and-radius-fix](swiftui-spacing-and-radius-fix/prompt.md) | A targeted fix, with the supplied source fixture |
| [swiftui-recordings-screen](swiftui-recordings-screen/prompt.md) | One finished native screen, not an unsolicited exploration |
| [swiftui-exploration-full-loop](swiftui-exploration-full-loop/prompt.md) | Seeded alternatives, concentric surfaces, dials and repeatable export |
| [uikit-mini-player-component](uikit-mini-player-component/prompt.md) | Native UIKit component and interaction |
| [appkit-library-window](appkit-library-window/prompt.md) | Mac window, selection, toolbar and menu commands |

Each directory has a `case.yaml`, a `prompt.md` with runner frontmatter, and weighted LLM
graders under `graders/`. Run each generation in a fresh workspace with
`plugins/fluid-skill/skills/ui-design` available; for implementation, also make
`coding-aesthetics` and `ios-coding-aesthetics` available. Run the optional `context.scaffold_script`
from the case with that workspace as the working directory. Give an independent judge the
generated files and execution trace, then apply the case's graders. Keep generated apps, traces
and scores outside the plugin. A parsed case or compiled fixture is not an evaluated generation.

## Local checks

From the repository root, with Python 3.9+ and full Xcode selected on macOS:

```sh
python3 tools/typecheck-snippets.py
```

This type-checks the bundled kit with and without DEBUG for iOS 17/macOS 14, and concatenated
Swift blocks from the framework, variations and rendering references against the matching SDKs.
The variations example uses its actual layout view. This check does not launch an app or prove
layout, rendering or gesture behaviour. `DEVELOPER_DIR` can select another installed Xcode.

The installed skill also includes a dependency-free pattern checker:

```sh
python3 plugins/fluid-skill/skills/ui-design/scripts/check_swift_ui.py path/to/Sources --scale 4,8,12,16,20,24,32,48,64
```

Exit status: 0 means no findings, 1 means findings, and 2 means no input files. `--json` emits
structured findings. A trailing `// design-check: ignore` suppresses a line. Findings require
human confirmation; the checker does not measure concentric geometry, hit targets or runtime
behaviour. For package changes also validate manifests and skill frontmatter, resolve local
Markdown links, parse cases/graders, and run `git diff --check`.

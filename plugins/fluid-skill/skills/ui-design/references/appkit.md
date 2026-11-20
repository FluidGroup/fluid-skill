# Building for the Mac: AppKit, and SwiftUI on macOS

Patterns and pitfalls for steps 2, 6 and 7 in a Mac app. A Mac app is judged first on whether it
behaves like one. Follow the project's own coding guide and design system first; this file fills
gaps. The code blocks here are type-checked against the SDK by `tools/typecheck-snippets.py`;
they were not run.

## What a Mac app owes the user

Check these before any visual work. Each one is a failure of gate item 5 if missing.

- **The menu bar holds every command,** with standard shortcuts for standard commands (New,
  Open, Save, Close, Undo, Find, Settings on Command-comma). A toolbar button or a context menu
  item is a second route, never the only one. Menu items disable themselves when they do not
  apply.
- **Windows resize.** Give each a sensible minimum size, let the content reflow, remember the
  frame between launches, and support full screen and tabs unless there is a reason not to.
- **Sidebar, content, inspector.** Top-level sections are a sidebar in a split view, not a tab
  bar. Columns collapse and resize.
- **Keyboard first.** Full keyboard navigation, a visible focus ring, Return for the default
  button, Escape to cancel, arrow keys in lists, type-to-select where it fits.
- **Pointer behaviour.** Hover states, tooltips on toolbar items, right click for a context
  menu, double click to open, drag and drop where data can move.
- **Undo** for every change to the user's data.
- **Density.** Controls and rows are smaller than on iOS. Do not carry over 44-point rows,
  large titles, bottom tab bars, full-width buttons or swipe-only actions.
- **Appearance.** Light and dark, the user's accent colour, Increase Contrast, Reduce Motion,
  Reduce Transparency, and an inactive-window state that the system controls dim on their own.

## Tokens first

```swift
import AppKit

enum Spacing {
  static let s1: CGFloat = 4
  static let s2: CGFloat = 8
  static let s3: CGFloat = 12
  static let s4: CGFloat = 16
  static let s5: CGFloat = 20
}

enum Corner {
  static let panel: CGFloat = 12
  static func inner(_ outer: CGFloat, inset: CGFloat) -> CGFloat { max(0, outer - inset) }
}

enum Motion {
  static let panelDuration: TimeInterval = 0.35
  static let panelBounce: CGFloat = 0
}
```

- **Type.** `NSFont.preferredFont(forTextStyle:)`, or `NSFont.systemFont(ofSize:
  NSFont.systemFontSize)` and the small and label sizes for control text. Mac text styles are
  smaller than their iOS namesakes; do not copy iOS point sizes.
- **Colour.** `.labelColor`, `.secondaryLabelColor`, `.windowBackgroundColor`,
  `.controlBackgroundColor`, `.separatorColor`, `.controlAccentColor`. Never hard-code the
  accent: the user chooses it. Layer colours must be reset on appearance change
  (`viewDidChangeEffectiveAppearance`).
- **Spacing.** The 4pt scale applies to the space you add. System controls bring their own
  metrics; use `controlSize` to change density, not custom heights.
- **Materials.** `NSVisualEffectView` with a semantic material (`.sidebar`, `.headerView`,
  `.popover`). On macOS 26, system sidebars and toolbars supply glass; `NSGlassEffectView` is
  for a custom floating control. Content stays opaque.
- **Symbols.** SF Symbols in toolbars and sidebars, with a label for the toolbar's text mode
  and a tooltip.

## Standard structure

```swift
final class LibraryWindowController: NSWindowController {
  convenience init() {
    let split = NSSplitViewController()
    let sidebar = NSSplitViewItem(sidebarWithViewController: NSViewController())
    sidebar.minimumThickness = 180
    split.addSplitViewItem(sidebar)
    split.addSplitViewItem(NSSplitViewItem(viewController: NSViewController()))
    let inspector = NSSplitViewItem(inspectorWithViewController: NSViewController())
    inspector.isCollapsed = true
    split.addSplitViewItem(inspector)

    let window = NSWindow(contentViewController: split)
    window.title = "Recordings"
    window.styleMask.insert([.resizable, .miniaturizable, .closable, .fullSizeContentView])
    window.contentMinSize = NSSize(width: 640, height: 400)
    window.setFrameAutosaveName("Library")        // remembers size and position
    window.toolbarStyle = .unified
    window.toolbar = NSToolbar(identifier: "library")
    self.init(window: window)
  }
}

enum MainMenu {
  /// Every command is a menu item. The action travels the responder chain, so the item
  /// enables itself only when something can handle it.
  static func recordItem() -> NSMenuItem {
    let item = NSMenuItem(title: "New Recording", action: #selector(LibraryActions.newRecording(_:)), keyEquivalent: "n")
    item.keyEquivalentModifierMask = [.command]
    return item
  }
}

@objc protocol LibraryActions {
  func newRecording(_ sender: Any?)
}
```

- **Lists:** `NSTableView` or `NSOutlineView` (`style = .sourceList` in a sidebar, `.inset` in
  content). They bring selection, keyboard navigation, type-to-select, sorting and drag and
  drop.
- **Tasks:** a sheet on the window for a task tied to that window, a popover for a small
  transient edit, a separate window for something the user keeps open beside the main one.
- **Primary action:** the default button (`keyEquivalent = "\r"`) in a dialog; a toolbar item
  plus a menu command in a main window. One per window.
- **Settings:** a separate Settings window, opened with Command-comma.

In a SwiftUI Mac app, the same structure:

```swift
import SwiftUI

struct LibraryScene: Scene {
  var body: some Scene {
    WindowGroup {
      LibraryView()
        .frame(minWidth: 640, minHeight: 400)
    }
    .commands {
      CommandGroup(replacing: .newItem) {
        Button("New Recording") {}.keyboardShortcut("n")
      }
      CommandMenu("Playback") {
        Button("Play") {}.keyboardShortcut(.space, modifiers: [])
      }
    }
    Settings {
      Form { Toggle("Skip silence", isOn: .constant(true)) }
        .formStyle(.grouped)
    }
  }
}

struct LibraryView: View {
  @State private var selection: Int?
  @State private var showsInspector = false

  var body: some View {
    NavigationSplitView {
      List(selection: $selection) {
        Label("All Recordings", systemImage: "waveform").tag(0)
      }
      .navigationSplitViewColumnWidth(min: 180, ideal: 220)
    } detail: {
      Text("Select a recording")
        .foregroundStyle(.secondary)
        .inspector(isPresented: $showsInspector) { Text("Details") }
        .toolbar {
          ToolbarItem(placement: .primaryAction) {
            Button("New Recording", systemImage: "plus") {}
              .help("Start a new recording")
          }
        }
    }
  }
}
```

## Interruptibility on the Mac

Most Mac interactions are clicks and key presses, so the common cases are **reverse** and
**rapid input**: the user toggles a panel twice, or holds an arrow key. The rules are the same as
in `motion.md`: no input lock, start from the presented value, nothing queued.

- Never disable a control or ignore events while an animation runs.
- Keep animations short. A Mac user repeats commands quickly; a 0.2 to 0.35 second spring with
  no bounce is the default.
- Scroll views, split views, sheets and popovers already animate correctly. Do not re-time
  them.

On macOS 15 and later, `NSAnimationContext.animate(_:changes:)` takes a SwiftUI `Animation` and
retargets a running animation with its velocity:

```swift
@available(macOS 15, *)
final class DrawerController: NSViewController {
  private let drawer = NSView()
  private var isOpen = false

  @objc func toggleDrawer(_ sender: Any?) {
    isOpen.toggle()
    let reduceMotion = NSWorkspace.shared.accessibilityDisplayShouldReduceMotion
    let spring: Animation = reduceMotion
      ? .smooth(duration: 0.15)
      : .spring(duration: Motion.panelDuration, bounce: Motion.panelBounce)
    NSAnimationContext.animate(spring) {
      self.drawer.frame.origin.y = self.isOpen ? 0 : -self.drawer.frame.height
    }
  }
}
```

On earlier targets, animate the layer with a spring that starts from the presentation value, so
a reversal turns around from where the layer is:

```swift
final class LegacyDrawerController: NSViewController {
  private let drawer = NSView()
  private var isOpen = false

  override func viewDidLoad() {
    super.viewDidLoad()
    drawer.wantsLayer = true
    drawer.layer?.cornerRadius = Corner.panel
    drawer.layer?.cornerCurve = .continuous
    view.addSubview(drawer)
  }

  @objc func toggleDrawer(_ sender: Any?) {
    isOpen.toggle()
    guard let layer = drawer.layer else { return }
    let keyPath = "transform.translation.y"
    let target: CGFloat = isOpen ? 0 : -drawer.bounds.height
    let current = layer.presentation()?.value(forKeyPath: keyPath) as? CGFloat ?? target

    let spring = CASpringAnimation(perceptualDuration: Motion.panelDuration, bounce: Motion.panelBounce)
    spring.keyPath = keyPath
    spring.fromValue = current
    spring.toValue = target
    spring.duration = spring.settlingDuration
    layer.setValue(target, forKeyPath: keyPath)      // the model value is the target at once
    layer.add(spring, forKey: "drawer")              // replaces the running animation
  }
}
```

For simple property changes without a spring, `NSAnimationContext.runAnimationGroup` with
`allowsImplicitAnimation` and the `animator()` proxy is enough; keep the duration under about
0.25 seconds.

## Feedback

- Hover: a tracking area with `.mouseEnteredAndExited` and `.inVisibleRect`; show the state on
  the first frame.
- Focus: keep the system focus ring; make custom controls accept first responder and draw it.
- Haptics exist only on Force Touch trackpads: `NSHapticFeedbackManager` with `.alignment` when
  a drag snaps to a guide, `.levelChange` for a discrete step. Use them sparingly.
- Sound and bounce are not feedback on the Mac. Do not port iOS haptic moments as animations.

## Dials and variations

- Put the dials panel in its own window or an inspector, opened from a Debug menu that exists
  only in debug builds. A SwiftUI `Form` in an `NSHostingController` is the cheapest panel.
- Structure toggles: draw layout guides and control frames in an overlay view; show the
  first responder and the interaction state in a readout.
- The contact sheet from `assets/swift/DesignPlayground.swift` runs on macOS. Use a window
  size, not a device size, as the canvas, and render a second sheet at the minimum window size.
  Wrap AppKit views in an `NSViewRepresentable`.
- `#Preview { SomeNSViewController() }` works for AppKit (macOS 14 SDK).

## Checks before the gate

- Build and launch it. Resize the window to its minimum and to full screen.
- Do the screen's whole job with the keyboard only, then with the pointer only.
- Walk the menu bar: every command is there, with its shortcut, enabled only when it applies.
- Light and dark, a non-default accent colour, Increase Contrast, Reduce Motion.
- Toggle every animated panel rapidly; hold arrow keys in lists.
- VoiceOver reads the sidebar, the list and the primary action.
- Run `scripts/check_swift_ui.py` on the files you wrote.
- State in the report which of these were done and which were not.

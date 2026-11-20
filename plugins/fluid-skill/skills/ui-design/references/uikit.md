# Building in UIKit

Patterns and pitfalls for steps 6 and 7 in a UIKit codebase. Follow the project's own coding
guide, layout approach (Auto Layout, manual frames, a layout library) and design system first;
this file fills gaps. Do not introduce SwiftUI views into a UIKit screen as part of a design
task; a debug-only dials panel hosted in a `UIHostingController` is the one exception. The code
blocks here are type-checked against the SDK by `tools/typecheck-snippets.py`; they were not
run.

## Tokens first

```swift
import UIKit

enum Spacing {
  static let s1: CGFloat = 4
  static let s2: CGFloat = 8
  static let s3: CGFloat = 12
  static let s4: CGFloat = 16
}

enum Corner {
  static let card: CGFloat = 24
  static func inner(_ outer: CGFloat, inset: CGFloat) -> CGFloat { max(0, outer - inset) }
}

enum Motion {
  static let sheetDuration: TimeInterval = 0.45
  static let sheetBounce: CGFloat = 0.15
  static let projection: CGFloat = 0.2      // seconds of momentum added to the release position
}

enum TextRole {
  static var rowTitle: UIFont {
    UIFontMetrics(forTextStyle: .body).scaledFont(for: .systemFont(ofSize: 17, weight: .semibold))
  }
  static var rowDetail: UIFont { .preferredFont(forTextStyle: .footnote) }
}
```

- **Type.** `UIFont.preferredFont(forTextStyle:)`, or `UIFontMetrics` for a weight or a brand
  face. Every label sets `adjustsFontForContentSizeCategory = true` and `numberOfLines = 0`
  unless truncation is intended. A fixed `systemFont(ofSize:)` on its own ignores the user's
  text size.
- **Colour.** `.label`, `.secondaryLabel`, `.systemBackground`, `.secondarySystemBackground`,
  `.systemGroupedBackground`, `.separator`, `.tintColor`. Custom colours come from the asset
  catalogue. Layer colours (`CGColor`) do not update on their own: set them again when the
  appearance changes.
- **Margins.** Pin content to `layoutMarginsGuide`, and long text to `readableContentGuide`.
  Set `directionalLayoutMargins` only to a value on the spacing scale. Use leading and trailing
  anchors, never left and right.
- **Corners.** `layer.cornerCurve = .continuous` on every rounded layer. On iOS 26 and later
  `cornerConfiguration` can make a view concentric with its container; earlier, compute
  `outer − inset`.

```swift
final class RecordingCardView: UIView {
  private let artwork = UIImageView(image: UIImage(systemName: "waveform"))
  private let title = UILabel()
  private let stack = UIStackView()

  override init(frame: CGRect) {
    super.init(frame: frame)
    backgroundColor = .secondarySystemBackground
    layer.cornerRadius = Corner.card
    layer.cornerCurve = .continuous
    directionalLayoutMargins = NSDirectionalEdgeInsets(
      top: Spacing.s3, leading: Spacing.s3, bottom: Spacing.s3, trailing: Spacing.s3)

    artwork.backgroundColor = .tertiarySystemFill
    artwork.layer.cornerCurve = .continuous
    if #available(iOS 26, *) {
      artwork.cornerConfiguration = .corners(radius: .containerConcentric(minimum: 4))
    } else {
      artwork.layer.cornerRadius = Corner.inner(Corner.card, inset: Spacing.s3)
    }

    title.font = TextRole.rowTitle
    title.adjustsFontForContentSizeCategory = true
    title.numberOfLines = 0
    title.textColor = .label

    stack.addArrangedSubview(artwork)
    stack.addArrangedSubview(title)
    stack.spacing = Spacing.s3
    stack.alignment = .center
    stack.translatesAutoresizingMaskIntoConstraints = false
    addSubview(stack)
    NSLayoutConstraint.activate([
      artwork.widthAnchor.constraint(equalToConstant: 56),
      artwork.heightAnchor.constraint(equalTo: artwork.widthAnchor),
      stack.topAnchor.constraint(equalTo: layoutMarginsGuide.topAnchor),
      stack.bottomAnchor.constraint(equalTo: layoutMarginsGuide.bottomAnchor),
      stack.leadingAnchor.constraint(equalTo: layoutMarginsGuide.leadingAnchor),
      stack.trailingAnchor.constraint(equalTo: layoutMarginsGuide.trailingAnchor),
    ])

    registerForTraitChanges([UITraitPreferredContentSizeCategory.self]) { (view: Self, _: UITraitCollection) in
      view.updateAxis()
    }
  }

  override func didMoveToWindow() {
    super.didMoveToWindow()
    updateAxis()
  }

  private func updateAxis() {
    stack.axis = traitCollection.preferredContentSizeCategory.isAccessibilityCategory ? .vertical : .horizontal
  }

  @available(*, unavailable)
  required init?(coder: NSCoder) { fatalError() }
}
```

Trait-change registration does not perform the initial layout update. Apply the current category
when the view joins its window as well as when the category changes; an accessibility launch
must not wait for a settings change before restacking.

## Standard components first

- **Lists:** `UICollectionView` with `UICollectionLayoutListConfiguration` and
  `UIListContentConfiguration`, or `UITableView`. They bring swipe actions, selection, editing,
  separators and self-sizing rows for Dynamic Type.
- **Buttons:** `UIButton.Configuration` (`.filled()` for the one prominent action, `.plain()`,
  `.tinted()`; `.glass()` and `.prominentGlass()` on iOS 26). Configurations handle states,
  Dynamic Type, pointer effects and minimum sizes better than a custom control.
- **Bars:** `UINavigationController`, `UITabBarController`, `UIToolbar`, `UIBarButtonItem`,
  `UIMenu` for secondary actions. Do not hide the navigation bar to draw your own; that loses
  the back swipe and the scroll-edge appearance.
- **Presentation:** `UISheetPresentationController` with detents and a grabber, popovers on
  iPad, `UIContextMenuInteraction` as a shortcut.
- **Empty states:** `UIContentUnavailableConfiguration` (iOS 17).
- **iPad:** `UISplitViewController` for regular width; respond to size class changes, not to
  the device idiom.

```swift
final class LibraryViewController: UIViewController {
  private let source = UIView()

  func makeListLayout() -> UICollectionViewLayout {
    var configuration = UICollectionLayoutListConfiguration(appearance: .insetGrouped)
    configuration.trailingSwipeActionsConfigurationProvider = { _ in
      UISwipeActionsConfiguration(actions: [
        UIContextualAction(style: .destructive, title: "Delete") { _, _, done in done(true) }
      ])
    }
    return UICollectionViewCompositionalLayout.list(using: configuration)
  }

  func makeCarouselSection() -> NSCollectionLayoutSection {
    let item = NSCollectionLayoutItem(layoutSize: .init(
      widthDimension: .fractionalWidth(1), heightDimension: .fractionalHeight(1)))
    let group = NSCollectionLayoutGroup.horizontal(
      layoutSize: .init(widthDimension: .fractionalWidth(0.8), heightDimension: .absolute(200)),
      subitems: [item])
    let section = NSCollectionLayoutSection(group: group)
    section.interGroupSpacing = Spacing.s3
    section.orthogonalScrollingBehavior = .groupPagingCentered   // native snap and momentum
    return section
  }

  func presentDetail(_ detail: UIViewController) {
    if #available(iOS 18, *) {
      detail.preferredTransition = .zoom { [source] _ in source }   // interruptible, drag to go back
    }
    if let sheet = detail.sheetPresentationController {
      sheet.detents = [.medium(), .large()]
      sheet.prefersGrabberVisible = true
    }
    present(detail, animated: true)
  }
}
```

## Whole targets, pointer and keyboard

- A tappable card is a `UIControl` (or a list cell), not a view with a tap gesture recogniser:
  a control gives the highlighted state, the accessibility trait and pointer support.
- Show the highlight on touch-down, in `isHighlighted`'s observer, with a short spring.
- Keep the visible glyph small and the target at 44 by 44 points by widening hit testing.
- On iPad add key commands for the primary action, and pointer interactions for custom
  controls.

```swift
final class GlyphControl: UIControl {
  override func point(inside point: CGPoint, with event: UIEvent?) -> Bool {
    let dx = min(0, (bounds.width - 44) / 2)
    let dy = min(0, (bounds.height - 44) / 2)
    return bounds.insetBy(dx: dx, dy: dy).contains(point)
  }

  override var isHighlighted: Bool {
    didSet {
      UIView.animate(springDuration: 0.2, bounce: 0, options: [.allowUserInteraction, .beginFromCurrentState]) {
        self.alpha = self.isHighlighted ? 0.6 : 1
      }
    }
  }
}
```

## Interruptibility

Three rules in UIKit terms:

- Always pass `.allowUserInteraction` and `.beginFromCurrentState` to block-based animations,
  or use an API that implies them.
- Never set `isUserInteractionEnabled = false` or `isEnabled = false` to wait for an animation,
  and never unlock anything in a completion handler.
- Animate with springs. `UIView.animate(withDuration:delay:options:)` with a curve cannot carry
  velocity into the next change.

### iOS 18 and later: SwiftUI springs on UIKit views

`UIView.animate(_:changes:)` takes a SwiftUI `Animation`. Changes made during a gesture with
`.interactiveSpring` and the change made on release with a spring form one continuous motion:
velocity is carried over, and a new change retargets the running one.

```swift
import SwiftUI

@available(iOS 18, *)
final class MiniPlayerController: UIViewController {
  private let panel = RecordingCardView()
  private var isExpanded = false
  private var travel: CGFloat { -view.bounds.height * 0.6 }
  private let landing = UIImpactFeedbackGenerator(style: .light)

  override func viewDidLoad() {
    super.viewDidLoad()
    view.addSubview(panel)
    panel.addGestureRecognizer(UIPanGestureRecognizer(target: self, action: #selector(pan)))
    panel.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(toggle)))
    panel.isAccessibilityElement = true
    panel.accessibilityTraits = .button
  }

  @objc private func toggle() { settle(expanded: !isExpanded) }

  @objc private func pan(_ gesture: UIPanGestureRecognizer) {
    switch gesture.state {
    case .began:
      landing.prepare()
    case .changed:
      let resting = isExpanded ? travel : 0
      let offset = resting + gesture.translation(in: view).y
      UIView.animate(.interactiveSpring) { self.panel.transform = CGAffineTransform(translationX: 0, y: offset) }
    case .ended, .cancelled:
      let projected = panel.transform.ty + gesture.velocity(in: view).y * Motion.projection
      settle(expanded: projected < travel / 2)
    default:
      break
    }
  }

  private func settle(expanded: Bool) {
    isExpanded = expanded
    let spring: Animation = UIAccessibility.isReduceMotionEnabled
      ? .smooth(duration: 0.25)
      : .spring(duration: Motion.sheetDuration, bounce: Motion.sheetBounce)
    UIView.animate(spring) {
      self.panel.transform = CGAffineTransform(translationX: 0, y: expanded ? self.travel : 0)
    } completion: {
      self.landing.impactOccurred()    // cleanup and feedback only; nothing is unlocked here
    }
  }
}
```

### iOS 17 and earlier: a property animator per settle

Stop the running animator where it is, then start a new spring from there with the gesture's
velocity. `stopAnimation(true)` leaves the view at its in-flight position, so there is no jump.
The initial velocity of `UISpringTimingParameters` is relative: points per second divided by the
distance still to travel.

```swift
final class LegacyMiniPlayerController: UIViewController {
  private let panel = RecordingCardView()
  private var animator: UIViewPropertyAnimator?
  private var isExpanded = false
  private var collapsedY: CGFloat { view.bounds.maxY - 80 }
  private var expandedY: CGFloat { view.bounds.midY }

  @objc private func pan(_ gesture: UIPanGestureRecognizer) {
    switch gesture.state {
    case .began:
      animator?.stopAnimation(true)                   // catch it mid-flight, at the presented position
    case .changed:
      panel.center.y += gesture.translation(in: view).y
      gesture.setTranslation(.zero, in: view)
    case .ended, .cancelled:
      let velocity = gesture.velocity(in: view).y
      let projected = panel.center.y + velocity * Motion.projection
      settle(expanded: projected < (collapsedY + expandedY) / 2, velocity: velocity)
    default:
      break
    }
  }

  private func settle(expanded: Bool, velocity: CGFloat) {
    animator?.stopAnimation(true)
    isExpanded = expanded
    let target = expanded ? expandedY : collapsedY
    let distance = target - panel.center.y
    let relative = distance == 0 ? 0 : velocity / distance
    let timing = UISpringTimingParameters(dampingRatio: 0.86, initialVelocity: CGVector(dx: 0, dy: relative))
    let next = UIViewPropertyAnimator(duration: Motion.sheetDuration, timingParameters: timing)
    next.addAnimations { self.panel.center.y = target }
    next.startAnimation()
    animator = next
  }
}
```

Points that matter in both versions:

- While dragging, the view is set directly from the gesture; nothing animates toward the
  finger with a delay.
- The landing is decided from the projected position, so a flick commits from anywhere.
- A tap, a second drag or a programmatic change during the settle starts from the presented
  position, because nothing is locked.
- The gesture has a non-gesture route (the tap, and the accessibility activation that comes
  with the button trait).
- For a custom gesture inside a scroll view, set a relationship with the scroll view's pan
  (`require(toFail:)` or the delegate methods) so the scroll wins on its axis.

## Haptics and Reduce Motion

- Create the generator once, call `prepare()` when the gesture begins, and fire at the state
  boundary: `UIImpactFeedbackGenerator` for a landing, `UISelectionFeedbackGenerator` for a
  detent or picker step, `UINotificationFeedbackGenerator` for success or failure.
- Read `UIAccessibility.isReduceMotionEnabled` wherever a spring overshoots or a view travels
  far, and use a cross-fade or a spring with no bounce.

## Dials in a debug build

Keep a `#if DEBUG` file with one observable object holding the tunable values, and token
accessors that read it in debug builds and the constants in release builds (the same shape as in
`swiftui.md`). Present the panel from a debug entry point (a shake in a `UIWindow` subclass, or
the project's debug menu) as a sheet with a medium detent; a SwiftUI `Form` in a
`UIHostingController` is the cheapest panel. Structure toggles:

- **Layout guides:** an overlay view that draws `layoutMarginsGuide`, `readableContentGuide`
  and `safeAreaLayoutGuide`.
- **Hit areas:** outline every `UIControl` in the hierarchy, using its hit-test bounds.
- **State readout:** a label fed by the interaction's state, offset and velocity.
- **Slow motion:** Simulator → Debug → Slow Animations, or `window.layer.speed = 0.2` in a
  debug build.

## Variations and previews

`#Preview { SomeViewController() }` and `#Preview { SomeView() }` work for UIKit (iOS 17 SDK).
For a contact sheet, wrap the layout view in a `UIViewRepresentable` and pass it to
`ContactSheet` from `assets/swift/DesignPlayground.swift`, inside `#if DEBUG` (see
`variations.md`).

## Checks before the gate

- Build it for the deployment target.
- Run at the default and the largest accessibility text size, light and dark, smallest and
  largest width, and on iPad in a narrow multitasking width if the app supports iPad.
- Run the four interruption tests with slow animations, on a device if possible.
- VoiceOver reaches and names the primary action; the Accessibility Inspector audit is clean.
- Run `scripts/check_swift_ui.py` on the files you wrote.
- State in the report which of these were done and which were not.

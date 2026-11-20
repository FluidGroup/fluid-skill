# Components

Read when the feature is a whole surface: a sheet, a list, a chat screen, a
camera, an image editor, or a visual effect. Repositories are under
`https://github.com/FluidGroup/`. The floor is the package's declared minimum;
**untagged** and **private API** are explained in `SKILL.md`.

## Sheets and Floating Surfaces

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| A SwiftUI sheet with custom detents, shown inline in the layout or presented, dragged with rubber banding | `swiftui-blanket` | `SwiftUIBlanket`: `.blanket(isPresented:)`, `.blanket(item:)`, `.blanketContentDetents(_:)` | iOS 16 | Untagged. Use `.sheet` with `presentationDetents` when the system sheet's look and behavior are acceptable |
| A UIKit drawer like Maps or Shortcuts with several snap points and scroll view coordination | `Rideau` | `Rideau`: `RideauView` (inline), `RideauViewController` (modal) | iOS 13 | Snap points `.hidden`, `.fraction`, `.pointsFromBottom`, `.full` |
| A compact bar that expands into a detail surface, like the Apple Music mini player | `swiftui-persistent-control` | `SwiftUIPersistentControl`: `Container` | iOS 18 | Untagged, no README; read the source and previews first |
| A notification banner that slides in and can be flicked away | `swiftui-glance` | `SwiftUIGlance` | iOS 15 | Untagged, no README. In UIKit, `FluidSnackbar` from `FluidInterfaceKit` |

## Lists and Scrolling

All from `swiftui-list-support` (iOS 17, macOS 15). Depend only on the
product needed.

| Need | Product | Entry point | Notes |
| --- | --- | --- | --- |
| Trigger loading more content near the end of a `ScrollView` or `List` | `ScrollTracking` | `.onAdditionalLoading` | Uses introspection |
| Pull to refresh with a custom indicator, or any pull-distance interaction | `PullingControl` | `RefreshControl` (high level), `PullingControl` (low level) | `refreshable` is enough for the system indicator |
| A header that sticks and stretches on overscroll | `StickyHeader` | `StickyHeader` | |
| Single or multiple selection in any container | `SelectableForEach` | `SelectableForEach`, selection state through the environment | `List(selection:)` is enough for a plain system list |
| A very large or heavily updated list where lazy stacks are too slow | `DynamicList` | `DynamicListView` (a `UICollectionView` with diffable data source and SwiftUI cells) | Use only after `List` or a lazy stack is measured to be the problem |
| List and grid layouts behind one container | `CollectionView` | `CollectionView` with `.list`, `.grid`, `.platformList` | Pure SwiftUI |

## Chat

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| A message list that prepends older messages without scroll jumps, follows the keyboard, auto-scrolls, reveals timestamps on swipe, and shows typing and loading indicators | `swiftui-messaging-ui` | `MessagingUI`: `TiledView` | iOS 17 | `UICollectionView`-backed with SwiftUI cells. It provides the list infrastructure; bubbles and the composer are the app's |

Adjusting `contentOffset` after an insert, or inverting a `ScrollView`, are the
approaches this package exists to replace. Do not hand-roll either for a chat
screen.

## Camera and Image Editing

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| A SwiftUI capture screen where the app draws the preview frame, shutter, and dials, and the library supplies camera behavior | `swiftui-camera` | `Camera`: `Camera(photo:)`, `CameraPreview`, `Shutter`, `.onPhotoCapture` | iOS 18, macOS 26 | Untagged. Runs a simulated camera in the Simulator and in previews |
| A lower-level `AVCaptureSession` wrapper with inputs, outputs, and a pixel-buffer preview | `Capturer` | `Capturer`: `CaptureBody`, `CameraInput`, `PhotoOutput`, `PreviewOutput` | iOS 16 | Use when the app needs its own pipeline |
| A photo editor: crop, adjustments, filters, masks, undo history, export | `Brightroom` | `BrightroomUI` (built-in editor and canvas), `BrightroomEngine` (documents and rendering), `BrightroomParametric` (features and Core Image, no SwiftUI) | iOS 17 (`BrightroomParametric` also macOS 14) | Requires Swift 6.3. Take `BrightroomEngine` alone to render without UI |

`PhotosPicker` and `UIImagePickerController` are enough when the app only
needs a photo, not a capture experience.

## Visual Effects

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| A blur of the content behind a view with a chosen radius, uniform or progressive | `swiftui-backdrop-blur` | `BackdropBlur`: `BackdropBlurView(blurRadius:)` | iOS 17 | **Private API.** A system `Material` is the default; use this only when the design needs a specific radius or a gradient of blur |
| Scroll content that fades out at the edges | `swiftui-scroll-edge-effect` | `ScrollEdgeEffect`: `ScrollEdgeEffectScrollView` (iOS 17), a modifier on an existing scroll view (iOS 18) | iOS 17, macOS 14 | |
| A linear gradient without the visible banding or hard midpoint of `LinearGradient` | `swiftui-gaussian-linear-gradient` | `GaussianLinearGradient`: a `View` and `ShapeStyle` with `LinearGradient`'s initializers | iOS 17, macOS 14 | Typical use: scrims over images |
| A live mirror of a mounted view shown elsewhere while the original keeps its state | `swiftui-portal` | `Portal`: `MirrorView`, `@PortalSource` | iOS 17 | **Private API.** Untagged |
| Lifting live content into an overlay above a blurred screen, like a context menu preview | `swiftui-context-overlay` | `ContextOverlay`: `ContextOverlayContainer` | iOS 17 | **Private API** through `Portal` and `BackdropBlur`. Untagged. `contextMenu(menuItems:preview:)` is the system form |

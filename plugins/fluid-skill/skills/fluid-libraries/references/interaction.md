# Interaction, Gestures, and Navigation

Read when the feature is something the finger moves: a draggable view, a
custom slider, or a transition between screens. These packages already
implement what `coding-aesthetics` asks of direct manipulation (relative
tracking, release velocity, rubber banding, recovery on cancellation), which
is the part hand-written versions usually get wrong. Repositories are under
`https://github.com/FluidGroup/`.

## Dragging

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| A view that is dragged along one or both axes, rubber-bands at its limits, and springs to a target using release velocity (swipe actions, throwable cards, dismissible panels) | `swiftui-snap-dragging-modifier` | `SwiftUISnapDraggingModifier`: `SnapDraggingModifier` | iOS 16 | `.directional` and scroll-view-interoperable gesture modes need iOS 18 |
| The same for a `UIView` | `FluidInterfaceKit` | `FluidGesture`: `view.makeDraggable(descriptor:)` | iOS 17 | |
| A drag that yields to a scroll view and takes over when the content reaches an edge (a sheet or pager that contains a scroll view) | `swiftui-scrollview-interoperable-drag-gesture` | `SwiftUIScrollViewInteroperableDragGesture`: `ScrollViewInteroperableDragGesture`, `UIScrollViewInteroperableDragGestureRecognizer` | iOS 18 to use | Built on `UIGestureRecognizerRepresentable` |
| Release velocity in pt/s from a plain `DragGesture` | `swiftui-gesture-velocity` | `SwiftUIGestureVelocity`: `@GestureVelocity`, `.updatingVelocity($velocity)` | iOS 13 | For a custom gesture that `SnapDraggingModifier` does not cover |
| The rubber-band curve itself | `swift-rubber-banding` | `RubberBanding`: `rubberBand(value:min:max:bandLength:)` | none | One function; copying it is fine when nothing else needs the package |

Reach for `SnapDraggingModifier` before composing `DragGesture`,
`@GestureState`, and a spring by hand. Write the gesture yourself when the
motion is not "follow, then settle" (drawing, scrubbing, multi-touch).

## Sliders and Dials

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| A reel that slides under a fixed center mark for precise values, like the Photos adjustment slider | `PrecisionLevelSlider` | `PrecisionLevelSlider`: `SwiftUIPrecisionLevelSlider`, `PrecisionLevelSlider` (UIKit) | iOS 17 | The app draws the center level and the track; haptics are a callback |
| An endless rotary dial for fine adjustment (rotation, hue) | `swiftui-ring-slider` | `SwiftUIRingSlider`: `RingSlider(value:)` | iOS 17 | Built-in haptic feedback |
| A bar the user adjusts by dragging anywhere on it (brightness, volume) | `swiftui-touch-slider` | `TouchSlider`: `TouchSlider(direction:value:speed:…)` | iOS 14 | |
| Pinch to zoom an image in place, like a feed photo | `InteractiveZoomDriver` | `InteractiveZoomDriver`: `InteractiveZoomView`, `InteractiveZoomSwiftUIView` | iOS 13 | |

`Slider` is correct for an ordinary bounded value. These exist for designs
where a knob is the wrong control.

## Navigation and Transitions

| Need | Package | Product and entry point | Floor | Notes |
| --- | --- | --- | --- | --- |
| A SwiftUI stack with custom and contextual (zoom from a cell) transitions | `swiftui-stack` | `SwiftUIStack`: `Stack`, `StackLink`, `StackUnwindLink` | iOS 14 | Check `NavigationStack` with `navigationTransition(.zoom)` first (iOS 18) |
| A UIKit app whose screens stack with interactive, interruptible custom transitions instead of `UINavigationController` and modal presentation | `FluidInterfaceKit` | `FluidStack`: `FluidStackController`, `FluidViewController`, `fluidPush`, `fluidPop` | iOS 17 | **Private API** through `FluidPortal`, which contextual transitions use. Replaces system navigation for the whole app, giving up the back-button history menu, page sheets, and some accessibility behavior. An architecture decision for the user, not a component to drop in |
| Floating UIKit surfaces: snackbars, tooltips, picture-in-picture, keyboard tracking | `FluidInterfaceKit` | `FluidSnackbar`, `FluidTooltipSupport`, `FluidPictureInPicture`, `FluidKeyboardSupport` | iOS 17 | Each is a separate product. `FluidTooltipSupport` and `FluidPictureInPicture` (through `FluidStack`) depend on `FluidPortal` (**private API**) |

Standard navigation is the default. Recommend these only when the requirement
names a transition or stacking behavior the system container cannot produce.

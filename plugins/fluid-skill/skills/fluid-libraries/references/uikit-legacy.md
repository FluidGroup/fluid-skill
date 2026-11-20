# UIKit and Texture Codebases

Read only when working in an existing UIKit or Texture (AsyncDisplayKit)
codebase. These packages are stable and still used in such apps, but most
predate SwiftUI's current APIs. Keep using one where the project already
depends on it; do not introduce one into a SwiftUI screen or a new app, where
the platform or a package from the other references is the better answer.
Repositories are under `https://github.com/FluidGroup/`.

| Need | Package | Product and entry point | Floor | In new code |
| --- | --- | --- | --- | --- |
| A scrolling form built from stacked views | `StackScrollView` | `StackScrollView` | iOS 11 | `UIStackView` in a scroll view, or SwiftUI `Form` and `List` |
| Auto Layout written as a declarative tree | `MondrianLayout` | `MondrianLayout` | iOS 12 | Layout anchors, or SwiftUI |
| A text view that grows with its content, for a chat composer | `NextGrowingTextView` | `NextGrowingTextView` | iOS 10 | `TextField(axis: .vertical)` in SwiftUI |
| Typed `NSAttributedString` attributes | `TypedTextAttributes` | `TypedTextAttributes` | iOS 12 | `AttributedString` |
| A custom view shown in place of the keyboard | `Bureau` | `Bureau` | iOS 12 | |
| Data-driven collection and table views with diffing | `DataSources` | `DataSources` | iOS 16 | Diffable data sources |
| Composing small UIKit components | `CompositionKit` | `CompositionKit` | iOS 12 | |
| Mapping a progress value through ranges for interactive transitions | `TransitionPatch` | `TransitionPatch` | iOS 10 | |
| A matched-geometry style transition between two UIKit views | `MatchedTransition` | `MatchedTransition` | iOS 12 | |
| Measuring a view's fitting size | `ViewSizeCalculator` | `ViewSizeCalculator` | iOS 12 | |
| `CGRect` and `CGSize` fitting and aspect helpers | `GeometryKit` | `GeometryKit` | iOS 11 | |
| Texture layout specs in a Swift DSL, buttons, and Auto Layout bridging | `TextureSwiftSupport`, `GlossButtonNode`, `TextureBridging` | same names | iOS 13 | Only in apps already on Texture |

The actively developed UIKit packages are listed with the features they
provide: `Rideau` in [components.md](components.md), and `FluidInterfaceKit`
and `InteractiveZoomDriver` in [interaction.md](interaction.md).

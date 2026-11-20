import SwiftUI

struct LightScene: Identifiable {
  let id: Int
  let name: String
  let detail: String
  let symbol: String
}

struct SceneCardsView: View {
  let scenes = [
    LightScene(id: 0, name: "Pulse", detail: "Brightness varies slowly", symbol: "flame"),
    LightScene(id: 1, name: "Flow", detail: "Shapes move across the screen", symbol: "wind"),
    LightScene(id: 2, name: "Gradient", detail: "Colours change gradually", symbol: "water.waves"),
  ]

  var body: some View {
    ScrollView {
      VStack(spacing: 28) {
        ForEach(scenes) { scene in
          VStack(alignment: .leading, spacing: 12) {
            Image(systemName: scene.symbol)
              .font(.largeTitle)
              .frame(maxWidth: .infinity)
              .frame(height: 160)
              .background(.fill.tertiary, in: RoundedRectangle(cornerRadius: 24, style: .continuous))
            Text(scene.name).font(.headline)
            Text(scene.detail).font(.subheadline).foregroundStyle(.secondary)
          }
          .padding(12)
          .background(.background.secondary, in: RoundedRectangle(cornerRadius: 24, style: .continuous))
        }
      }
      .padding(.horizontal, 16)
    }
    .navigationTitle("Scenes")
  }
}

#Preview {
  NavigationStack { SceneCardsView() }
}

---
type: llm
focus: trace
weight: 1
---

In the edited SceneCardsView.swift the image corner is concentric with the card: its radius equals the card radius minus the card padding (12 with a 24 card radius and 12 padding), or it uses ConcentricRectangle behind an availability check with that value as the fallback.

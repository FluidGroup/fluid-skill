---
type: llm
focus: output
weight: 1
---

A small persisted command exports the real comparison View and fixtures, not duplicated UI.
It fixes variant order, width, scale, appearance, locale, layout direction and text environment,
supports an explicit output directory, fails on capture/encoding errors, and keeps generated
images, executables and metadata out of Git. Conditions, dimensions, OS/toolchain, Git state and
relevant source hashes identify the export. Regeneration and a path with spaces are checked, or
explicitly reported unverified. The full expected comparison is visible, not just a lazy grid's
viewport. If native views cannot be captured faithfully, the limitation is reported and an
existing supported host is used. macOS ImageRenderer output is labelled as static macOS output,
not iOS Simulator, iOS Dynamic Type, VoiceOver, Reduce Motion, playback or interaction proof.

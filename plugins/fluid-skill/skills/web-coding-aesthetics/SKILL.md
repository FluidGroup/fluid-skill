---
name: web-coding-aesthetics
description: "Design and review web UI code: component ownership and catalogs, CSS modules and corner and shadow primitives, navigation and loading boundaries, accessible controls and scroll effects, client/server authority and HTTP operations, and local development surfaces. Builds on coding-aesthetics, which holds the language-neutral principles; apply both."
metadata:
    github-path: plugins/fluid-skill/skills/web-coding-aesthetics
    github-ref: refs/heads/main
    github-repo: https://github.com/FluidGroup/fluid-skill
---
# Web UI

This skill adds web UI specifics to `coding-aesthetics`, which states the
general principles and the reasons behind them; apply both. Preserve explicit
repository contracts; these choices do not establish a dependency's current
behavior.

## Avoid Appearance Owned by Screens

- A component lives in its own module (context-sharing parts such as tabs may
  share one) and owns appearance, named variants, states, interactions, and
  accessibility; screens compose components with data and actions. Express
  differences as named variants, not screen-specific overrides, and inspect
  existing components before adding another.
- Render the production components in an independent catalog, separating
  primitives, composite components, and screens; a whole-screen example does
  not replace component examples, and a catalog-only copy is not the
  component. Verify fixtures, states, variants, and desktop, touch, and
  keyboard behavior.
- Complex component CSS goes in an adjacent CSS Module; callers never import
  another component's internal classes; one directional layout primitive with
  a named spacing input (in CSS pixels) replaces repeated layout utilities;
  tests target semantic elements, not generated class names.
- App-owned rectangular surfaces (cards, sheets, inputs, buttons, menus) use
  the project's shared continuous-corner primitive with semantic radii; plain
  `border-radius` is the server-rendered fallback; circles, pills, arrows, and
  illustrations are exempt. When a clipped surface needs a shadow, put the
  shape on an inner element and `filter: drop-shadow(...)` on an unclipped
  wrapper; use `outline` for focus; keep the shape owner visible in the
  component API rather than scanning class names and mutating the DOM.

## Avoid Loading That Moves the User

- Navigate to the destination shell first and load inside it; buttons and
  route guards never wait for destination fetching, valid cache shows
  immediately, and back or close stays available. Block in place only when the
  save or authentication result decides navigation.
- One initialization boundary with explicit loading, loaded, and failed states
  keeps navigation outside it; the fetching layer owns start, cache,
  cancellation, and per-user isolation; refetching and its failures stay inside
  the loaded state, preserving mounted content, input, and media. Show empty
  and permission-denied states too. Create typed component families once at
  module scope.
- Reserve the finished layout before content arrives and replace placeholders
  in place; stale responses must not move the user. Verify cold cache, delayed
  and failing requests, and leaving before a response.

## Avoid Controls and Effects That Fight Activity

- If controls hide when idle, keep them visible during keyboard interaction.
  Touch users must be able to reveal controls without triggering the
  underlying action; do not rely on hover as the only way to find them.
- Scroll edge fades are a reusable container with an alpha mask over the real
  background, fading only where content continues, tracking resizes, and
  keeping ref-based scrolling and keyboard control.

## Avoid Hidden Authority Over Server Operations

- A local browser app driving CLI or native workers sends typed commands to a
  server that owns mutable state, worker launch, ordering, timeouts, retries,
  validation, and restart recovery; browser and CLI are thin clients of the
  same command bus, and recovering retained artifacts is a durable server
  transition, not relaunch logic in the UI. A native in-process app needs no
  such server.
- Distinct HTTP operations get explicit methods and paths, not one URL plus an
  action string; share authentication, CORS, and error representation, and
  aggregate metrics by route template rather than by IDs.

## Avoid Surprises in Development Surfaces

- Keep server-only secrets out of browser bundles. Opening local web UI and
  sharing environment values follow `verification.md` in `coding-aesthetics`.

Capturing feedback or revising this skill follows `maintenance.md` in
`coding-aesthetics`.

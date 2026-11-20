# Maintenance

Read only when the user asks to capture feedback, study their code, or revise
these skills: `coding-aesthetics` and its domain skills
(`ios-coding-aesthetics`, `web-coding-aesthetics`). Ordinary coding does not
need this file.

## Avoid Editing the Wrong Copy

Change a skill in its source repository (its metadata names it). Installed
plugin caches and exported copies are distribution artifacts; installing or
publishing is a separate, requested step. Edit a skill only when the user
asks.

## Avoid Promoting an Observation to a Rule

1. Keep new feedback in a local working note first (context, candidate
   decision, current scope, open question) unless it is
   repeated, resolves an ambiguity, or clearly changes future code.
2. Search for the same idea and merge instead of duplicating; give each
   decision one home and keep each `SKILL.md` to principles and routing. A
   language-neutral decision lives in `coding-aesthetics`; a domain skill
   holds only that domain's concrete form of it and the domain's own
   principles, never a restatement.
3. Separate the kind of guidance (style preference, design default,
   correctness contract) from its evidence; never invent a safety or
   performance reason for taste.
4. Phrase a decision as the failure it avoids, why, and what that leaves, with
   the conditions and exceptions that change it. Remove the pending entry once
   it is distilled.
5. When observations conflict, ask the user a two-choice question with a short
   code example for each side; a direct answer outranks code evidence within
   its scope, and library and application guidance stay distinct.

## Avoid Treating Accidents as Preferences

- Direct user guidance establishes a preference without a citation; a
  repository policy stays local unless its reason generalizes.
- An implementation, a commit author, or acceptance of agent-assisted work does
  not prove a style preference. Confirm the reason for a choice before turning
  it into a rule.
- Editor and template residue (labeled closures from completion, whitespace,
  typos, carried-over headers) is not preference; older code reflects older
  APIs. Copied code is not independent confirmation, and reading source proves
  nothing about runtime behavior.
- Never derive blanket rules such as weak capture everywhere, a manager for
  every async flow, locks or noncopyability for every holder, a model for every
  view, silent cancellation, or sharing after a fixed number of repeats.

## Avoid Studying Code Without Labels

When asked to learn from repositories, read representative implementations,
their call sites, design documents, and history, labeling hand-written work and
later accepted changes separately. For each candidate keep the decision, the
cost it avoids, its evidence type, its conditions, and a counterexample. Keep
raw evidence, repository names, and attribution in a local research record
outside the skill; distribute only project-neutral principles with synthetic
examples.

## Avoid Unmeasured Rewrites

To measure or improve how closely agent output matches the user's code:

1. Re-specify hand-written reference code (about 100–900 lines) as a prose
   request with no type names, labels, file layout, or techniques from the
   original (a package name and a required dependency's API may stay).
2. Have a fresh agent implement it with only the skill and the request (no
   network, no original source), and a separate judge compare it with the
   original on layout, API shape, state,
   implementation, formatting, documentation, previews and tests, concision,
   and overall recognizability, classifying each difference as habit, request
   gap, or neutral; add objective counts (files, lines, documentation density,
   README length).
3. Fold in only generalizable habits from training targets, with synthetic
   examples; evaluate held-out targets chosen after freezing a revision, and
   report the two separately.
4. Keep requests, prompts, scripts, generated code, and scores outside the
   distributed skill.

For a structural revision, map every existing decision to its new home before
moving it, keep moves separate from preference changes, and never harden a
default into a ban. Check that links resolve, audit the old and new text
sentence by sentence for dropped qualifiers, exceptions, and negatives (a
keyword check misses them), and rerun a fresh-agent check before shipping.

---
name: long-term-maintainability
description: Distinguish shortsighted minimal code from thoughtful minimal code when designing, implementing, or reviewing software expected to keep evolving. Judge whether a small implementation expresses the problem clearly and leaves room for change, or merely fits today's circumstances. Use for abstraction, boundaries, technical debt, and decisions about what to keep, adjust, or defer; ground recommendations in the code and its contracts.
metadata:
  github-path: plugins/fluid-skill/skills/long-term-maintainability
  github-ref: refs/heads/main
  github-repo: https://github.com/FluidGroup/fluid-skill
---
# Long-Term Maintainability

Minimal code can have very different qualities. One small implementation fits
the immediate task by relying on today's incidental circumstances. Another is
equally small because its concepts and responsibilities have been chosen with
continued evolution in mind. Both may satisfy the current requirement.

Aim for the latter: thoughtful minimalism. Its beauty comes from what remains
after unnecessary machinery is removed: the essential meaning, clear
responsibilities, and few assumptions that a later change must untangle.
Considering the future can improve today's expression of the problem without
adding any future functionality, configuration, or abstraction.

Judge what the code retains and what it leaves out:

- Does it express the actual concept, or use a convenient coincidence that
  happens to give the right result today?
- Are responsibilities and invariants apparent in the small implementation,
  or has brevity made the reader reconstruct them from hidden assumptions?
- Can change be expressed through the responsible concept, or must exceptions
  accumulate around choices tied to today's circumstances?

These are questions about the code and its contracts, not claims about how
much thought its author put in. Support a judgment of quality with concrete
reasoning. Line count, apparent simplicity, and architecture patterns alone
cannot establish it.

Software that keeps improving will outgrow some of today's decisions. Doing
less now often preserves the most options, while even a small implementation
can spread an incidental assumption into callers, persisted data, or public
contracts. The change-cost analysis below helps assess these consequences;
keep it grounded in this distinction between kinds of minimalism.

## Scope

- Apply this lens during design and implementation as well as review. In a
  review, recommend changes; do not rewrite code unless asked.
- Establish whether this is evolving product code, a reusable library, or a
  disposable experiment. Scale the effort to its expected life, consumers,
  delivery constraints, and the consequences of mistakes. If unspecified,
  state a working assumption; ask only when the answer changes the decision.
- This is one review aspect. Correctness remains a requirement. Readability,
  performance, and portability matter here when they create a concrete
  maintenance cost; do not claim to have reviewed those aspects completely.
- Apply `coding-aesthetics` and the matching domain skill when available for
  concrete code-shape defaults. This skill adds the reasoning about change
  costs; it does not replace those defaults or prescribe a new architecture.

## Make the Judgment

### 1. Establish What Must Work and What Is Known

Read the change, nearby code, real callers, and relevant contracts. Inspect
storage, dependency boundaries, tests, or history only where they explain a
consequential decision. Identify the current behavior that must be preserved.

Separate evidence about evolution into:

- **Required now**: behavior and constraints the current task must satisfy.
- **Supported direction**: an explicit upcoming requirement, repeated changes,
  existing variants, or a limitation already visible in callers. State the
  source and uncertainty; an upcoming need is not automatically in scope now.
- **Possible only**: a future someone can imagine. This alone does not justify
  new interfaces, configuration, compatibility machinery, or implementations.

Do not invent a roadmap. Even when the next feature is unknown, existing
commitments such as durable data and public APIs have observable costs.

### 2. Trace the Cost of Changing the Decision

Choose the few decisions that matter in this change. For each, ask:

- Where does the assumption live, and who relies on it? Can a maintainer find
  its owner and invariant without reconstructing unrelated code?
- If it changes, is the edit local, or must multiple callers, teams, data
  formats, or independently released components move together? Trace the
  actual dependency that causes the spread.
- Can the implementation be replaced or deleted without changing its callers?
  Does a private detail escape into a public contract or persistent format?
- Would the change require migration, coordinated release, or compatibility
  support? Distinguish a cheap private refactor from a lasting commitment.
- Can the intended behavior be verified without freezing implementation
  details? Missing evidence limits confidence; it does not license a rewrite.

Use a small change scenario when it exposes the mechanism: for example, changing
one existing business rule or replacing the dependency whose types are already
exposed. Label an unsupported scenario as hypothetical and do not turn it into
a requirement. No exhaustive catalogue of possible futures is needed.

### 3. Compare Acting Now with Waiting

Consider keeping the implementation, making a small local adjustment, and
deferring a larger change. Compare them in plain language:

- What must readers and maintainers pay for immediately: concepts, indirection,
  dependencies, configuration, tests, and ongoing compatibility?
- What specific change becomes cheaper, and what evidence makes that relevant?
- What becomes harder if we wait: more consumers, more durable data, repeated
  coordination, or a contract that becomes difficult to retract?
- What can we learn by waiting, and can the decision still be changed locally
  when that information arrives?

Prefer a minimal complete implementation that expresses the problem faithfully
and keeps incidental assumptions contained. First look for a better expression
of the existing concept, responsibility, or dependency; an improvement need not
add code. Do not assume the choice is between terse code now and more structure
for the future.

A concrete private implementation can be easy to replace without an interface.
A small boundary or clearer ownership can be justified by today's coupling even
without a second implementation. A new abstraction earns its cost only when
its responsibility is clear and the benefit outweighs maintaining it now.

Do not equate fewer lines with lower debt, duplication with a shared concept,
more layers with flexibility, or a possible future rewrite with present failure.
Never weaken required behavior to obtain a simpler shape.

### 4. Choose an Action and Its Limit

- **Keep it** when change remains local and a more elaborate design buys little.
  A review with no maintenance findings is a valid outcome.
- **Adjust now** when a bounded change prevents a demonstrated maintenance cost
  or contains a commitment that is expensive to undo. Name the smallest useful
  edit and what it costs; do not implement hypothetical future features.
- **Defer deliberately** when more information is worth more than preparation.
  For material accepted debt, name its local boundary, consequence, and an
  observable reason to revisit it, such as another consumer or a planned format
  change. Do not invent deadlines or add TODOs for every imaginable future.

Delivery pressure may justify debt, but name the tradeoff and check that the
shortcut is contained. A smaller diff is not inherently cheaper over the
software's lifetime. Conversely, do not expand a feature into a repository-wide
cleanup: report necessary follow-up separately when it exceeds the task.

## Show the Reasoning

During implementation, express the judgment in the code and mention only
material tradeoffs. In a design discussion or review, lead with the recommended
action. For each material finding, give:

1. The location and observed assumption or coupling.
2. The kind of change affected, its evidence, and how the cost spreads.
3. The smallest useful action, its present cost, and why waiting is better or
   worse. State what new information would change the recommendation.

Prioritize by consequence, spread, and difficulty of reversal. Keep established
problems, conditional risks, and preferences distinct; do not inflate a
hypothetical risk into a blocking defect or manufacture findings to fill a list.
Avoid scores without evidence and phrases such as "not scalable" or "not
future-proof" without a concrete mechanism.

For calibration, read [contrasting cases](references/contrasting-cases.md).
They show how different evidence changes the recommendation, not patterns to
apply mechanically.

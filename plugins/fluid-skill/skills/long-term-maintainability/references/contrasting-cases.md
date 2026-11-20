# Contrasting Cases

These are synthetic examples of judgment, not mandatory designs. Change the
evidence and the recommendation may change with it.

## Equally Small, Different Meaning

A cart's empty state means that it contains no items. Today's catalog has only
positive prices and no discounts, so both implementations produce the required
result:

```javascript
function isEmpty(cart) {
  return cart.total === 0;
}
```

```javascript
function isEmpty(cart) {
  return cart.items.length === 0;
}
```

**Use the item count.** It expresses emptiness directly. The total-based version
relies on a coincidence between price and presence; it makes the meaning of
"empty" depend on pricing policy. The second version is just as minimal, but
its choice of concept makes it remain meaningful as pricing evolves.

A free item or a discount illustrates how the first version could need an
exception. Neither is a promised feature or a reason to build pricing machinery
now. The present definition of emptiness already justifies the choice. If the
actual question were whether payment is due, the total could be appropriate:
name and implement that different responsibility accordingly.

## One Dependency, No Evidence of Another

A private service calls one provider. Provider-specific values stay inside the
service, callers receive the values they need, and the service has one clear
owner. Someone proposes a provider interface and registry because another
provider might be needed someday.

**Keep the concrete service.** Replacing it is already a local operation. The
interface and registry add concepts now without reducing a demonstrated change
cost. Reconsider when a real second provider, a useful test double, or an
external extension contract establishes the required variation. Even then,
choose the mechanism that represents that variation, not an assumed framework.

If provider SDK types instead escape through several feature APIs, the
recommendation changes: inspect whether those features intentionally need the
provider's semantics. If not, translate the required values at the existing
boundary so provider changes stop spreading through unrelated features. That
translation has a maintenance cost too; avoid a mirror model for every SDK type.
No provider registry is needed to contain this current coupling.

## Similar Code with Different Reasons to Change

Two screens format labels similarly, but one follows editorial rules and the
other displays contractual wording. A shared formatter would need flags for
their different policies.

**Keep the policies separate.** Their resemblance does not establish a common
responsibility. Sharing them would couple changes that should be independent.
Reconsider if the product establishes one policy that should change both.

If two purchase paths instead duplicate the same eligibility rule, and the
requirement says both must always agree, a local shared policy is justified
now. It prevents one real rule from acquiring two authorities; it does not
require a configurable rules engine. Verify the agreed behavior through the
affected paths rather than asserting the helper's internal shape.

## A Small Implementation That Makes a Lasting Promise

A document stores a display label as an object's identity. Labels are currently
unique, but users can already rename them, and references survive across saves.
Using the label is short and passes a create-and-open example.

**Adjust the identity boundary now.** Rename behavior and durable references
already require identity independent of presentation. Use a stable identity and
keep the label as display data. The cost is a separate value and its handling;
waiting allows more documents to depend on the conflated meaning. If documents
already exist, account for their migration rather than silently changing their
interpretation. This also reveals a current correctness issue, which takes
priority over the maintenance finding.

Contrast a private, short-lived lookup whose labels cannot change during its
lifetime and never escape into storage or callers. The same representation can
be adequate there. Do not demand durable identifiers merely because the other
case needed them; revisit if the lookup's lifetime or contract changes.

## Deadline Pressure and Contained Debt

A delivery deadline requires supporting one legacy response shape. A private
decoder can translate it into the application's existing model, while a broad
compatibility framework would delay delivery. Several screens could also each
special-case the legacy response with slightly fewer lines initially.

**Keep the workaround at the decoder.** The legacy shape has one boundary and
can be removed there; spreading it through screens makes eventual removal a
coordinated task. Record the reason for the translation and the observable
removal condition: the supported server versions no longer emit that shape.
Avoid a general framework until actual compatibility requirements justify it.

For a throwaway import script with no retained consumers or outputs that rely
on its internal representation, inline handling may instead be appropriate.
Confirm that disposal assumption. If it becomes a recurring production job,
revisit ownership and verification based on that new use, not on a prediction
that every script inevitably becomes a product.

---
name: wayfinder
description: "把目标模糊或跨多个阶段的大工作拆成有依赖的真实决策与行动，维护共享 tracker 或本地地图，并持续推进直到目标可交付或遇到真实阻塞。"
disable-model-invocation: true
---

A broad goal has unresolved questions, dependencies, or manual prerequisites. Wayfinding makes the path visible and keeps moving toward the **destination**. It can use a shared tracker or a local map; work the ready questions in dependency order and continue across multiple tickets or sessions as needed. Planning is the default, while implementation can be included when the user asks for it.

The destination varies per effort, and naming it is the first act of charting: it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic: engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear, with nothing left to decide before someone goes and does the thing. The pull to do implementation is a scope boundary: record the decision and hand off the implementation unless the user explicitly includes execution in this effort. Keep planning useful by resolving the real prerequisite questions and refreshing the map as evidence arrives; do not stop merely because one ticket or one session ended.

## Refer by name

Give every map and question a descriptive title. In narration and summaries, use that title; include a tracker id or local slug as a locator when useful. A short title helps people recognize the decision without opening its detail.

## The Map

When a shared issue tracker is authorized and available, the map is one issue labelled `wayfinder:map`, and its tickets are children. Otherwise, the same map structure can live in a local Markdown file or in the conversation; do not make tracker setup a prerequisite.

The map is an **index**, not a duplicate store. It summarizes the destination, current frontier, dependency edges, decisions and unknowns. Each decision has one canonical detail record; map summaries point to it or link to it.

The map and its tickets may live in an issue tracker or local Markdown workspace. Use the tracker the user names or the one already configured in the project. Do not require a particular setup skill or issue-tracker file. If tracker access is missing, create a local draft map when that fits the request, or present the next decisions without writing externally. Before changing a shared tracker, check that the user asked for that change; when authorization is unclear, prepare the exact changes for review first.

### The map body

Load the map summary first. In a tracker, query tickets as needed instead of loading every body. In a local Markdown map, keep a compact ticket index with status and blockers so the frontier remains visible.

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain, relevant references, constraints, standing preferences, and useful context pointers>

## Decisions so far

<!-- one line per decided question, with a link or path to its evidence -->

- [<decision title>](link or path): <one-line gist of the answer>

## Not yet specified

<!-- in-scope questions that are not yet precise enough to act on -->

## Tickets

<!-- id/title | type | status/owner | blockers | canonical detail path or URL -->

## Out of scope

<!-- work ruled beyond the destination, with reason and prior record if any -->
```

### Tickets

Each ticket is a focused question or prerequisite. A tracker ticket uses its issue id; a local ticket uses a stable slug recorded in the map. Size it to the evidence needed, not an assumed agent token limit:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

A tracker ticket may carry a `wayfinder:<type>` label; a local ticket can use the same type field. Choose among `research`, `prototype`, `grilling`, and `task` when the distinction helps collaborators. These labels are organizational metadata, not a requirement to invoke a named skill.

When several sessions may change a shared tracker, claim a ticket before work if the tracker supports a clear owner/status field and the user authorized that write. A local map can use `status: in-progress` and an owner when concurrency is real. With one writer, no claim field, or no authorization, proceed from the local task context without inventing a write.

Use native dependency links when the chosen tracker supports them. Otherwise record `blocked_by` links in ticket bodies or the local index. A question is **ready** when all prerequisite decisions and manual prerequisites are resolved; the **frontier** is the set of ready questions not already in progress. Keep dependencies explicit even if the user works sequentially.

Record the resolution, evidence and remaining uncertainty in the ticket detail or local note. Put large artifacts in an appropriate workspace and link them instead of duplicating them in the map.

## Ticket Types

Every ticket is either **HITL** (human in the loop, worked _with_ a human who speaks for themselves) or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research**: gather a factual answer from primary sources or project files. Delegate only when an agent is available and parallel reading will help; otherwise research directly. Record citations, date and limits.
- **Prototype**: build a small, runnable artifact when direct observation will clarify behavior or appearance. Completion is the prototype plus question, observed evidence and limits; production implementation is a separate scope.
- **Grilling**: use a focused human discussion when the answer is a user decision. Ask only the next questions whose prerequisites are clear; do not force a fixed number of skill calls.
- **Task**: complete or prepare a prerequisite that blocks a decision, such as importing a sample or checking a service. Do reversible local preparation directly. For account creation, external writes, costs, or manual access, prepare concrete steps and wait for the required user authorization or input.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war**: the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets, as prerequisites become clear until the destination is reached or all remaining questions are genuinely blocked.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination: everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now, _not_ whether you can answer it now.

- **Ticket when** the question is already sharp, even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope**: it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates (the frontier stops at the destination), so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a question sits past the destination, mark it out of scope with a reason. Close a tracker ticket only when the user authorized the tracker change; otherwise prepare the closure note. Keep the historical record and do not list it as a decision reached.

## Invocation

There are two modes. Choose the mode from the user's request; do not make the map artificially small. Continue toward the stated destination while the next decision is clear, authorized, and useful. Stop or hand off when the destination is reached, a decision truly needs the user or an outside event, the user asks to stop, or the available context/tools make reliable progress impossible. A single session may resolve several independent tickets. Several sessions may work separate unclaimed frontier tickets when real capacity and isolated context are available; sequential work is fine when they are not.

### Chart the map

Use this when the goal is broad enough that its decisions and sequence are not yet clear.

1. **Name the destination.** Reuse the goal already stated. Ask only for a missing choice that changes the destination or scope. Gather facts from files and available tools yourself; do not turn factual research into a user question.
2. **Map decisions breadth-first.** Identify what must be decided or learned before the goal can be delivered, which questions depend on each other, and which are genuinely unknown. Put crisp, answerable questions in the first decision frontier; keep dependent and not-yet-specific questions in `Not yet specified`.
3. **Choose a useful artifact.** If a shared tracker map was requested and access is available, create or update it and its tickets. Otherwise keep a local Markdown map or present the map in the conversation. Do not create external issues, assign people, or add labels without authorization for those changes.
4. **Wire dependencies after identifiers exist.** Use native tracker links when available. In a local map, record explicit blockers and the reason. Avoid duplicate tickets and keep the map an index: each decision's evidence and detail belong in one place.
5. **Resolve independent research when practical.** Use available research delegation only when it saves time and a real agent is available. Otherwise investigate directly. Save cited findings at the project's normal research location, or state where the user can find the result.
6. **Continue into the next useful frontier when the user asked for ongoing planning.** A chart-only request ends with the map, first actionable questions, dependencies, and uncertainty. Do not force a pause if the user asked you to continue.

### Work through the map

The user may provide a map, a decision ticket, or just the destination. A named ticket is a priority; without one, choose the most useful unblocked question.

1. Load the destination and the map summary first. Read full ticket details only for the selected question and its relevant dependencies. Check for parallel edits before changing shared state.
2. Select the next decision by dependency and impact. Claim or assign it only when the tracker supports that action and the user has authorized tracker updates. A local plan can mark it in progress without external mutation.
3. Resolve it using the smallest effective method: inspect project sources, do focused research, make a throwaway prototype, or discuss a decision with the user. Use domain-modeling or grilling only when the terminology or human decision is genuinely unclear; neither is a mandatory ritual.
4. Record the evidence, decision, owner, and remaining uncertainty. Update the ticket and map only within the user's authorization; otherwise prepare the exact text locally for review. Do not close or delete tickets automatically.
5. Recompute the frontier. Add a new ticket only for a specific in-scope question that became answerable; keep vague future questions in `Not yet specified`. Remove stale dependencies carefully and record why. If a question falls outside the destination, mark it out of scope in the map; do not silently erase history.
6. Continue with another ready question if it advances the real goal and no human or external blocker remains. Stop at a true decision gate and state exactly what input or event is needed to proceed.

## Completion

The map is complete when the user's stated planning destination is clear: required decisions have evidence and owners, unresolved dependencies are explicit, and the next execution step can be handed off. A large project may still need implementation; do not call that implementation complete. Report the destination, decisions reached, open questions, next action, and any tracker updates actually made.

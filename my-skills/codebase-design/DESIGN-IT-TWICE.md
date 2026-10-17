# Design It Twice

When alternative interfaces could change a design decision, compare at least two distinct shapes before settling on one. This can be done inline. Use parallel agents only when they are available, independent, and likely to improve the comparison; do not make a fixed agent count or tool call a prerequisite.

Uses the vocabulary in [SKILL.md](SKILL.md): **module**, **interface**, **seam**, **adapter**, **leverage**.

## Process

### 1. Frame the problem space

Frame the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- A rough illustrative code sketch to ground the constraints, not a proposal, just a way to make the constraints concrete

Share the concise framing when the user is participating in the design, then proceed with available exploration. Comparing reversible options does not require a separate approval.

### 2. Generate alternative shapes

Produce two or more meaningfully different interfaces. If suitable agents are available, parallelize independent alternatives; otherwise derive them from different constraints such as smallest caller surface, strongest locality, or easiest migration.

For each alternative, record the relevant files, coupling, dependency category from [DEEPENING.md](DEEPENING.md), what sits behind the seam, and the design constraint used:

- Agent 1: "Minimize the interface: aim for 1–3 entry points max. Maximise leverage per entry point."
- Agent 2: "Maximise flexibility: support many use cases and extension."
- Agent 3: "Optimise for the most common caller: make the default case trivial."
- Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

Include both [SKILL.md](SKILL.md) vocabulary and GLOSSARY.md vocabulary in the brief so each sub-agent names things consistently with the architecture language and the project's domain language.

Each sub-agent outputs:

1. Interface (types, methods, params, plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters (see [DEEPENING.md](DEEPENING.md))
5. Trade-offs: where leverage is high, where it's thin

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated: the user wants a strong read, not a menu.

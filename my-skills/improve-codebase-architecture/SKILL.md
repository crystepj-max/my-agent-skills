---
name: improve-codebase-architecture
description: "审阅代码库架构，提出有证据的模块深化候选并协助打磨设计；仅在用户明确要求实施且目标与范围足够明确时实施。"
disable-model-invocation: true
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Use the bundled [codebase-design](../codebase-design/SKILL.md) vocabulary where it clarifies the analysis: **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, and **locality**. Follow the project's own names when they are more precise; the vocabulary is a lens, not a naming restriction.
- The domain language in `GLOSSARY.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Explore

**Scope before you scan: YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction (a module, a subsystem, a pain point), take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots, the files and areas that keep coming up, and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

Read the project's domain glossary (`GLOSSARY.md`) and any ADRs in the area you're touching first.

Inspect the codebase directly. Honor an explicit request to delegate; otherwise delegate independent exploration when the scope and likely time or quality savings justify it. Don't follow rigid heuristics; explore organically and note evidence of friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present findings in a format that fits the review

Choose the output for the question being answered. For several competing candidates, create a self-contained HTML report in the OS temp directory; for a focused review, a concise Markdown or chat report with file paths or code examples may be clearer. Use a fresh filename, avoid overwriting user files, and open the artifact only when a local viewer is available. Report its absolute path.

If an HTML report is useful, use the retained [HTML-REPORT.md](HTML-REPORT.md) patterns selectively. Diagrams should explain the specific code relationships; do not require a visual for a candidate when file paths and examples are clearer.

For each candidate, render a card with:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Constraints and verification**: applicable constraints, dependencies, interface/seam implications, and the test surface that can verify the design
- **Benefits**: explained in terms of locality and leverage, and how tests would improve
- **Before / After comparison**: use a side-by-side diagram when it makes the current friction and proposed deepening easier to compare; for a focused issue, a concise code or call-path example may be clearer. When comparing alternatives, keep a comparable before/after view rather than dropping it for brevity.
- **Recommendation strength**: one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

Analyze applicable constraints, dependencies, interfaces/seams, and test surface for every candidate, whether or not a question for the user is needed. The grilling loop resolves decisions that depend on user intent; it does not replace this analysis.

Prefer the project's established domain terms and accurate code names. Use `GLOSSARY.md` and `/codebase-design` vocabulary when it clarifies the explanation, but do not impose a vocabulary list as a naming restriction or replace a real project term with a generic architecture label.

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts ADR-0007, but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full HTML scaffold, diagram patterns, and styling guidance.

For an exploratory request, recommend the best-supported bounded candidate and show meaningful alternatives; invite the user to choose only when the choice materially changes scope. Implement only when the user explicitly asks for implementation and the target and scope are sufficiently clear. Then carry out the confirmed design without asking again for the same approval, and update directly related documentation as part of that implementation. During review-only work, propose relevant glossary or ADR changes when useful, but do not edit those documents automatically.

### 3. Grilling loop

When a design choice is genuinely unresolved, use the [grilling](../grilling/SKILL.md) method inline to examine constraints, dependencies, module shape, the seam, and the tests that should survive. Ask only about the remaining decision that depends on the user's intent.

When the task includes changing domain documentation, use [domain-modeling](../domain-modeling/SKILL.md) inline to keep the domain model current:

- **Naming a deepened module after a concept not in `GLOSSARY.md`?** Propose or add the term according to the user's requested scope; create the file only when documentation changes are included.
- **Sharpening a fuzzy term during the conversation?** Record it when the task includes editing the glossary; otherwise include it as a proposed change.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing; skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Use [DESIGN-IT-TWICE.md](../codebase-design/DESIGN-IT-TWICE.md), comparing alternatives inline or with optional parallel agents.

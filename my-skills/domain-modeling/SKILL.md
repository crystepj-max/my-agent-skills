---
name: domain-modeling
description: "构建并打磨项目的领域模型。当用户要讨论代码库术语、编写或编辑 GLOSSARY.md、记录或编辑 ADR 时使用。"
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When a term appears to conflict with an existing glossary entry, show the conflict and its effect on the model. Continue with the interpretation supported by context when safe; ask the user only if choosing the meaning changes the design or decision.

### Sharpen fuzzy language

When a vague or overloaded term matters to the model, propose a precise candidate and explain the distinction. If the difference does not affect the current outcome, record the assumption instead of interrupting.

### Discuss concrete scenarios

When domain relationships are being discussed, test them against concrete scenarios, including an edge case when it could change a boundary or invariant. Use scenarios to clarify decisions rather than as a mandatory interview sequence.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When the task includes editing the domain model, update `GLOSSARY.md` as terms settle and use [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md). If the user asked only to discuss or review, present proposed glossary edits without writing them. Preserve the repository's existing structure and unrelated local changes.

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Offer or create an ADR only when the task includes recording decisions and all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).

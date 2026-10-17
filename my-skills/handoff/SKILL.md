---
name: handoff
description: "把当前对话压缩成一份交接文档，供另一个 agent 接手。"
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a concise handoff document so another agent can continue the requested work. Use the focus supplied in the arguments; if it is absent, infer the next useful action from the current task and its evidence. Save to the user's requested location, or to an OS temporary directory when no durable project location was requested. Do not overwrite an existing handoff without checking it first.

Include an optional "useful skills or references" section with the relevant skill names and why they may help. The next session may not expose a separate Skill tool, so include a short inline description or a direct file path when that is needed to continue.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Omit secrets such as API keys and passwords. Include only personal details that are necessary to continue the user's task; do not copy unrelated personal data into the handoff.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

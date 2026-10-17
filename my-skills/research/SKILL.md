---
name: research
description: "针对高可信一手来源调研某个问题，并把结论以 Markdown 文件存入仓库。当用户想调研某个主题、收集文档或 API 事实，或把繁琐的资料查阅交给后台 agent 时使用。"
---

Research the question against sources that own the relevant facts. Use a background agent only when the current environment supports it and parallel reading helps; otherwise do the work in the current session. Do not delay a useful answer waiting for an unavailable agent.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Cite each material claim near the source that supports it. Prefer official documentation, source code, specifications, and first-party APIs; distinguish an inference from a directly stated fact.
3. If the user requested a research artifact, write one Markdown report where the repo already keeps such notes; follow its convention, or choose a focused `docs/research/` path when none exists. For a question that asks only for an answer, respond with the findings and citations without creating an unsolicited file.
4. State the time-sensitive scope and what you could not verify. Do not claim a full survey when only a representative sample was checked.

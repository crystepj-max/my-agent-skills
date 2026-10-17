---
name: grilling
description: "就某个计划、决策或想法对用户穷追不舍地追问。当用户想压力测试自己的思路，或使用了任何『grill』触发词时使用。"
---

仅在用户明确要求压力测试或深度追问时进行，围绕本轮决定达到可行动的共同理解即结束。 Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question depends on facts available in the workspace or connected tools, inspect those sources first. Delegate independent fact-finding only when the current environment offers a suitable agent and it will save time; otherwise continue inline. Do not block on delegation: an unresolved fact is an unsettled prerequisite, so only questions downstream of it wait. Ask the user to decide only where their preference, product intent, or authorization is genuinely needed.

当前决定的关键问题已回答、剩余分支不影响本轮结果时结束，不扩展到所有潜在分支。给出结论、依据和仍未验证的假设；既有确认可复用，实质改变目标的部分才重新确认。

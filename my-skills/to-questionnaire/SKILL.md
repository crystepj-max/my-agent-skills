---
name: to-questionnaire
description: 把你无法完全独立回答的一个决策，转化为一份由他人填写的问卷。
disable-model-invocation: true
---

Turn information the user needs from someone else into a usable **questionnaire**: a Markdown document for an asynchronous reply or a meeting. The recipient holds facts or context the user needs to make a decision.

**Resolve only the information gap.** Use the request and surrounding context to infer the recipient's role and the decision the answers will support. Ask only for details that materially change the questions or how the answers will be used; combine missing details into one concise exchange. Do not ask the user to restate facts already available. The questionnaire itself targets the **gap** between what the recipient knows and what the user needs.


1. **Identify the audience.** Infer the recipient's role, expertise, and relationship from the task when possible. If a missing detail would materially change the framing, ask for it; otherwise use a neutral role-based label and mark it as an assumption.

2. **Identify the needed answers.** Convert the user's decision or next step into the specific facts, constraints, or recommendations the recipient can provide. Ask only if the target decision remains unclear after reading context.

3. **Write the questionnaire.** Draft questions aimed at the information gap, following the document structure below. Write it to `to-questionnaire-<slug>.md` in the requested output location; if none is specified, use the current project convention or current directory and report the path. Done when every needed answer has a clear, focused question and the recipient can understand how to respond.

Do not send the questionnaire or contact its recipient. Creating the document does not authorize an external message.

## Document structure

Frame the document as a **discovery questionnaire**: the user lacks context, the recipient holds it. Order questions most-important-first, since async means you may only get one pass, and group them under `##` headings by theme once there are more than a handful. Write it using the template below.

<questionnaire-template>

# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision riding on it.

**From:** <the user>, **To:** <the recipient>, **How your answers will be used:** <where they go>

## Context

One paragraph orienting a recipient who wasn't in the user's head. Enough to answer well, not a page.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful: flag anything you're unsure of rather than skipping it.

## <Theme heading>

One `##` section per theme. Under each, its questions, most-important-first. Every question is one idea, never compound, with an answer stub directly beneath, and a one-line _why this matters_ only where the question could be misread or invite a throwaway answer.

<question-example>
### What load is the system expected to handle at launch?

_Why this matters: it decides whether we provision for burst traffic now or defer it._

>
</question-example>

## Anything else?

A closing catch-all: anything we didn't ask that we should know?

</questionnaire-template>

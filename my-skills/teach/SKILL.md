---
name: teach
description: "在当前工作区内，教用户一项新技能或概念。"
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

The user has asked you to learn a topic with them. Keep the learning goal and practice loop in view. Treat this as a multi-session workspace only when the user names one or this directory already contains the teaching files; otherwise teach within the current request and do not create persistent files by default.

## Teaching Workspace

Use an existing, user-designated teaching workspace when one is clear. Do not assume that any current project directory is a teaching workspace. If none is designated, deliver the lesson in the conversation; create a durable workspace only when the user asks for one or has already established it:

- MISSION.md: In a designated teaching workspace, this captures the user's learning outcome. Use MISSION-FORMAT.md. In a one-off lesson, use the goal stated in the request rather than creating a file.
- `./reference/*.html`: A directory of reference materials. These are the compressed learnings from the lessons - cheat sheets, reference algorithms, syntax, yoga poses, glossaries. They are the raw units of learning. They should be beautiful documents which print out well, and are designed for quick reference.
- `RESOURCES.md`: A list of resources which can be explored to ground your teaching in contextual knowledge, or to acquire knowledge and wisdom. Use the format in [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- ./learning-records/*.md: In an established workspace, these can capture demonstrated understanding or user-disclosed prior knowledge for later lessons. Do not create or update them unless the user has asked to retain learning progress in that workspace. Use sequential names such as 0001-topic.md.
- `./lessons/*.html`: A directory of lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching in this workspace.
- `./assets/*`: Reusable **components** shared across lessons. See [Assets](#assets).
- NOTES.md: Use only for task notes needed in the current workspace. Do not store long-term teaching preferences unless the user asks to retain them.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Before the `RESOURCES.md` is well-populated, your focus should be to find high-quality resources which will help the user acquire knowledge. Never trust your parametric knowledge.

Some topics may require more skills than knowledge. Learning more about theoretical physics might be more knowledge-based. For yoga, more skills-based.

### Fluency vs Storage Strength

You should be careful to split between two types of learning:

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give the user an illusory sense of mastery, but storage strength is the real goal. Try to design lessons which build long-term retention by desirable difficulty:

- Using retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing up different but related topics in practice - for skills practice only)

## Lessons

A lesson is the main thing you produce: the unit in which knowledge and skills reach the user. Each lesson is one self-contained HTML file, saved to `./lessons/` and titled `0001-<dash-case-name>.html` where the number increments each time.

A lesson should be **beautiful**, with clean, readable typography and layout, since the user will return to these later to review. Think Tufte.

The lesson should be short, and completable very quickly. Learners' working memory is very small, and we need to stay within it. But each lesson should give the user a single tangible win that they can build on. It should be directly tied to the mission, and should be in the user's zone of proximal development.

When the lesson is a saved file, show or open it with the current host's available file-opening capability. Do not assume a particular CLI name.

Each lesson should link via HTML anchors to other lessons and reference documents.

Each lesson should recommend a relevant primary source when one is available. Prefer high-trust material and verify current or consequential claims with sources; do not invent a citation or present an unverified link as checked.

Each lesson should contain a reminder to ask followup questions to the agent. The agent is their teacher, and can assist with anything that's unclear.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`: stylesheets, quiz widgets, simulators, diagram helpers, and anything else a second lesson could reuse.

Reuse is the default, not the exception. Before authoring a lesson, read `./assets/` and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it; never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns: every lesson links it, so the lessons look like one consistent course rather than a pile of one-offs. As the workspace grows, so should the component library.

## The Mission

Every lesson should be tied into the mission - the reason that the user is interested in learning about the topic.

If a missing learning outcome would materially change what to teach, ask a focused question. When the user already named the topic and desired result, proceed with that as the task-specific mission; do not force an interview or require a persistent MISSION.md.

Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next.

A learner's goal may change. In a designated workspace, update its mission or learning record only when the user requested that persistent workspace maintenance; otherwise adapt the current lesson and mention any material goal change without writing durable state.

## Zone Of Proximal Development

Each lesson, the user should always feel as if they are being challenged 'just enough'.

The user may specify the exact thing they want to learn. If so, teach that goal directly and use existing records only to tune the level. If the goal is open-ended, estimate the zone of proximal development from:

- Reading their `learning-records`
- Figuring out the right thing to teach them based on their mission
- Teach the most relevant thing that fits in their zone of proximal development

## Knowledge

Lessons should be designed around a skill the user is going to learn. The knowledge in the lesson should be only what's required to acquire that skill. You teach the knowledge first, then get the user to practice the skills via an interactive feedback loop.

Knowledge should first be gathered from trusted resources. Use `RESOURCES.md` to keep track of them. Lessons should be littered with citations - links to external resources to back up any claim made. This increases the trustworthiness of the lesson.

For acquiring knowledge, difficulty is the enemy. It eats working memory you need for understanding.

## Skills

If knowledge is all about acquisition, skills are about durability and flexibility. Make the knowledge stick.

For skill acquisition, difficulty is the tool. Effortful retrieval is what builds storage strength. Skills should be taught through interactive lessons. There are several tools at your disposal:

- Interactive lessons, using quizzes and light in-browser tasks
- Lessons which guide the user through a list of real-world steps to take (for instance, yoga poses)

Each of these should be based on a **feedback loop**, where the user receives feedback on their performance. This feedback loop should be as tight as possible, giving feedback immediately - and ideally automatically.

For quizzes, each answer should be exactly the same number of words (and characters, if possible). Don't give the user any clues about the answer through formatting.

## Acquiring Wisdom

Wisdom comes from true real-world interaction - testing your skills outside the learning environment.

When the user asks a question that appears to require wisdom, try to answer within the available evidence and point to an appropriate community or practitioner when real-world experience matters. Do not post, join, or contact anyone on the user's behalf without explicit authorization.

A community is a place (online or offline) where the user can test their skills in the real world. This might be a forum, a subreddit, a real-world class (budget permitting) or a local interest group.

You should attempt to find high-reputation communities the user can join. If the user expresses a preference that they don't want to join a community, respect it.

## Reference Documents

While creating lessons, you should also create reference documents. Lessons can reference these documents - they are useful for tracking raw units of knowledge useful across lessons.

Lessons will rarely be revisited later - reference documents will be. They should be the compressed essence of the lesson, in a format designed for quick reference.

Some learning topics lend themselves to reference:

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Yoga poses and sequences for yoga
- Exercises and routines for fitness
- Glossaries for any topic with its own nomenclature

Glossaries, in particular, are an essential reference. Once one is created, it should be adhered to in every lesson.

## NOTES.md

Use this only for short-lived task notes inside an established teaching workspace. Save enduring preferences or personal learning history only when the user asks for that persistence.

## Interactive completion

A lesson is not complete merely because its HTML or explanation was written. End with one focused recall question or exercise tied to the user's goal, invite the learner to answer, and wait for their response before grading or recording demonstrated understanding. Give feedback against the actual answer, then offer the next practice step. Never fabricate the learner's answer or claim mastery from exposure alone.

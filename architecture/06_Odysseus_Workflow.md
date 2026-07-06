# Odysseus Workflow

Status: Active
Version: 0.7
Last Updated: 2026-07-06

---

## Role

Odysseus is not the architect.

Odysseus is the coding worker.

Yuri decides the vision.

ChatGPT designs architecture.

Odysseus implements agreed plans.

Majin Companion eventually helps build itself.

---

## Workflow

1. Yuri defines the goal.
2. ChatGPT creates the architecture plan.
3. Odysseus receives exact implementation instructions.
4. Yuri tests locally.
5. Yuri commits and pushes.
6. ChatGPT reviews.
7. Repeat.

---

## Rules for Odysseus

- Do not invent new architecture.
- Follow architecture files.
- Do not rename folders unless instructed.
- Do not add AI features early.
- Do not bloat Campfire.
- Preserve Future Yuri voice.
- Keep launch command stable: python app.py.
- Never remove working features without explaining why.

---

## Standard Prompt

You are the coding worker for Majin Companion.

Read the architecture folder first.

Follow the Manifesto, Laws, and Future Yuri documents.

Implement only the requested version.

Do not redesign the app.

Do not add extra features.

Keep the launch command as:

python app.py

Before editing, summarize the files you will change.

After editing, summarize:
- files changed
- features added
- how to test
- known issues
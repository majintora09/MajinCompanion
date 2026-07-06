# Refactor Plan

Status: Active
Version: 0.7
Last Updated: 2026-07-06

---

## Goal

Clean the codebase before building v0.8.

No more god files.

No more random feature folders.

Every system owns its own code.

---

## Target Structure

app.py

architecture/

campfire/
- screen.py
- hero.py
- continue_card.py
- thought.py
- mission.py
- workshop_summary.py

workshop/
- screen.py
- place_card.py

places/
- registry.py
- place.py

brains/
- brain.py
- screen.py

sessions/
- session.py
- screen.py

dreams/
- dreams.py
- screen.py

goals/
- goals.py
- screen.py

activity/
- activity.py
- screen.py

future/
- personality.py
- capabilities.py
- prompts.py

ui/
- card.py
- button.py
- background.py

themes/
- colors.py
- spacing.py
- typography.py

data/
- memory files
- active session
- project brains

---

## Refactor Rules

1. app.py only launches the app.
2. No UI inside core logic.
3. No business logic inside UI components.
4. Campfire stays minimal.
5. Workshop lists Places.
6. Brains store Place memory.
7. Sessions capture context.
8. Future Yuri is prepared, not implemented yet.
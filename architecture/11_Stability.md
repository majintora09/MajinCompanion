# Stability

Status: Active
Version: 0.9.1
Last Updated: 2026-07-06

---

## Purpose

Majin Companion should feel safe to build on.

Every version must keep the app launchable.

---

## Rules

1. `python app.py` must always work.
2. Window size should not reset during navigation.
3. Unsupported Flet APIs must not be used.
4. Every new screen needs a simple test path.
5. Every version must be committed before the next one starts.
6. If the app breaks, stability comes before new features.

---

## Test Checklist

Before committing:

- App launches.
- Campfire opens.
- Workshop opens.
- Workbench opens.
- Brain opens.
- Session starts.
- Notes save.
- Dreams save.
- Folder button works.
- Website button works.
- GitHub button works.
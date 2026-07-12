import re
from pathlib import Path

from projects.registry import PROJECTS


IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".idea",
    ".vs",
    ".vscode",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "vendor",
    "build",
    "dist",
    ".next",
    ".nuxt",
    "coverage",
    "storage",
    "public/build",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".vue",
    ".php",
    ".html",
    ".css",
    ".scss",
    ".sass",
    ".json",
    ".md",
    ".yml",
    ".yaml",
    ".toml",
}

IMPORTANT_FILENAMES = {
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "composer.json",
    "vite.config.js",
    "vite.config.ts",
    "next.config.js",
    "next.config.mjs",
    "README.md",
}

MAX_FILE_SIZE = 180_000
MAX_SELECTED_FILES = 10
MAX_TOTAL_CHARACTERS = 50_000


def get_project(project_id: str):
    return next(
        (project for project in PROJECTS if project["id"] == project_id),
        None,
    )


def get_project_root(project_id: str) -> Path | None:
    project = get_project(project_id)

    if not project:
        return None

    root = Path(project["path"])

    if not root.exists() or not root.is_dir():
        return None

    return root


def collect_source_files(project_id: str) -> list[Path]:
    root = get_project_root(project_id)

    if not root:
        return []

    files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(root)

        if should_ignore(relative):
            continue

        if not is_supported_file(path):
            continue

        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                continue
        except OSError:
            continue

        files.append(path)

    return files


def should_ignore(relative_path: Path) -> bool:
    parts = relative_path.parts

    for index, part in enumerate(parts):
        if part in IGNORED_DIRECTORIES:
            return True

        joined = "/".join(parts[: index + 1])

        if joined in IGNORED_DIRECTORIES:
            return True

    return False


def is_supported_file(path: Path) -> bool:
    if path.name in IMPORTANT_FILENAMES:
        return True

    return path.suffix.lower() in ALLOWED_EXTENSIONS


def request_keywords(request: str) -> set[str]:
    ignored = {
        "a",
        "an",
        "and",
        "are",
        "be",
        "for",
        "from",
        "have",
        "i",
        "in",
        "is",
        "it",
        "make",
        "of",
        "on",
        "or",
        "so",
        "that",
        "the",
        "this",
        "to",
        "with",
        "you",
    }

    words = re.findall(r"[a-zA-Z0-9_-]{3,}", request.lower())

    return {
        word
        for word in words
        if word not in ignored
    }


def score_file(
    path: Path,
    root: Path,
    keywords: set[str],
) -> tuple[int, str]:
    relative = path.relative_to(root).as_posix()
    relative_lower = relative.lower()
    score = 0

    if path.name in IMPORTANT_FILENAMES:
        score += 8

    for keyword in keywords:
        if keyword in relative_lower:
            score += 12

    try:
        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except OSError:
        return score, ""

    content_lower = content.lower()

    for keyword in keywords:
        occurrences = content_lower.count(keyword)
        score += min(occurrences, 8)

    mobile_terms = {
        "mobile",
        "responsive",
        "fighter",
        "character",
        "picker",
        "select",
        "roster",
        "team",
        "slot",
        "modal",
    }

    if keywords.intersection(mobile_terms):
        for term in mobile_terms:
            if term in relative_lower:
                score += 4
            if term in content_lower:
                score += 2

    return score, content


def build_repository_context(
    project_id: str,
    request: str,
) -> str:
    root = get_project_root(project_id)

    if not root:
        return (
            "Repository unavailable.\n"
            "The selected Place folder does not exist or cannot be read."
        )

    files = collect_source_files(project_id)

    if not files:
        return (
            f"Repository root: {root}\n\n"
            "No supported source files were found."
        )

    keywords = request_keywords(request)
    scored_files = []

    for path in files:
        score, content = score_file(path, root, keywords)

        scored_files.append(
            {
                "path": path,
                "score": score,
                "content": content,
            }
        )

    scored_files.sort(
        key=lambda item: (
            item["score"],
            -len(item["path"].parts),
        ),
        reverse=True,
    )

    selected = scored_files[:MAX_SELECTED_FILES]
    sections = [
        f"Repository root: {root}",
        f"Supported files found: {len(files)}",
        (
            "Files below were selected automatically based on the "
            "request and repository structure."
        ),
    ]

    total_characters = 0

    for item in selected:
        relative = item["path"].relative_to(root).as_posix()
        content = item["content"]

        remaining = MAX_TOTAL_CHARACTERS - total_characters

        if remaining <= 0:
            break

        if len(content) > remaining:
            content = (
                content[:remaining]
                + "\n[File content truncated by Builder Preview.]"
            )

        sections.append(
            "\n"
            f"===== FILE: {relative} =====\n"
            f"{content}"
        )

        total_characters += len(content)

    return "\n".join(sections)
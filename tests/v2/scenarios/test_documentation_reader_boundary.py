from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[3]


USER_DOC_FORBIDDEN_PATTERNS = [
    re.compile(r"\bADR(?:-\d+)?\b", re.IGNORECASE),
    re.compile(r"\bv2/v3\b", re.IGNORECASE),
    re.compile(r"\bv[23]\b", re.IGNORECASE),
    re.compile(r"Docs/dev(?:/|$)", re.IGNORECASE),
    re.compile(r"Docs/(?:EN|ZH|JP)/Developer(?:/|$)", re.IGNORECASE),
    re.compile(r"tests/v[0-9]", re.IGNORECASE),
]

NON_DEV_DOC_FORBIDDEN_PATTERNS = [
    re.compile(r"\bADR(?:-\d+)?\b", re.IGNORECASE),
    re.compile(r"Docs/dev(?:/|$)", re.IGNORECASE),
    re.compile(r"tests/v[0-9]", re.IGNORECASE),
]


def test_user_docs_do_not_expose_development_stage_material() -> None:
    for user_docs in sorted((REPO_ROOT / "Docs").glob("*/User")):
        for path in sorted(user_docs.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for pattern in USER_DOC_FORBIDDEN_PATTERNS:
                assert not pattern.search(text), f"{path.relative_to(REPO_ROOT)} contains {pattern.pattern}"


def test_non_dev_docs_do_not_reference_adr_or_versioned_test_paths() -> None:
    for path in sorted((REPO_ROOT / "Docs").rglob("*.md")):
        if (REPO_ROOT / "Docs" / "dev") in path.parents:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in NON_DEV_DOC_FORBIDDEN_PATTERNS:
            assert not pattern.search(text), f"{path.relative_to(REPO_ROOT)} contains {pattern.pattern}"

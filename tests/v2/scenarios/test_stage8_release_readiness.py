from pathlib import Path

import tomllib


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_release_tooling_is_configured() -> None:
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dev_deps = set(pyproject["project"]["optional-dependencies"]["dev"])

    assert any(dep.startswith("ruff") for dep in dev_deps)
    assert any(dep.startswith("mypy") for dep in dev_deps)
    assert "ruff" in pyproject["tool"]
    assert "mypy" in pyproject["tool"]


def test_no_generated_artifacts_are_present() -> None:
    forbidden_names = {"__pycache__", ".pytest_cache", "build", "dist"}
    forbidden_suffixes = {".egg-info"}

    for path in REPO_ROOT.rglob("*"):
        if any(part in forbidden_names for part in path.parts):
            raise AssertionError(f"generated artifact present: {path}")
        if any(str(path).endswith(suffix) for suffix in forbidden_suffixes):
            raise AssertionError(f"generated artifact present: {path}")


def test_no_oversized_text_files() -> None:
    max_size = 250_000
    suffixes = {".md", ".py", ".toml", ".txt", ".json"}

    for path in REPO_ROOT.rglob("*"):
        if path.is_file() and path.suffix in suffixes:
            assert path.stat().st_size <= max_size, str(path)

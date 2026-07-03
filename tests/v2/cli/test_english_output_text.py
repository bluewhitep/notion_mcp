import ast
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[3]
CJK_PATTERN = re.compile(r"[\u3400-\u9fff]")


def test_python_source_string_literals_are_english_only() -> None:
    offenders: list[str] = []
    for source_file in sorted((REPO_ROOT / "src" / "nilo").rglob("*.py")):
        module = ast.parse(source_file.read_text(encoding="utf-8"), filename=str(source_file))
        for node in ast.walk(module):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and CJK_PATTERN.search(node.value):
                rel_path = source_file.relative_to(REPO_ROOT)
                offenders.append(f"{rel_path}:{node.lineno}: {node.value}")

    assert offenders == []

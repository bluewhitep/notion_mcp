import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_isolated_install_cli_and_mcp_help() -> None:
    commands = [
        ["nilo", "--help"],
        ["nilo", "server", "stdio", "--help"],
        ["nilo", "server", "run", "--help"],
    ]

    for command in commands:
        result = subprocess.run(
            [
                "uv",
                "run",
                "--no-project",
                "--with",
                str(REPO_ROOT),
                *command,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr

import re


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def plain_cli_output(output: str) -> str:
    return ANSI_ESCAPE_RE.sub("", output)

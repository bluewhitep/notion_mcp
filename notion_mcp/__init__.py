# Local development compatibility shim.
#
# The installable package now lives under src/notion_mcp. This top-level package
# remains only so legacy tests that put the repository root on sys.path can still
# import notion_mcp without modifying existing test files.

from importlib import metadata
from pathlib import Path

_SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "notion_mcp"
if _SRC_PACKAGE.exists():
    __path__.append(str(_SRC_PACKAGE))

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    # Package is not installed; fallback for local development
    __version__ = "0.0.0"

__all__ = ["__version__"]

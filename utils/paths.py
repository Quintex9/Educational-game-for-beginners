import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """
    Return absolute path to an app resource for both:
    - source run (python main.py)
    - PyInstaller build (.exe, one-dir / one-file)
    """
    if getattr(sys, "frozen", False):
        base_path = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    else:
        # project root (parent of utils/)
        base_path = Path(__file__).resolve().parent.parent
    return str(base_path / relative_path)


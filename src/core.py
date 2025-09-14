import os
from typing import Iterable

DEFAULT_INDENT = 2  # spaces per level

def _leading_ws_count(s: str) -> int:
    """Count leading spaces after expanding tabs to two spaces."""
    expanded = s.replace("\t", "  ")
    return len(expanded) - len(expanded.lstrip(" "))

def _iter_structure_lines(text: str, comment_prefix: str = "#") -> Iterable[str]:
    """
    Yield non-empty, non-comment lines.
    A line is ignored if, after stripping leading spaces, it starts with comment_prefix.
    """
    for raw in text.splitlines():
        if not raw.strip():
            continue
        # Ignore full-line comments (allow indentation before '#')
        if raw.lstrip().startswith(comment_prefix):
            continue
        yield raw.rstrip("\n\r")

def create_structure_from_text(
    structure_text: str,
    base_dir: str = ".",
    indent_size: int = DEFAULT_INDENT,
    comment_prefix: str = "#",
) -> None:
    """
    Build directories/files from a tree-like text.
    Rules:
      - Directories must end with '/'.
      - Files are everything else.
      - Indentation depth = (leading spaces // indent_size).
      - Lines that start with `comment_prefix` (after leading spaces) are ignored.

    Idempotent: safe to re-run.
    """
    if indent_size <= 0:
        raise ValueError("indent_size must be a positive integer")

    os.makedirs(base_dir, exist_ok=True)
    base_dir = os.path.abspath(base_dir)

    # depth -> absolute directory path at that depth
    depth_dir = {-1: base_dir}

    for raw_line in _iter_structure_lines(structure_text, comment_prefix):
        leading = _leading_ws_count(raw_line)
        depth = leading // indent_size
        name = raw_line.strip()

        is_dir = name.endswith("/")
        clean_name = name[:-1] if is_dir else name

        parent = depth_dir.get(depth - 1, base_dir)
        path = os.path.join(parent, clean_name)

        if is_dir:
            os.makedirs(path, exist_ok=True)
            depth_dir[depth] = path
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # touch file
            with open(path, "a", encoding="utf-8"):
                pass

def read_structure_file(structure_basename: str, extension: str = ".txt") -> str:
    """
    Read <structure_basename><extension> and return its contents as string.
    E.g., structure_basename='structure' -> reads 'structure.txt'
    """
    filename = f"{structure_basename}{extension}"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Structure file not found: {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

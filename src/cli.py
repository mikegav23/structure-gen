import argparse
import os
import sys
from .core import create_structure_from_text, DEFAULT_INDENT

def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="structure-gen",
        description="Create a directory/file tree from a simple indented text file."
    )
    p.add_argument(
        "structure_name",
        help="Base name of the structure file (without extension). Example: 'structure' -> reads 'structure.txt'."
    )
    p.add_argument(
        "base_dir",
        nargs="?",
        default=".",
        help="Directory to create the structure in (default: current directory)."
    )
    p.add_argument(
        "--indent",
        type=int,
        default=DEFAULT_INDENT,
        help=f"Spaces per indentation level (default: {DEFAULT_INDENT})."
    )
    p.add_argument(
        "--ext",
        default=".txt",
        help="Structure file extension to read (default: .txt)."
    )
    p.add_argument(
        "--comment-prefix",
        default="#",
        help="Lines starting with this (after leading spaces) are ignored (default: '#')."
    )
    return p.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)

    # Full path to the structure file
    txt_file = f"{args.structure_name}{args.ext}"
    txt_file = os.path.abspath(txt_file)

    if not os.path.exists(txt_file):
        print(f"❌ File not found: {txt_file}", file=sys.stderr)
        sys.exit(1)

    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    # If user didn’t specify base_dir, use the txt file’s directory
    if args.base_dir == ".":
        base_dir = os.path.dirname(txt_file)
    else:
        base_dir = args.base_dir

    os.makedirs(base_dir, exist_ok=True)

    try:
        create_structure_from_text(
            text,
            base_dir=base_dir,
            indent_size=args.indent,
            comment_prefix=args.comment_prefix,
        )
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Created structure in: {os.path.abspath(base_dir)}")


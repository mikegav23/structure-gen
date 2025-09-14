# structure-gen

A lightweight Python CLI tool that reads a **tree-style text file** and generates the corresponding directory + empty file structure on disk.  
Ideal for scaffolding projects quickly without manually running `mkdir` and `touch`.

---

## ✨ Features

- Reads simple `.txt` files with indentation.
- Directories must end with `/`, files can be anything else (dotfiles supported).
- Indentation depth = **2 spaces per level** (default, configurable with `--indent`).
- Ignores comments (lines starting with `#` by default).
- **Default behavior**: builds the structure in the same folder as the `.txt` file.
- Optional override: specify a custom base directory.

---

## 📂 Example

### Input: `structure.txt`

```txt
my-app/
  README.md
  requirements.txt
  src/
    init.py
    main.py
    tests/
    init.py
    test_main.py
```

### Run

```bash
structure-gen structure
```

---

## 🚀 Installation

```bash
pipx install git+https://github.com/mikegav23/structure-gen.git
```

---

## ⚡ Usage Examples

```bash
# Create structure in the same folder as structure.txt
structure-gen structure

# Create structure in a specific folder
structure-gen structure ./my-app

# Use a different extension
structure-gen structure --ext .tree

# Use 4-space indentation
structure-gen structure --indent 4

# Change comment prefix
structure-gen structure --comment-prefix "//"
```

---

## 🛡 Notes

- Directories must end with /.
- Indentation must be consistent (--indent spaces per level).
- Safe to re-run (idempotent).
- Lines starting with the comment prefix are ignored.

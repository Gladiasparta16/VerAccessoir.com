import py_compile
import pathlib
import sys

errors = []
for p in pathlib.Path('.').rglob('*.py'):
    # skip virtualenv and hidden dirs
    if any(part.startswith('.') or part in ('venv', '.venv', '__pycache__') for part in p.parts):
        continue
    try:
        py_compile.compile(str(p), doraise=True)
    except Exception as e:
        print(f"ERROR: {p}: {e}")
        errors.append((p, str(e)))

if errors:
    print(f"{len(errors)} files failed compilation")
    sys.exit(2)

print("All Python files compiled successfully")

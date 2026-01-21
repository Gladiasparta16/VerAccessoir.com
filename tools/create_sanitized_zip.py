import os
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
zip_path = Path.home() / 'Desktop' / 'verraaccessoire_share.zip'
exclude_dirs = {'.venv', 'venv', '__pycache__', 'logs', 'instance', '.git', '.vscode'}
exclude_files_suffix = {'.pyc', '.env'}

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for dirpath, dirnames, filenames in os.walk(root):
        # Compute relative path
        rel_dir = os.path.relpath(dirpath, root)
        # Skip excluded directories
        parts = rel_dir.split(os.sep)
        if any(p in exclude_dirs for p in parts if p and p != '.'):
            continue
        for f in filenames:
            if any(f.endswith(suf) for suf in exclude_files_suffix):
                continue
            full_path = Path(dirpath) / f
            rel_path = os.path.relpath(full_path, root)
            z.write(full_path, rel_path)

print(f'Created zip at: {zip_path}')

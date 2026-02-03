"""
Create admin with arbitrary email/password from command-line args.
Usage: .venv\Scripts\python.exe tools\create_admin_cli.py admin@example.com password123
"""
import sys, os
sys.path.insert(0, os.path.abspath('BACKEND'))
from create_admin import create_admin

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: create_admin_cli.py email password')
        sys.exit(1)
    create_admin(sys.argv[1], sys.argv[2])
    print('OK')

"""
Create a test admin programmatically by importing BACKEND modules correctly.
Run with: .venv\Scripts\python.exe tools\create_test_admin.py
"""
import os, sys
sys.path.insert(0, os.path.abspath('BACKEND'))
from create_admin import create_admin

if __name__ == '__main__':
    create_admin('qa_admin@example.com', 'TestAdmin123')
    print('Test admin created (if not present).')

import sqlite3
import sys

DB='database.db'
try:
    conn=sqlite3.connect(DB)
    cur=conn.cursor()
    rows=list(cur.execute("PRAGMA table_info(product);"))
    if not rows:
        print('NO_TABLE')
    else:
        for r in rows:
            print(r)
    conn.close()
except Exception as e:
    print('ERROR', e)
    sys.exit(1)

import sqlite3
DB='data.db'
conn=sqlite3.connect(DB)
cur=conn.cursor()
rows=list(cur.execute("SELECT name FROM sqlite_master WHERE type='table';"))
print(rows)
conn.close()

import sqlite3
DB='data.db'
conn=sqlite3.connect(DB)
cur=conn.cursor()
try:
    cols=[r[1] for r in cur.execute("PRAGMA table_info(product);")]
    if 'featured' in cols:
        print('already_exists')
    else:
        cur.execute('ALTER TABLE product ADD COLUMN featured BOOLEAN DEFAULT 0')
        conn.commit()
        print('column_added')
except Exception as e:
    print('ERROR', e)
finally:
    conn.close()

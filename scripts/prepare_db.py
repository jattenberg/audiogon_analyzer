import sqlite3
import sys

db = "data/audiogon.sqlite"

con = None

try:
    con = sqlite3.connect(db)
    con.execute("DROP TABLE IF EXISTS audiogon")
    cur = con.execute("CREATE TABLE audiogon(listing_id INT, url TEXT, display_title TEXT, anchor_title TEXT, category TEXT, asking_price REAL, new_price REAL)")

except sqlite3.Error, e:
    print "Error: %s" % e.args[0]
    sys.exit(1)

finally:
    if con:
        con.close()

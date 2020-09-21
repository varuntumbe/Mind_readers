import sqlite3


#getting the latest entry in database
def get_last_record_psy_id():
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()
    cur.execute("""
        SELECT * FROM fil_questions WHERE  id = (SELECT max(id) FROM fil_questions)
    """)
    rec=cur.fetchone()
    conn.close()
    return rec[5]


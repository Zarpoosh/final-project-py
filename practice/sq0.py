#  دستوراتی که تو دیتا بیس ها میزنیم میگن query


import sqlite3
db=sqlite3.connect("data.db")
cur=db.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY,
            name VARCHAR(20),
            grade INTEGER
        )"""
)


grades=[
    ("minoo", 20),
    ("maryam", 23),
    ("kimia", 12),
    ("romina", 100)
]


#--------------------------- insert query----------------------------------------
# cur.executemany(
#     """INSERT INTO students(name, grade) VALUES(?,?)""",grades
# )


# --------------------------select query-----------------------------------------
#  تنها کویری هست که نیازی به کامیت کردن نداره 
# res=cur.execute(
#     # """SELECT * FROM students"""
#     """SELECT name,grade FROM students"""
# )


# for item in res:
#     print(item)
    
    

# ---------------------------delete query--------------------------------------
# cur.execute("DELETE FROM students WHERE name=?",("maryam",) )

# update query

query="""UPDATE students SET name=? WHERE name="romina" """
value=("zahra",)
cur.execute(
    query,value
)
db.commit()
db.close()
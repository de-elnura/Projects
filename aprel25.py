# import sqlite3

# conn = sqlite3.connect("info.db")
# ishlatish = conn.cursor()

# ishlatish.execute("""
#     CREATE TABLE student(
# #         id INTEGER,
# #         name TEXT,
# #         age INTEGER
# #     );               
# # """)



# # conn.execute("INSERT INTO student (id, name, age) VALUES (?, ?, ?)", (2, "elnura", 22))



# conn.execute ("""UPDATE student SET name = "Charos" WHERE id = 2""")


# # ishlatish.execute("DELETE FROM student WHERE id = 1")
# conn.commit()
# # conn.commit()
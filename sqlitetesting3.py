import sqlite3

connection = sqlite3.connect("mainDatabase.db")
mainCursor = connection.cursor()

#mainCursor.execute("DROP TABLE TimeRecord")
#mainCursor.execute("""
#CREATE TABLE TimeRecord (
#                   date text,
#                  epoch text,
#                   overhead text,
#                  timerange_sunlit text
#                   )
#""")

#connection.commit()

#connection.execute("INSERT INTO TimeRecord VALUES ('lol', 'lol', 'lol')")



mainCursor.execute("SELECT * FROM TimeRecord")
print(mainCursor.fetchone())

connection.close()
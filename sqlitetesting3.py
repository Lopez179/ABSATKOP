import sqlite3

connection = sqlite3.connect("mainDatabase.db")
mainCursor = connection.cursor()

#mainCursor.execute("""
#CREATE TABLE TimeRecord (
#                   date text,
#                  epoch text,
#                   timerange_sunlit text
#                   )
#""")

#connection.execute("INSERT INTO TimeRecord VALUES ('lol', 'lol', 'lol')")

connection.commit()
connection.close()
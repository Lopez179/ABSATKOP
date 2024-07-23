import sqlite3

connection = sqlite3.connect("mainDatabase.db")
mainCursor = connection.cursor()

#mainCursor.execute("DROP TABLE TimeRecord")
#mainCursor.execute("""
#CREATE TABLE TimeRecord (
#                   date text,
#                  epoch text,
#                   overhead_periods_for_the_next_month text,
#                  timerange_sunlit_in_the_next_6_hours text
#                   )
#""")

#connection.commit()

#connection.execute("INSERT INTO TimeRecord VALUES ('lol', 'lol', 'lol')")



mainCursor.execute("SELECT * FROM TimeRecord ORDER BY date DESC")
print(mainCursor.fetchall())

connection.close()
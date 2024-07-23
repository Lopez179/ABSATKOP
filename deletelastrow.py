import sqlite3

connection = sqlite3.connect("mainDatabase.db")
mainCursor = connection.cursor()

mainCursor.execute("""DELETE FROM TimeRecord WHERE date IN
                    (SELECT date FROM TimeRecord ORDER BY date ASC limit 1)""")

connection.close()
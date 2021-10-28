import sqlite3


def create_bd() -> None:
    """ create the DB and populate if it doesn't exists """

    con = sqlite3.connect('prediction.db')

    cur = con.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS genre(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT NOT NULL );""")

    cur.execute(""" CREATE TABLE IF NOT EXISTS title (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        genre_id INTEGER NOT NULL,
        
        FOREIGN KEY (genre_id) REFERENCES genre (id));""")

    # Check if genre table is empty, if yes insert the genre
    cur.execute("SELECT COUNT(*) from genre LIMIT 1")
    res = cur.fetchone()
    if res[0] == 0:
        values = ["Soul and Reggae", "Pop", "Punk", "Jazz and Blues", "Metal",
                  "Dance and Electronica", "Folk", "Classic Pop and Rock"]

        for val in values:
            cur.execute("INSERT INTO genre (genre) VALUES (?)", [val])

    con.commit()
    con.close()
    return


def get_title_by_genre(genre: str):
    con = sqlite3.connect('./prediction.db')
    cur = con.cursor()
    cur.execute("SELECT title.title FROM title INNER JOIN genre ON genre.id=title.genre_id WHERE lower(genre.genre)=='%s'" % genre.lower())
    result = cur.fetchall()
    con.close()
    return result


def get_genre():
    con = sqlite3.connect('./prediction.db')
    cur = con.cursor()
    cur.execute("SELECT DISTINCT genre.genre FROM title INNER JOIN genre ON genre.id=title.genre_id")
    result = cur.fetchall()
    con.close()
    return result

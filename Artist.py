import psycopg2

def newArtist(curs, conn):
    try:
        curs.execute("SELECT COUNT(artist_id) FROM artist")
        artist_id = curs.fetchone()
        artist_id = artist_id[0]
        if artist_id is None:
            artist_id = 1
        else:
            curs.execute("SELECT MAX(artist_id) FROM artist")
            artist_id = curs.fetchone()
            artist_id = artist_id[0]
            artist_id += 1
        print("Artist Name:")
        name = input()
        sql = "INSERT INTO artist(artist_id, name) VALUES(%s, %s)"
        val = (str(artist_id), name)
        curs.execute(sql, val)
        conn.commit()

        print("Artist created")

    except psycopg2.Error as e:
        print(e.diag.message_primary)
        print("Artist not created")


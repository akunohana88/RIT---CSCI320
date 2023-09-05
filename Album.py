import psycopg2

def newAlbum(curs, conn):
    try:
        curs.execute("SELECT COUNT(album_id) FROM album")
        bum_id = curs.fetchone()
        bum_id = bum_id[0]
        if bum_id is None:
            bum_id = 1
        else:
            curs.execute("SELECT MAX(album_id) FROM album")
            bum_id = curs.fetchone()
            bum_id = bum_id[0]
            bum_id += 1
        print("Album Name:")
        name = input()
        sql1 = "INSERT INTO album(album_id, name) VALUES(%s, %s)"
        val1 = (str(bum_id), name)
        curs.execute(sql1, val1)
        conn.commit()
        print("Artist ID:")
        arti_id = input()
        sql2 = "INSERT INTO produces(artist_id, album_id) VALUES(%s, %s)"
        val2 = (str(arti_id), str(bum_id))
        curs.execute(sql2, val2)
        conn.commit()
        print("Genre ID:")
        genre_id = input()
        sql3 = "INSERT INTO categorizes(genre_id, album_id) VALUES(%s, %s)"
        val3 = (str(genre_id), str(bum_id))
        curs.execute(sql3, val3)
        conn.commit()
        print("Album Created")
    except psycopg2.Error as e:
        print(e.diag.message_primary)
        print("Playlist not created")

def insertAlbum(album_id, song_id, curs, conn):
    try:
        sql = "SELECT COUNT(track_number) FROM lists WHERE album_id = %s"
        val = (str(album_id),)
        curs.execute(sql, val)
        track_number = curs.fetchone()
        track_number = track_number[0]
        if track_number == 0:
            track_number = 1

        else:
            sql = "SELECT MAX(track_number) FROM lists WHERE album_id = %s"
            val = (str(album_id),)
            curs.execute(sql, val)
            track_number = curs.fetchone()
            #print(track_number)
            track_number = int(track_number[0])
            track_number += 1
            #print(track_number)
        sql1 = "INSERT INTO lists(song_id, album_id, track_number) VALUES(%s, %s, %s)"
        val1 = (str(song_id), str(album_id), str(track_number))
        curs.execute(sql1, val1)
        conn.commit()
        print("Inserted into album")
    except psycopg2.Error as e:
        print(e.diag.message_primary)
        print("Not inserted into album")

def deleteAlbum(album_id, curs, conn):
    try:
        sql1 = "DELETE FROM produces WHERE album_id = %s"
        val1 = (str(album_id),)
        curs.execute(sql1, val1)
        conn.commit()
        sql2 = "DELETE FROM lists WHERE album_id = %s"
        val2 = (str(album_id),)
        curs.execute(sql2, val2)
        conn.commit()
        sql3 = "DELETE FROM categorizes WHERE album_id = %s"
        val3 = (str(album_id),)
        curs.execute(sql3, val3)
        conn.commit()
        sql = "DELETE FROM album WHERE album_id = %s"
        val = (str(album_id),)
        curs.execute(sql, val)
        conn.commit()
    except psycopg2.Error as e:
        print(album_id, curs, conn)
        print(e)
        print("Album not deleted")
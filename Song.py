import psycopg2
import Album
import datetime

import Song


def newSong(muser, curs, conn):
    try:
        curs.execute("SELECT COUNT(song_id) FROM song")
        song_id = curs.fetchone()
        song_id = song_id[0]
        # curs.execute("INSERT INTO song(song_id, title, length) VALUES(" + song_id + ", " + title + ", " + length + ")")
        if song_id is None:
            song_id = 1
        else:
            curs.execute("SELECT MAX(song_id) FROM song")
            song_id = curs.fetchone()
            song_id = song_id[0]
            song_id += 1
        print("Title of song: ")
        title = input()
        print("Enter length of song: (HH:mm:ss)")
        length = input()
        print("Date released? (YYYY-mm-dd)")
        date_released = input()
        sql1 = "INSERT INTO song(song_id, title, length, date_released) VALUES(%s, %s, %s, %s)"
        val1 = (str(song_id), title, length, date_released)
        curs.execute(sql1, val1)
        conn.commit()
        print("ID for an Artist:")
        artist_id = input()
        sql2 = "INSERT INTO composes(artist_id, song_id) VALUES(%s, %s)"
        val2 = (str(artist_id), str(song_id))
        curs.execute(sql2, val2)
        conn.commit()
        sql3 = "INSERT INTO sings(artist_id, song_id) VALUES(%s, %s)"
        val3 = (str(artist_id), str(song_id))
        curs.execute(sql3, val3)
        conn.commit()
        print("Enter a genre id:")
        genre_id = input()
        sql5 = "INSERT INTO individualizes(genre_id, song_id) VALUES(%s, %s)"
        val5 = (str(genre_id), str(song_id))
        curs.execute(sql5, val5)
        conn.commit()
        print("Song created")

    except psycopg2.Error as e:
        print(e.diag.message_primary)
        print("Song not created")

def fetchSongFromID(song_id, curs, conn):
    sql = "SELECT title FROM song WHERE song_id = %s"
    val = (str(song_id),)
    curs.execute(sql, val)
    (title,) = curs.fetchone()
    return title

def fetchIDFromSongTitle(song_name, curs, conn):
    sql = "SELECT song_id FROM song WHERE title = %s"
    val = (song_name,)
    curs.execute(sql, val)
    (song_ID,) = curs.fetchone()
    return song_ID

# def addSongToPlaylist(muser, song_name, curs, conn):
#     song_id = fetchIDFromSongTitle(song_name, curs, conn)
#
#     print("Enter an id for a playlist")
#     playlist_id = input()
#     sql6 = "INSERT INTO collection(playlist_id, song_id, username) VALUES(%s, %s, %s)"
#     val6 = (str(playlist_id), str(song_id), muser)
#     curs.execute(sql6, val6)
#     conn.commit()
    # song_count = playSong(muser, song_id, curs, conn)
    # sql7 = "INSERT INTO plays(username, song_id, count) VALUES(%s, %s, %s)"
    # val7 = (muser, str(song_id), song_count)
    # curs.execute(sql7, val7)
    # conn.commit()

# def addSongtoAlbum(song_name, curs, conn):
#     song_id = fetchIDFromSongTitle(song_name, curs, conn)
#
#     print("ID for an Album:")
#     album_id = input()
#
#     Album.insertAlbum(album_id, str(song_id), curs, conn)  # for inserting into a lists table


def fetchSong(song_id, curs, conn):
    # gets all the songs in the data base ordered by title and artist name in ascending order
    sql = "SELECT * FROM song as S, artist as A, sings as C WHERE S.song_id = C.song_id AND " \
          "A.artist_id = C.artist_id ORDER BY S.title, A.name ASC"
    val = (str(song_id))
    curs.execute(sql, val)
    results = curs.fetchall()

    # get the title of song
    sql1 = "SELECT title FROM song WHERE song_id = %s"
    val1 = (str(song_id),)
    curs.execute(sql1, val1)
    title = curs.fetchone()
    print("Song title: " + title[0])

    # get the artist of a song
    sql2 = "SELECT A.name FROM artist as A, song as S, sings as C " \
           "WHERE S.song_id = %s AND C.artist_id = A.artist_id AND S.song_id = C.song_id"
    val2 = (str(song_id),)
    curs.execute(sql2, val2)
    song_artist = curs.fetchone()
    if song_artist is None:
        print("\tArtist of the song: None")
    else:
        print("\tArtist of the song: " + song_artist[0])

    # get the name of the album
    sql3 = "SELECT A.name FROM lists as L, song as S, album as A " \
           "WHERE S.song_id = %s AND L.album_id = A.album_id AND S.song_id = L.song_id"
    val3 = (str(song_id),)
    curs.execute(sql3, val3)
    song_album = curs.fetchone()
    if song_album is None:
        print("\tSong is in the album: None")
    else:
        print("\tSong is in the album: " + song_album[0])

    # get the length of the song
    sql4 = "SELECT length FROM song WHERE song_id = %s"
    val4 = (str(song_id),)
    curs.execute(sql4, val4)
    (song_len,) = curs.fetchone()
    print("\tLength of song: " + str(song_len))

    # get the total listen count of a song by a user
    sql5 = "SELECT P.count FROM plays as P, muser as U, song as S " \
           "WHERE S.song_id = %s AND P.username = U.username AND P.song_id = S.song_id"
    val5 = (str(song_id),)
    curs.execute(sql5, val5)
    song_listen_count = curs.fetchone()
    if song_listen_count is None:
        print("\tListen count of the song: None")
    else:
        print("\tListen count of the song: " + str(song_listen_count[0]))

    return results

def sortSong(curs, conn):
    print("What do you want to search by?")
    print("title / artist / year / genre")
    com = input().strip()
    print("Order by (ASC)ending or (DESC)ending:")
    order = input().strip()
    if com == "title":
        if order == "ASC" or order == "DESC":
            sql = "SELECT song_id FROM song" \
                  " ORDER BY title "+order
            curs.execute(sql)
            results = curs.fetchall()
            for i in results:
                fetchSong(i[0], curs, conn)
                print()

    elif com == "artist":
        if order == "ASC" or order == "DESC":
            sql = "SELECT S.song_id FROM artist as A, song as S, sings as C " \
               "WHERE S.song_id = C.song_id AND A.artist_id = C.artist_id ORDER BY A.name"+order
            curs.execute(sql)
            results = curs.fetchall()
            for i in results:
                fetchSong(i[0], curs, conn)
                print()
    elif com == "year":
        if order == "ASC" or order == "DESC":
            sql = "SELECT song_id FROM song ORDER BY date_released "+order
            curs.execute(sql)
            results = curs.fetchall()
            for i in results:
                fetchSong(i[0], curs, conn)
                print()
    elif com == "genre":
        if order == "ASC" or order == "DESC":
            sql = "SELECT S.song_id FROM genre as G, song as S, individualizes as I, artist as A, sings as C " \
                  "WHERE S.song_id = I.song_id AND G.genre_id = I.genre_id AND S.song_id = C.song_id AND A.artist_id = C.artist_id" \
                  " ORDER BY G.type "+order
            curs.execute(sql)
            results = curs.fetchall()
            for i in results:
                fetchSong(i[0], curs, conn)
                print()
    else:
        print("Error")

def searchSong(curs, conn):
    print("What do you want to sort by?")
    print("title / artist / album / genre")
    com = input().strip()
    print("Searching by " + com + ":")
    search = input().strip()

    if com == "title":
        sql = "SELECT S.song_id FROM artist as A, song as S, sings as L WHERE S.title = %s AND S.song_id = L.song_id AND A.artist_id = L.artist_id" \
              " ORDER BY S.title, A.name ASC"
        val = (search,)
        curs.execute(sql, val)
        results = curs.fetchall()
        for i in results:
            fetchSong(i[0], curs, conn)
            print(" Song ID: " + str(i[0]))
            print()

    elif com == "artist":
        sql = "SELECT S.song_id FROM artist as A, song as S, sings as L " \
              "WHERE A.name = %s AND S.song_id = L.song_id AND A.artist_id = L.artist_id ORDER BY S.title, A.name ASC"
        val = (search,)
        curs.execute(sql, val)
        results = curs.fetchall()
        for i in results:
            fetchSong(i[0], curs, conn)
            print(" Song ID: " + str(i[0]))
            print()
    elif com == "album":
        sql = "SELECT S.song_id FROM album as A, song as S, lists as L, artist as Art, sings as E " \
              "WHERE A.name = %s AND S.song_id = L.song_id AND A.album_id = L.album_id AND S.song_id = E.song_id AND Art.artist_id = E.artist_id " \
              "ORDER BY S.title, Art.name ASC"
        val = (search,)
        curs.execute(sql, val)
        results = curs.fetchall()
        for i in results:
            fetchSong(i[0], curs, conn)
            print(" Song ID: " + str(i[0]))
            print()
    elif com == "genre":
        sql = "SELECT S.song_id FROM genre as G, song as S, individualizes as I, artist as A, sings as L " \
              "WHERE G.type = %s AND S.song_id = I.song_id AND G.genre_id = I.genre_id AND S.song_id = L.song_id AND A.artist_id = L.artist_id" \
              " ORDER BY S.title, A.name ASC"
        val = (search,)
        curs.execute(sql, val)
        results = curs.fetchall()
        for i in results:
            fetchSong(i[0], curs, conn)
            print(" Song ID: " + str(i[0]))
            print()
    else:
        print("Error")

def playSong(muser, song_name, curs, conn):

    sql = "SELECT P.count FROM plays as P, song as S WHERE P.song_id = S.song_id AND S.title = %s AND P.username = %s"
    val = (song_name, muser[0])
    curs.execute(sql, val)
    count = curs.fetchone()

    song_id = fetchIDFromSongTitle(song_name, curs, conn)

    if count == 0 or count is None:
        playCount = 1
        sql = "INSERT INTO plays(username, song_id, count) VALUES(%s, %s, %s)"
        val = (muser[0], str(song_id), str(playCount))
        curs.execute(sql, val)
        conn.commit()
        print(muser[0] + " played " + str(song_name) + " " + str(playCount) +
              " time")

    else:
        playCount = int(count[0])
        playCount += 1
        sql = "UPDATE plays SET count = %s WHERE song_id = %s"
        val = (str(playCount), song_id)
        curs.execute(sql, val)
        conn.commit()

        print(muser[0] + " played " + song_name + " " + str(playCount) + " times")

def deleteSong(song_id, curs, conn):
    try:
        sql1 = "DELETE FROM collection WHERE song_id = %s"
        val1 = (str(song_id),)
        curs.execute(sql1, val1)
        conn.commit()
        sql2 = "DELETE FROM composes WHERE song_id = %s"
        val2 = (str(song_id),)
        curs.execute(sql2, val2)
        conn.commit()
        sql3 = "DELETE FROM individualizes WHERE song_id = %s"
        val3 = (str(song_id),)
        curs.execute(sql3, val3)
        conn.commit()
        sql4 = "DELETE FROM lists WHERE song_id = %s"
        val4 = (str(song_id),)
        curs.execute(sql4, val4)
        conn.commit()
        sql5 = "DELETE FROM plays WHERE song_id = %s"
        val5 = (str(song_id),)
        curs.execute(sql5, val5)
        conn.commit()
        sql6 = "DELETE FROM sings WHERE song_id = %s"
        val6 = (str(song_id),)
        curs.execute(sql6, val6)
        conn.commit()
        sql = "DELETE FROM song WHERE song_id = %s"
        val = (str(song_id),)
        curs.execute(sql, val)
        conn.commit()
    except psycopg2.Error as e:
        print(song_id, curs, conn)
        print(e)
        print("Song not deleted")

def top50songLast30(curs, conn):
    date = str(datetime.datetime.now()-datetime.timedelta(30)).split()
    date = str(date[0])

    sql1 = "SELECT T.song_id, SUM(T.count) FROM song_timeframe as T WHERE T.date >= %s " \
           "GROUP BY T.song_id ORDER BY SUM(T.count) DESC LIMIT 50"
    val1 = (date,)
    curs.execute(sql1, val1)
    genres = curs.fetchall()

    for x in genres:
        print()
        Song.fetchSong(x[0], curs, conn)
        print("Total Listens: " + str(x[1]))

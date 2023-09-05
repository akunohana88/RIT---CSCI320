import psycopg2
import Song


def numberOfPlaylists(muser, curs, conn):
    sql = "SELECT COUNT(playlistid) FROM playlist WHERE username = %s"
    val = (str(muser[0]),)
    curs.execute(sql, val)
    (results,) = curs.fetchone()
    return results

def fetchPlaylists(muser, curs, conn):
    sql = "SELECT * FROM playlist WHERE username = %s ORDER BY title ASC"
    val = (str(muser[0]),)
    curs.execute(sql, val)
    results = curs.fetchall()

    for x in results:
        print("Playlist name: " + x[1])
        sql1 = "SELECT COUNT(P.title) FROM playlist as P, collection as C WHERE P.title = %s and P.playlistid = C.playlist_id"
        val1 = (x[1],)
        curs.execute(sql1, val1)
        (number_of_songs,) = curs.fetchone()
        print("\tNumber of Songs: " + str(number_of_songs))
        sql2 = "SELECT SUM(S.length) FROM playlist as P, collection as C, song as S " \
               "WHERE P.title = %s and P.playlistid = C.playlist_id and C.song_id = S.song_id"
        val2 = (x[1],)
        curs.execute(sql2, val2)
        (total_time,) = curs.fetchone()
        print("\tTotal Duration: " + str(total_time))

    return results

def newPlaylist(username, curs, conn):
    try:
        curs.execute("SELECT COUNT(playlistid) FROM playlist")
        playlist_id = curs.fetchone()
        playlist_id = playlist_id[0]
        if playlist_id is None:
            playlist_id = 1
        else:
            curs.execute("SELECT MAX(playlistid) FROM playlist")
            playlist_id = curs.fetchone()
            playlist_id = playlist_id[0]
            playlist_id += 1
        print("Title:")
        title = input()
        sql = "INSERT INTO playlist(playlistid, title, username) VALUES(%s, %s, %s)"
        val = (str(playlist_id), title, username[0])
        curs.execute(sql, val)
        conn.commit()
        print("Playlist created")

    except psycopg2.Error as e:
        print(e.diag.message_primary)
        print("Playlist not created")


def insertPlaylist(playlist_id, username, curs, conn):
    try:
        print("What would you like to insert? song or album?")
        response = input().strip()
        print("ID of " + response)
        id = input().strip()
        if response == "song":
            sql1 = "INSERT INTO collection(playlist_id, song_id, username) VALUES(%s, %s, %s)"
            val1 = (str(playlist_id), id, username[0])
            curs.execute(sql1, val1)
            conn.commit()
        if response == "album":
            sql1 = "SELECT song_id FROM lists WHERE album_id = %s"
            val1 = (str(id),)
            curs.execute(sql1, val1)
            results = curs.fetchall()

            for x in results:
                sql = "INSERT INTO collection(playlist_id, song_id, username) VALUES(%s, %s, %s)"
                val = (str(playlist_id), x[0], username[0])
                curs.execute(sql, val)
                conn.commit()

        print("Inserted into playlist")
    except psycopg2.Error as e:
        print(e.diag.message_primary)
        print("Not inserted into playlist")

def deletePlaylist(play_id, curs, conn):
    try:
        sql1 = "DELETE FROM collection WHERE playlist_id = %s"
        val1 = (str(play_id),)
        curs.execute(sql1, val1)
        conn.commit()
        sql = "DELETE FROM playlist WHERE playlistid = %s"
        val = (str(play_id),)
        curs.execute(sql, val)
        conn.commit()
    except psycopg2.Error as e:
        print(play_id, curs, conn)
        print(e)
        print("Playlist not deleted")

def deleteSongFromPlaylist(song_id, playlist_id, curs, conn):
    try:
        sql1 = "DELETE FROM collection WHERE song_id = %s AND playlist_id = %s"
        val1 = (str(song_id), str(playlist_id),)
        curs.execute(sql1, val1)
        conn.commit()
    except psycopg2.Error as e:
        print(song_id, playlist_id, curs, conn)
        print(e)
        print("Song " + song_id + "not deleted from playlist " + playlist_id)

def getPlaylistIDFromTitle(title, curs, conn):
    sql = "SELECT playlistid FROM playlist WHERE title = %s"
    val = (title,)
    curs.execute(sql, val)
    (playlist_id,) = curs.fetchone()
    return playlist_id

def getPlaylistTitleFromId(playlist_id, curs, conn):
    sql = "SELECT title FROM playlist WHERE playlistid = %s"
    val = (str(playlist_id),)
    curs.execute(sql, val)
    (playlist_title,) = curs.fetchone()
    return playlist_title

def playAllSongsInPlaylist(playlist_name, muser, curs, conn):
    playlist_id = getPlaylistIDFromTitle(playlist_name, curs, conn)
    sql = "SELECT song_id FROM collection WHERE playlist_id = %s AND username = %s"
    val = (str(playlist_id), muser[0])
    curs.execute(sql, val)

    songIdsInPlaylist = curs.fetchall()

    for song_id in songIdsInPlaylist:
        song_name = Song.fetchSongFromID(song_id[0], curs, conn)
        Song.playSong(muser, song_name, curs, conn)

def updatePlaylistName(playlist_id, muser, curs, conn):
    old_playlist_name = getPlaylistTitleFromId(playlist_id, curs, conn)

    sql1 = "UPDATE playlist SET title = %s WHERE username = %s AND playlistid = %s"

    print("What do you want to change the name of " + old_playlist_name + " to?")
    new_playlist_name = input()
    val1 = (new_playlist_name, muser[0], str(playlist_id))
    curs.execute(sql1, val1)
    conn.commit()
    print("Name of the playlist has been changed to " + new_playlist_name)


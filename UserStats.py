import psycopg2
import Song

def userTopArtistsByMostPlayed(muser, curs, conn):
    sql = "SELECT A.name FROM artist as A, plays as P, composes as C " \
          "WHERE A.artist_id = C.artist_id AND C.song_id = P.song_id GROUP BY A.name ORDER BY SUM(P.count) DESC LIMIT 10"
    val = (str(muser[0]),)
    curs.execute(sql, val)
    top_artists = curs.fetchall()
    count = 1

    for x in top_artists:
        print(str(count) + ". " + x[0])
        count += 1

def userTopArtistsByCollections(muser, curs, conn):
    sql = "SELECT A.name FROM artist as A, composes as C, collection as S " \
          "WHERE A.artist_id = C.artist_id AND C.song_id = S.song_id GROUP BY A.name ORDER BY COUNT(A.name) DESC LIMIT 10"
    val = (str(muser[0]),)
    curs.execute(sql, val)
    top_artists = curs.fetchall()
    count = 1

    for x in top_artists:
        print(str(count) + ". " + str(x[0]))
        count += 1

def userTopArtistsByCombinations(muser, curs, conn):
    sql1 = "SELECT A.name FROM artist as A, plays as P, composes as C, collection as S " \
           "WHERE A.artist_id = C.artist_id AND C.song_id = P.song_id AND C.song_id = S.song_id GROUP BY A.name " \
           "ORDER BY SUM(P.count) + COUNT(A.name) DESC LIMIT 10"

    val = (str(muser[0]),)

    curs.execute(sql1, val)
    top_artists = curs.fetchall()
    count = 1

    for x in top_artists:
        print(str(count) + ". " + str(x[0]))
        count += 1

def recommendToPerson(muser, curs, conn):
    sql2 = "SELECT DISTINCT G.type FROM genre as G, individualizes as I, song as S, sings as Si, artist as A WHERE S.song_id in " \
           "(SELECT S.song_id FROM muser as M, plays as P, song as S " \
           "WHERE M.username = %s AND M.username = P.username AND S.song_id = P.song_id ORDER BY P.count DESC LIMIT 3)" \
           "AND S.song_id = I.song_id AND G.genre_id = I.genre_id AND S.song_id = Si.song_id AND A.artist_id = Si.artist_id"
    sql = "SELECT DISTINCT A.name FROM genre as G, individualizes as I, song as S, sings as Si, artist as A WHERE S.song_id in " \
           "(SELECT S.song_id FROM muser as M, plays as P, song as S " \
           "WHERE M.username = %s AND M.username = P.username AND S.song_id = P.song_id ORDER BY P.count DESC LIMIT 3)" \
           "AND S.song_id = I.song_id AND G.genre_id = I.genre_id AND S.song_id = Si.song_id AND A.artist_id = Si.artist_id"

    val = (str(muser[0]),)
    curs.execute(sql2, val)
    results = curs.fetchall()
    curs.execute(sql, val)
    results2 = curs.fetchall()

    ge = set()
    for i in results:
        genre = "SELECT S.song_id FROM song as S, genre as G, individualizes as I " \
                "WHERE G.type = %s " \
                "AND G.genre_id = I.genre_id AND S.song_id = I.song_id " \
                "ORDER BY RANDOM() DESC LIMIT 1"
        val2 = (str(i[0]),)
        curs.execute(genre, val2)
        r = curs.fetchone()
        ge.add(r[0])

    art = set()
    for i in results2:
        genre = "SELECT S.song_id FROM song as S, artist as G, sings as I " \
                "WHERE G.name = %s " \
                "AND G.artist_id = I.artist_id AND S.song_id = I.song_id " \
                "ORDER BY RANDOM() DESC LIMIT 1"
        val2 = (str(i[0]),)
        curs.execute(genre, val2)
        r = curs.fetchone()

        if r is not None:
            art.add(r[0])

    print("RECOMMENDATION BY GENRE:")
    for g in ge:
        print("Song ID: " + str(g))
        Song.fetchSong(g, curs, conn)
        print()
    print()
    print("RECOMMENDATION BY ARTIST:")
    for a in art:
        print("Song ID: "+str(a))
        Song.fetchSong(a, curs, conn)
        print()
    print()

    fr = set()
    genre = "SELECT S.song_id FROM song as S, plays as P, muser as M " \
            "WHERE M.username in (SELECT F.friend_username FROM muser as M, friends as F " \
            "WHERE M.username = %s AND M.username = F.username " \
            "ORDER BY RANDOM() DESC LIMIT 5) AND M.username = P.username AND S.song_id = P.song_id " \
            "ORDER BY P.count DESC LIMIT 5"
    val2 = (str(muser[0]),)
    curs.execute(genre, val2)
    r = curs.fetchall()
    plz = set()
    for ah in r:
        plz.add(ah[0])
    print()
    print("SIMILAR USER RECOMMENDATION:")
    for a in plz:
        print("Song ID: " + str(a))
        Song.fetchSong(a, curs, conn)
        print()







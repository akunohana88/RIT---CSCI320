

def popularity(muser, curs, conn):
    sql1 = "SELECT title FROM song as S, plays as P, friends as F WHERE F.username = %s AND " \
           "P.username = F.Friend_username AND P.song_id = S.song_id GROUP BY S.title ORDER BY COUNT(S.title) DESC LIMIT 50"
    val1 = (str(muser[0]),)
    curs.execute(sql1, val1)
    songs = curs.fetchall()

    count = 1
    for x in songs:
        print(str(count) + ". " + x[0])
        count += 1

def numOfFollowers(muser, curs, conn):
    sql1 = "SELECT COUNT(username) FROM friends WHERE friend_username = %s"
    val1 = (str(muser[0]),)
    curs.execute(sql1, val1)
    (result,) = curs.fetchone()
    print(result)

def following(muser, curs, conn):
    sql1 = "SELECT COUNT(friend_username) FROM friends WHERE username = %s"
    val1 = (str(muser[0]),)
    curs.execute(sql1, val1)
    (result,) = curs.fetchone()
    print(result)

def addAFriend(muser, curs, conn):
    done = 0
    while done == 0:
        print("Type search / follow / list / unfollow / exit:")
        com = input().strip()
        if com == "search":
            print("Enter email:")
            email = input().strip()
            sql = "SELECT * FROM muser WHERE email = %s"
            val = (email,)
            curs.execute(sql, val)
            results = curs.fetchone()
            if results is None:
                print("Email not found!")
            else:
                print("That users name is:")
                print(results[0])
        elif com == "follow":
            print("Enter username:")
            username = input().strip()
            sql = "SELECT * FROM muser WHERE username = %s"
            val = (username,)
            curs.execute(sql, val)
            results = curs.fetchone()
            if results is None:
                print("Invalid User")
            else:
                sql = "INSERT INTO friends(friend_username, username) VALUES(%s, %s)"
                val = (username, muser[0])
                curs.execute(sql, val)
                conn.commit()
                print("Added follow")
        elif com == "list":
            sql = "SELECT friend_username FROM friends WHERE username = %s"
            val = (muser[0],)
            curs.execute(sql, val)
            results = curs.fetchall()
            print("Friends:")
            for i in results:
                print(i[0])
        elif com == "unfollow":
            print("Enter username:")
            username = input().strip()
            sql = "SELECT * FROM muser WHERE username = %s"
            val = (username,)
            curs.execute(sql, val)
            results = curs.fetchone()
            if results is None:
                print("Invalid User")
            else:
                sql = "DELETE FROM friends WHERE friend_username = %s AND username = %s"
                val = (username, muser[0])
                curs.execute(sql, val)
                conn.commit()
                print("Removed follow")
        elif com == "done":
            done = 1
        else:
            print("Not valid!")

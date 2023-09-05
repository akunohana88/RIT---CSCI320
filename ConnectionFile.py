import psycopg2
from sshtunnel import SSHTunnelForwarder
import Album
import Artist
import Friends
import Genre
import Login
import Playlist
import Song
import GenerateNames
import PasswordHash
import UserStats

f = open("UserInfo")
username = f.readline().strip()
password = f.readline().strip()
dbName = "p32002_32"
f.close()
curs = 0
conn = 0

def startProg(curs):
    # login username password
    # crAcc
    #   first
    #   last
    #   email
    #   username
    #   password
    # album art_id name
    # artist name
    # genre name
    # song artist_id title length(HH:mm:ss) date-released (YYYY-mm-dd) genre_id
    muser = None
    playlist = None
    inputCom = ""
    while inputCom != "exit":
        print("Command:")
        inputCom = input()
        com = inputCom.split()
        if muser is not None:
            if com[0] == "friend":
                print("What do you want to do?")
                friend = input()
                if friend == "add":
                    Friends.addAFriend(muser, curs, conn)
                elif friend == "popularity":
                    Friends.popularity(muser, curs, conn)
                elif friend == "followers":
                    Friends.numOfFollowers(muser, curs, conn)
                elif friend == "following":
                    Friends.following(muser, curs, conn)
            #search (LOTS OF BRANCHES)
            elif com[0] == "stats":
                print("Who are your Top 10 Artists?")
                print("Get By most plays/additions to playlists/both/genre")
                answ = input()
                if answ == "most plays":
                    UserStats.userTopArtistsByMostPlayed(muser, curs, conn)
                elif answ == "additions to playlists":
                    UserStats.userTopArtistsByCollections(muser, curs, conn)
                elif answ == "both":
                    UserStats.userTopArtistsByCombinations(muser, curs, conn)
                elif answ == "genre":
                    Genre.topFiveGenres(curs, conn)
            elif com[0] == "last30":
                Song.top50songLast30(curs, conn)
            elif com[0] == "playlist":
                print("What do you want to do?")
                playlist = input()
                if playlist == "number":
                    playlist = Playlist.numberOfPlaylists(muser, curs, conn)
                    print(playlist)
                elif playlist == "fetch":
                    print("Playlists:")
                    playlist = Playlist.fetchPlaylists(muser, curs, conn)
                    print(playlist)
                elif playlist == "create":
                    Playlist.newPlaylist(muser, curs, conn)
                elif playlist == "insert":
                    print("What is the playlist ID?")
                    play_id = input()
                    Playlist.insertPlaylist(play_id, muser, curs, conn)
                elif playlist == "delete":
                    print("Do you want to delete a playlist or a song?")
                    delete = input()
                    if delete == "playlist":
                        print("What is the playlist ID?")
                        play_id = input()
                        Playlist.deletePlaylist(play_id, curs, conn)
                    elif delete == "song":
                        print("What is the song ID of the song you want to delete?")
                        song_id = input()
                        print("Which playlist do you want to delete it from?")
                        playlist_id = input()
                        Playlist.deleteSongFromPlaylist(song_id, playlist_id, curs, conn)
                elif playlist == "play":
                    print("What is the playlist title?")
                    playlist_name = input()
                    Playlist.playAllSongsInPlaylist(playlist_name, muser, curs, conn)
                elif playlist == "update":
                    print("What is the playlist ID?")
                    play_id = input()
                    Playlist.updatePlaylistName(play_id, muser, curs, conn)
                else:
                    print("Code not recognized")
            elif com[0] == "play":
                print("What is the song name?")
                song_name = input()
                Song.playSong(muser, song_name, curs, conn)
            elif com[0] == "search":
                Song.searchSong(curs, conn)
            elif com[0] == "sort":
                Song.sortSong(curs, conn)
            elif com[0] == "recommend":
                UserStats.recommendToPerson(muser,curs,conn)
            #edit playlist
            elif com[0] == "edit":
                pass
            elif com[0] == "signout":
                print("Logged off")
                muser = None
        else:
            if com[0] == "login":
                if muser is None:
                    muser = Login.start(com[1], com[2], curs, conn)
                    if muser is not None:
                        print("Hello " + muser[0] + "! You've been logged in.")

                else:
                    print(muser[0] + " is logged in!")
            elif com[0] == "crAcc":
                muser = Login.create_account(curs, conn)
            elif com[0] == "search":
                Song.searchSong(curs, conn)
            elif com[0] == "sort":
                Song.sortSong(curs, conn)
            elif com[0] == "fetch":
                print("What is the song ID?")
                song_id = input()
                Song.fetchSong(song_id, curs, conn)
            elif com[0] == "delete":
                print("What do you want to delete?")
                delete = input()
                if delete == "album":
                    print("What is the album ID?")
                    bum_id = input()
                    Album.deleteAlbum(bum_id, curs, conn)
                elif delete == "song":
                    print("What is the song ID?")
                    song_id = input()
                    Song.deleteSong(song_id, curs, conn)
                else:
                    print("Code not recognized")
            elif com[0] == "create":
                print("What do you want to create?")
                create = input()
                if create == "album":
                    album = Album.newAlbum(curs, conn)
                    # print(album)
                elif create == "user":
                    muser = Login.create_account(curs, conn)
                elif create == "genre":
                    genre = Genre.newGenre(curs, conn)
                    # print(genre)
                elif create == "artist":
                    artist = Artist.newArtist(curs, conn)
                    # print(artist)
                elif create == "song":
                    song = Song.newSong(muser, curs, conn)
                    # print(song)
            elif com[0] == "insert":
                print("What is the album ID?")
                bum_id = input()
                print("What is the song ID?")
                song_id = input()
                Album.insertAlbum(bum_id, song_id, curs, conn)
            elif com[0] == "help":
                print("login username password")
                print("unlogin")
                print("crAcc (Create's Account)")
                print("album art_id name")
                print("artist name")
                print("genre name")
            elif com[0] == "generate":
                # try:
                #     check_login = "SELECT username FROM muser"
                #     curs.execute(check_login)
                # except psycopg2.Error as e:
                #     print(e.diag.message_primary)
                # results = curs.fetchall()
                # lists = []
                # for r in results:
                #     lists.append(r[0])
                #
                check_login = "SELECT username FROM muser"
                curs.execute(check_login)
                results = curs.fetchall()
                lists = []
                for r in results:
                    lists.append(r[0])

                GenerateNames.randomPairing(range(1,28), range(1,36))
            else:
                print("YA DONE MESSED UP! You can run 'help' to see list of available commands")

    conn.close()


try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")
        startProg(curs)

except psycopg2.Error as e:
    print(e.diag.message_primary)
    print("Connection failed")
    conn.close()
conn.close()



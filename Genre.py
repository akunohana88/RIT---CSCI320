import psycopg2
import datetime

def newGenre(curs, conn):
    try:
        curs.execute("SELECT COUNT(genre_id) FROM genre")
        gene_id = curs.fetchone()
        gene_id = gene_id[0]
        if gene_id is None:
            gene_id = 1
        else:
            curs.execute("SELECT MAX(genre_id) FROM genre")
            gene_id = curs.fetchone()
            gene_id = gene_id[0]
            gene_id += 1
        print("Genre Type:")
        type = input()
        sql1 = "INSERT INTO genre(genre_id, type) VALUES(%s, %s)"
        val1 = (str(gene_id), type)
        curs.execute(sql1, val1)
        conn.commit()
        print("Genre Created")
    except psycopg2.Error as e:
        print(e.diag.message_primary)
        print("Genre Not Created")

def topFiveGenres(curs, conn):
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    day = datetime.datetime.now().day
    currDate = str(datetime.datetime.now() + datetime.timedelta(32-day)).split()

    sql1 = "SELECT G.type FROM genre as G, song_timeframe as T WHERE T.date >= %s AND T.date < %s " \
           "ORDER BY T.count DESC LIMIT 5"
    val1 = (str(year) + "-" + str(month) + "-01", str(currDate[0]))
    curs.execute(sql1, val1)
    genres = curs.fetchall()

    count = 1
    for x in genres:
        print(str(count) + ". " + x[0])
        count += 1

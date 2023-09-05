import datetime

import psycopg2

import PasswordHash


def start(username, password, curs, conn):
    try:
        check_login = "SELECT * FROM muser WHERE username in (%s) AND password in (%s)"
        val = (username, PasswordHash.encode(password))
        curs.execute(check_login, val)
    except psycopg2.Error as e:
        print(e.diag.message_primary)
    results = curs.fetchone()
    #print(results)
    if results is None:
        print("NOT VALID LOL TRY AGAIN NEXT YEAR")
    date = str(datetime.datetime.now()).split()
    date = date[0]
    try:
        sql = "UPDATE muser SET last_date_logged_in = %s WHERE username in (%s)"
        val = (date, username)
        curs.execute(sql, val)
        conn.commit()
    except psycopg2 as e:
        print(e.diag.message_primary)
    return results


def create_account(curs, conn):
    print("To make a account we need some info!")
    print("First Name:")
    first = input()
    print("Last Name:")
    last = input()
    print("Email:")
    email = input()
    print("Hello " + first + " " + last+"!, Make your own account now")
    print("Username:")
    username = ""
    while username == "":
        username = input()
        check_login = "SELECT * FROM muser WHERE username in (%s)"
        val = (username, )
        curs.execute(check_login, val)
        result = curs.fetchone()
        if result is not None:
            print("Already in use! Enter a new one:")
            username = ""
    print("Password:")
    password = input()
    print("Creating account...")
    date = str(datetime.datetime.now()).split()
    date = date[0]
    sql = "INSERT INTO muser(username, first_name, last_name, email, password, last_date_logged_in, creation_date) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    val = (username, first, last, email, password, date, date)
    curs.execute(sql, val)
    conn.commit()
    print("Congrats!")
    return start(username, password, curs, conn)








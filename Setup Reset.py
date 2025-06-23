import mysql.connector

cnx = mysql.connector.connect(user='----', password='----', host='----', autocommit=True)

cur = cnx.cursor()

cur.execute('CREATE DATABASE IF NOT EXISTS copterroyale;')
cur.execute('USE copterroyale;')
cur.execute('CREATE TABLE IF NOT EXISTS game(mode varchar(100));')
cur.execute('SELECT COUNT(*) FROM game');
if cur.fetchone()[0] < 1:
    cur.execute("INSERT INTO game VALUES ('off')")
cur.execute('CREATE TABLE IF NOT EXISTS users(username varchar(20), password varchar(20));')
cur.execute('CREATE TABLE IF NOT EXISTS player(user varchar(20), name varchar(20), r int, g int, b int);')
cur.execute('CREATE TABLE IF NOT EXISTS status(user varchar(20), state char);')
cur.execute('CREATE TABLE IF NOT EXISTS stats(user varchar(20), games int, won int, kills int, maxkills int, topthree int);')

cur.execute("UPDATE game SET mode = 'off';")
cur.execute("UPDATE status SET state = 'i';")

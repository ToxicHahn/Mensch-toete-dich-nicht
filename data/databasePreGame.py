import sqlite3

class DatabasePreGame:
    def __init__(self, init, db_name='inventar.db'):
        self.load = init
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        if self.load == 1:
            print("init database")
            self.drop_tables()
            self.create_tables()
            self.loadTables()

    def drop_tables(self):
        queryDropCoin = '''DROP TABLE IF EXISTS coin;'''
        self.cursor.execute(queryDropCoin)

        queryDropInventar = '''DROP TABLE IF EXISTS inventar;'''
        self.cursor.execute(queryDropInventar)

        print("alle Tabellen gelöscht")

    def create_tables(self):
        queryCoin = '''CREATE TABLE IF NOT EXISTS coin (
            username TEXT NOT NULL PRIMARY KEY,
            coins INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryCoin)
        self.connection.commit

        queryInventar = '''CREATE TABLE IF NOT EXISTS inventar (
            username TEXT NOT NULL PRIMARY KEY,
            freeze INTEGER NOT NULL,
            bombe INTEGER NOT NULL,
            atombombe INTEGER NOT NULL,
            zoll INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryInventar)
        self.connection.commit()

        queryMaxFreeze = '''CREATE TABLE IF NOT EXISTS maxFreeze (
            player TEXT NOT NULL PRIMARY KEY,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryMaxFreeze)
        self.connection.commit()

        queryMaxBombe = '''CREATE TABLE IF NOT EXISTS maxBombe (
            player TEXT NOT NULL PRIMARY KEY,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryMaxBombe)
        self.connection.commit()

        queryMaxAtombombe = '''CREATE TABLE IF NOT EXISTS maxAtombombe (
            player TEXT NOT NULL PRIMARY KEY,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryMaxAtombombe)
        self.connection.commit()

        queryMaxZoll = '''CREATE TABLE IF NOT EXISTS maxZoll (
            player TEXT NOT NULL PRIMARY KEY,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryMaxZoll)
        self.connection.commit()

    def insertCoin(self, username, coins):
        query = 'INSERT INTO coin (username, coins) VALUES (?, ?);'
        self.cursor.execute(query, (username, coins))
        self.connection.commit()

    def insertInventar(self, username, freeze, bombe, atombombe, zoll):
        query = 'INSERT INTO inventar (username, freeze, bombe, atombombe, zoll) VALUES (?, ?, ?, ?, ?);'
        self.cursor.execute(query, (username, freeze, bombe, atombombe, zoll))
        self.connection.commit()

    def insertMaxFreeze(self, player, maxi):
        query = 'INSERT INTO maxFreeze (player, max) VALUES (?, ?) ON CONFLICT(player) DO UPDATE SET max = ?;'
        self.cursor.execute(query, (player, maxi, maxi))
        self.connection.commit()

    def insertMaxBombe(self, player, maxi):
        query = 'INSERT INTO maxBombe (player, max) VALUES (?, ?) ON CONFLICT(player) DO UPDATE SET max = ?;'
        self.cursor.execute(query, (player, maxi, maxi))
        self.connection.commit()

    def insertMaxAtombombe(self, player, maxi):
        query = 'INSERT INTO maxAtombombe (player, max) VALUES (?, ?) ON CONFLICT(player) DO UPDATE SET max = ?;'
        self.cursor.execute(query, (player, maxi, maxi))
        self.connection.commit()

    def insertMaxZoll(self, player, maxi):
        query = 'INSERT INTO maxZoll (player, max) VALUES (?, ?) ON CONFLICT(player) DO UPDATE SET max = ?;'
        self.cursor.execute(query, (player, maxi, maxi))
        self.connection.commit()


    
    def fetchAlleCoin(self):
        query = 'SELECT * FROM coin;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleInventar(self):
        query = 'SELECT * FROM inventar;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleMaxFreeze(self):
        query = 'SELECT * FROM maxFreeze;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleMaxBombe(self):
        query = 'SELECT * FROM maxBombe;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleMaxAtombombe(self):
        query = 'SELECT * FROM maxAtombombe;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleMaxZoll(self):
        query = 'SELECT * FROM maxZoll;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def loadTables(self):
        self.insertCoin('player1', '500')
        self.insertCoin('player2', '500')
        self.insertCoin('player3', '500')
        self.insertCoin('player4', '500')

        self.insertInventar('player1', '0', '0', '0', '0')
        self.insertInventar('player2', '0', '0', '0', '0')
        self.insertInventar('player3', '0', '0', '0', '0')
        self.insertInventar('player4', '0', '0', '0', '0')

        self.insertMaxFreeze('player1', '0')
        self.insertMaxFreeze('player2', '0')
        self.insertMaxFreeze('player3', '0')
        self.insertMaxFreeze('player4', '0')

        self.insertMaxBombe('player1', '0')
        self.insertMaxBombe('player2', '0')
        self.insertMaxBombe('player3', '0')
        self.insertMaxBombe('player4', '0')

        self.insertMaxAtombombe('player1', '0')
        self.insertMaxAtombombe('player2', '0')
        self.insertMaxAtombombe('player3', '0')
        self.insertMaxAtombombe('player4', '0')

        self.insertMaxZoll('player1', '0')
        self.insertMaxZoll('player2', '0')
        self.insertMaxZoll('player3', '0')
        self.insertMaxZoll('player4', '0')


    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    db = DatabasePreGame(1)

    print("DatabasePreGame::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    
    print("COINS::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleCoin()
    for row in data:
        print(row)
    
    print("Inventar::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleInventar()
    for row in data:
        print(row)

    print("MaxFreeze::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleMaxFreeze()
    for row in data:
        print(row)

    print("MaxBombe::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleMaxBombe()
    for row in data:
        print(row)

    print("MaxAtombombe::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleMaxAtombombe()
    for row in data:
        print(row)

    print("MaxZoll::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleMaxZoll()
    for row in data:
        print(row)
        
    db.close_connection()

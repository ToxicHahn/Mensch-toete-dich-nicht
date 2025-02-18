import sqlite3

class Database:
    def __init__(self, init, db_name='databaseN.db'):
        self.load = init
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        if self.load == 1:
            print("init database")
            self.drop_tables()
            self.create_tables()
            self.loadTables()

    def drop_tables(self):
        
        queryDropUser = '''DROP TABLE IF EXISTS user;'''
        self.cursor.execute(queryDropUser)
        
        queryDropGem = '''DROP TABLE IF EXISTS gem;'''
        self.cursor.execute(queryDropGem)
        
        queryDropFreeze = '''DROP TABLE IF EXISTS freeze;'''
        self.cursor.execute(queryDropFreeze)
        queryDropBombe = '''DROP TABLE IF EXISTS bombe;'''
        self.cursor.execute(queryDropBombe)
        queryDropAtombombe = '''DROP TABLE IF EXISTS atombombe;'''
        self.cursor.execute(queryDropAtombombe)
        queryDropZoll = '''DROP TABLE IF EXISTS zoll;'''
        self.cursor.execute(queryDropZoll)

        queryDropKaeufe = '''DROP TABLE IF EXISTS kaeufe;'''
        self.cursor.execute(queryDropKaeufe)
        queryDropSkinKrone = '''DROP TABLE IF EXISTS skinKrone;'''
        self.cursor.execute(queryDropSkinKrone)
        queryDropSkinSchwarz = '''DROP TABLE IF EXISTS skinSchwarz;'''
        self.cursor.execute(queryDropSkinSchwarz)
        queryDropSkinLila = '''DROP TABLE IF EXISTS skinLila;'''
        self.cursor.execute(queryDropSkinLila)
        queryDropSkinRainbow = '''DROP TABLE IF EXISTS skinRainbow;'''
        self.cursor.execute(queryDropSkinRainbow)
        queryDropInventarSkin = '''DROP TABLE IF EXISTS inventarSkin;'''
        self.cursor.execute(queryDropInventarSkin)

        queryDropShop = '''DROP TABLE IF EXISTS shop;'''
        self.cursor.execute(queryDropShop)

        print("alle Tabellen gelöscht")

    def create_tables(self):
        
        queryUser = '''CREATE TABLE IF NOT EXISTS user (
            username TEXT NOT NULL PRIMARY KEY,
            passwort INTEGER NOT NULL,
            status INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryUser)
        self.connection.commit()
        
        queryGem = '''CREATE TABLE IF NOT EXISTS gem (
            username TEXT NOT NULL PRIMARY KEY,
            gems INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryGem)
        self.connection.commit()

        queryFreeze = '''CREATE TABLE IF NOT EXISTS freeze (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryFreeze)
        self.connection.commit()

        queryBombe = '''CREATE TABLE IF NOT EXISTS bombe (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryBombe)
        self.connection.commit()

        queryAtombombe = '''CREATE TABLE IF NOT EXISTS atombombe (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryAtombombe)
        self.connection.commit()

        queryZoll = '''CREATE TABLE IF NOT EXISTS zoll (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryZoll)
        self.connection.commit()

        queryKaeufe = '''CREATE TABLE IF NOT EXISTS kaeufe (
            kaufNr INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            freeze INTEGER,
            bombe INTEGER,
            atombombe INTEGER,
            zoll INTEGER,
            krone INTEGER,
            schwarz INTEGER,
            lila INTEGER,
            rainbow INTEGER,
            ausgabenIns INTEGER
            );
            '''
        self.cursor.execute(queryKaeufe)
        self.connection.commit()

        querySkinKrone = '''CREATE TABLE IF NOT EXISTS skinKrone (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(querySkinKrone)
        self.connection.commit()

        querySkinSchwarz = '''CREATE TABLE IF NOT EXISTS skinSchwarz (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(querySkinSchwarz)
        self.connection.commit()

        querySkinLila = '''CREATE TABLE IF NOT EXISTS skinLila (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(querySkinLila)
        self.connection.commit()

        querySkinRainbow = '''CREATE TABLE IF NOT EXISTS skinRainbow (
            beschreibung TEXT NOT NULL PRIMARY KEY,
            kosten INTEGER NOT NULL,
            max INTEGER NOT NULL
            );
            '''
        self.cursor.execute(querySkinRainbow)
        self.connection.commit()

        queryInventarSkin = '''CREATE TABLE IF NOT EXISTS inventarSkin (
            username TEXT NOT NULL PRIMARY KEY,
            skinKrone INTEGER NOT NULL,
            skinSchwarz INTEGER NOT NULL,
            skinLila INTEGER NOT NULL,
            skinRainbow INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryInventarSkin)
        self.connection.commit()

        queryShop = '''CREATE TABLE IF NOT EXISTS shop (
            shop TEXT NOT NULL PRIMARY KEY,
            beschreibung INTEGER NOT NULL
            );
            '''
        self.cursor.execute(queryShop)
        self.connection.commit()
        
    def insertUser(self, username, passwort, status):
        query = 'INSERT INTO user (username, passwort, status) VALUES (?, ?, ?);'
        self.cursor.execute(query, (username, passwort, status))
        self.connection.commit()
        
    def insertGem(self, username, gems):
        query = 'INSERT INTO gem (username, gems) VALUES (?, ?);'
        self.cursor.execute(query, (username, gems))
        self.connection.commit()
    
    def insertFreeze(self, beschreibung, kosten, max):
        query = 'INSERT INTO freeze (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertBombe(self, beschreibung, kosten, max):
        query = 'INSERT INTO bombe (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertAtombombe(self, beschreibung, kosten, max):
        query = 'INSERT INTO atombombe (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertZoll(self, beschreibung, kosten, max):
        query = 'INSERT INTO zoll (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertKaeufe(self, username, freeze, bombe, atombombe, zoll, krone, schwarz, lila, rainbow, ausgabenIns):
        query = 'INSERT INTO kaeufe (username, freeze, bombe, atombombe, zoll, krone, schwarz, lila, rainbow, ausgabenIns) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        self.cursor.execute(query, (username, freeze, bombe, atombombe, zoll, krone, schwarz, lila, rainbow, ausgabenIns))
        self.connection.commit()

    def insertSkinKrone(self, beschreibung, kosten, max):
        query = 'INSERT INTO skinKrone (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertSkinSchwarz(self, beschreibung, kosten, max):
        query = 'INSERT INTO skinSchwarz (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertSkinLila(self, beschreibung, kosten, max):
        query = 'INSERT INTO skinLila (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertSkinRainbow(self, beschreibung, kosten, max):
        query = 'INSERT INTO skinRainbow (beschreibung, kosten, max) VALUES (?, ?, ?);'
        self.cursor.execute(query, (beschreibung, kosten, max))
        self.connection.commit()

    def insertInventarSkin(self, username, skinKrone, skinSchwarz, skinLila, skinRainbow):
        query = 'INSERT INTO inventarSkin (username, skinKrone, skinSchwarz, skinLila, skinRainbow) VALUES (?, ?, ?, ?, ?);'
        self.cursor.execute(query, (username, skinKrone, skinSchwarz, skinLila, skinRainbow))
        self.connection.commit()

    def insertShop(self, shop, beschreibung):
        query = 'INSERT INTO shop (shop, beschreibung) VALUES (?, ?);'
        self.cursor.execute(query, (shop, beschreibung))
        self.connection.commit()
        
    def fetchAlleUser(self):
        query = 'SELECT * FROM user;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleGem(self):
        query = 'SELECT * FROM gem;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleFreeze(self):
        query = 'SELECT * FROM freeze;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleBombe(self):
        query = 'SELECT * FROM bombe;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleAtombombe(self):
        query = 'SELECT * FROM atombombe;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleZoll(self):
        query = 'SELECT * FROM zoll;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleKaeufe(self):
        query = 'SELECT * FROM kaeufe;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleSkinKrone(self):
        query = 'SELECT * FROM skinKrone;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleSkinSchwarz(self):
        query = 'SELECT * FROM skinSchwarz;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleSkinLila(self):
        query = 'SELECT * FROM skinLila;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleSkinRainbow(self):
        query = 'SELECT * FROM skinRainbow;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleInventarSkin(self):
        query = 'SELECT * FROM inventarSkin;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetchAlleShop(self):
        query = 'SELECT * FROM shop;'
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def loadTables(self):
        
        self.insertUser('jannis', 'jannis', '0')
        self.insertUser('simon', 'simon', '0')
        self.insertUser('emilio', 'emilio', '0')
        self.insertUser('niklas', 'niklas', '0')

        self.insertGem('jannis', '500')
        self.insertGem('simon', '1000')
        self.insertGem('niklas', '600')
        self.insertGem('emilio', '300')

        self.insertFreeze('Eine Falle, welche darauf abzielt den Gegenspieler, der als nächstes das Feld betritt, auf welchem es plaziert wird, für eine Runde aussetzen zu lassen. Diese Falle kann in einem Spiel nur 3 mal verwendet werden.', '200', '3')

        self.insertBombe('Eine Falle, welche darauf abzielt die Figur des Gegenspieler, der als nächstes das Feld betritt, auf welchem es plaziert wird, 3 Felder zurückzuwerfen. Diese mächtige Falle kann 3 mal pro Spiel platziert werden und kostet 20 Coins.', '20', '3')

        self.insertAtombombe('Eine Falle, welche darauf abzielt die Figur des Gegenspieler, der als nächstes das Feld betritt, auf welchem es plaziert wird, zurück in das Haus des Spielers zu werfen.', '20', '3')

        self.insertZoll('Eine strategische Falle, die platziert werden kann, um gegnerische Spieler zu überraschen. Wenn ein Gegner auf den Zoll tritt, verliert er sofort die Hälfte seiner Münzen, die direkt an den Spieler gehen, der die Falle platziert hat. Diese mächtige Falle kann pro Spiel nur zwei Mal erworben werden und ist ideal, um die Kontrolle über das Spielfeld zu sichern und sich einen Vorteil zu verschaffen.', '20', '2')

        self.insertKaeufe('jannis', '0', '0', '0', '0', '0', '0', '0', '0', '0')
        self.insertKaeufe('simon', '0', '0', '0', '0', '0', '0', '0', '0', '0')
        self.insertKaeufe('niklas', '0', '0', '0', '0', '0', '0', '0', '0', '0')
        self.insertKaeufe('emilio', '0', '0', '0', '0', '0', '0', '0', '0', '0')

        self.insertSkinKrone('Ein einzigartiger Skin, der deinem Charakter das Aussehen eines Königs verleiht. exklusive Skin kann nur einmal erworben werden und zeigt allen, wer der wahre Herrscher auf dem Spielfeld ist. Perfekt, um deine Dominanz und deinen Stil', '100', '1')

        self.insertSkinSchwarz('Ein einzigartiger Skin, der deinem Charakter das Aussehen eines Schattens verleiht. Dieser exklusive Skin kann nur einmal erworben werden und zeigt allen, wer die wahre Macht auf dem Spielfeld hat. Perfekt, um Stärke und Präsenz zu präsentieren.', '20', '1')

        self.insertSkinLila('Ein einzigartiger Skin, der deinem Charakter das Aussehen eines Magiers verleiht. exklusive Skin kann nur einmal erworben werden und zeigt allen, wer die wahre Eleganz auf dem Spielfeld besitzt. Perfekt, um deinen Stil und deine Klasse zu', '20', '1')

        self.insertSkinRainbow('Ein einzigartiger Skin, der deinem Charakter das Aussehen eines Künstlers verleiht. Dieser exklusive Skin kann nur einmal erworben werden und zeigt allen, wer die wahre Kreativität auf dem Spielfeld besitzt. Perfekt, um deinen Stil und deine Vielfalt zu präsentieren.', '30', '1')

        self.insertInventarSkin('jannis', '1', '0', '0', '1')
        self.insertInventarSkin('niklas', '0', '1', '0', '1')
        self.insertInventarSkin('emilio', '1', '1', '0', '0')
        self.insertInventarSkin('simon', '0', '0', '1', '1')

        self.insertShop('skin', 'Der Skin Shop ermöglicht es dir durch gesammelte Gems verschiedene Skins zu kaufen, welche deine Gegner einschüchtern und Deine Dominanz auf dem Spielfeld beweisen!')
        self.insertShop('map', 'Der Map Shop ermöglicht es dir durch gesammelte Gems verschiedene Maps zu kaufen. Dies steigert die Varianz innerhalb des Spiels!')
        self.insertShop('marketplace', 'Der Marketplace ermöglicht es dir gesammelte Skins und Maps anderen Spielern zum Kauf anzubieten oder Skins und Maps, welche andere Spieler anbieten, selber zu kaufen!')

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    db = Database(1)
        
    print("Database::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    
    print("User::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleUser()
    for row in data:
        print(row)
        
    print("Gems::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleGem()
    for row in data:
        print(row)

    print("Freeze::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleFreeze()
    for row in data:
        print(row)
    
    print("Bombe::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleBombe()
    for row in data:
        print(row)
    
    print("Atombombe::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleAtombombe()
    for row in data:
        print(row)
    
    print("Zoll::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleZoll()
    for row in data:
        print(row)

    print("Kaeufe::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleKaeufe()
    for row in data:
        print(row)
    
    print("SkinKrone::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleSkinKrone()
    for row in data:
        print(row)
    
    print("SkinSchwarz::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleSkinSchwarz()
    for row in data:
        print(row)
    
    print("SkinLila::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleSkinLila()
    for row in data:
        print(row)
    
    print("SkinRainbow::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleSkinRainbow()
    for row in data:
        print(row)
    
    print("InventarSkin::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleInventarSkin()
    for row in data:
        print(row)

    print("Shops::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    data = db.fetchAlleShop()
    for row in data:
        print(row)
        
    db.close_connection()

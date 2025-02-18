import sqlite3
from oneWindow_GUI import MainWindow

class Login():

    def login(self, username, passwort):
        from login_GUI import LoginWindow # type: ignore

        # Stelle sicher, dass für jede Instanz eine separate Verbindung genutzt wird
        connection = sqlite3.connect(f"databaseN.db")
        cursor = connection.cursor()
        
        query = f'SELECT * FROM user WHERE username == ?;'
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user:
            passwortDB = user[1]
            if passwort == passwortDB:
                if not user[2] == 1:
                    statusn = 1
                    query = f'UPDATE user SET status == ? WHERE username == ?;'
                    cursor.execute(query, (statusn, username))
                    connection.commit()
                    
                    self.oneWindow = MainWindow(username, connection)
                    self.oneWindow.show()
                    self.destroy()
                else:
                    LoginWindow.show_error_message(self, 2)
                    return
            else:
                LoginWindow.show_error_message(self, 1)
                return
        else:
            LoginWindow.show_error_message(self, 0)       
            return    

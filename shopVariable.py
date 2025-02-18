class VariableShop:
    
    def kaufen(self, skin, username):
        query = f'SELECT gems FROM gem WHERE username == ?;'
        self.cursor.execute(query, (username,))
        gem = self.cursor.fetchone()
        if not gem:
            self.show_error_message(1)
            return
        anzGems = gem[0]
        query = f'SELECT kosten FROM {skin};'
        self.cursor.execute(query)
        kosten = self.cursor.fetchone()[0]
        if anzGems >= kosten:
            print(skin)
            query = f'SELECT {skin} FROM inventarSkin WHERE username == ?;'
            self.cursor.execute(query, (username,))
            maxi = self.cursor.fetchone()
            print(maxi)
            maxiN = maxi[0]
            if not maxiN:
                anzGemsNeu = anzGems - kosten
                query = f'UPDATE gem SET gems = ? WHERE username == ?;'
                self.cursor.execute(query, (anzGemsNeu, username))
                self.connection.commit()

                query = f'UPDATE inventarSkin SET {skin} = ? WHERE username == ?;'
                self.cursor.execute(query, (1, username))
                self.connection.commit()
            else:
                self.show_error_message(0)
        else:
            self.show_error_message(1)
        self.updateGUI()
def InitDB(database):
	database.execute('CREATE TABLE IF NOT EXISTS rooms (Id INT NOT NULL, \
		PRIMARY KEY (Id));')
	database.execute('CREATE TABLE IF NOT EXISTS chars (Id INT NOT NULL, \
		Name VARCHAR(255) NOT NULL DEFAULT \'\', \
		Room INT NOT NULL DEFAULT 0, \
			PRIMARY KEY (Id), \
			CONSTRAINT Room FOREIGN KEY (Room) REFERENCES rooms (Id));')
	database.execute('CREATE TABLE IF NOT EXISTS `world` (Id INT NOT NULL, \
		Version INT NOT NULL DEFAULT 1000, \
			PRIMARY KEY (Id));')
	if len(database.execute('SELECT * FROM world WHERE Id = 0').fetchall()) <= 0:
		database.execute('INSERT INTO world (Id, Version) VALUES (0, 1000);')		
	database.commit()

def GetPlayerData(self, playerId):
	playerData = self.bot.database.execute(f'SELECT * FROM chars WHERE Id = {playerId};').fetchall()
	if len(playerData) > 0:
		return playerData[0]
	pass
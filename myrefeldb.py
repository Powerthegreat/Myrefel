def InitDB(database):
	worldVersion = database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()
	if len(worldVersion) <= 0:
		# Initialise the database
		database.execute('CREATE TABLE IF NOT EXISTS rooms (Id INT NOT NULL, \
			Description VARCHAR(2048) NOT NULL DEFAULT \'\', \
			Name VARCHAR(255) NOT NULL DEFAULT \'\', \
				PRIMARY KEY (Id));')
		database.execute('CREATE TABLE IF NOT EXISTS chars (Id INT NOT NULL, \
			Name VARCHAR(255) NOT NULL DEFAULT \'\', \
			Room INT NOT NULL DEFAULT 0, \
				PRIMARY KEY (Id), \
				CONSTRAINT Room FOREIGN KEY (Room) REFERENCES rooms (Id));')
		database.execute('CREATE TABLE IF NOT EXISTS `world` (Id INT NOT NULL, \
			Version INT NOT NULL DEFAULT 0, \
				PRIMARY KEY (Id));')
		database.execute('INSERT INTO world (Id, Version) VALUES (0, 1003);')
		AddRooms(database)
	else:
		# Update from 1000 to 1001 - adding room descriptions, added tavern room
		if worldVersion[0][0] == 1000:
			database.execute('ALTER TABLE rooms \
				ADD COLUMN Description VARCHAR(2048) NOT NULL DEFAULT \'\';')
			database.execute('UPDATE world SET Version = 1001 WHERE  Id = 0;')
			database.execute('INSERT INTO rooms (Id, Description) VALUES (0, \'A tavern with no distinguishing features.\');')
		# Update from 1001 to 1002 - adding names to rooms
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1001:
			database.execute('ALTER TABLE rooms \
				ADD COLUMN Name VARCHAR(255) NOT NULL DEFAULT \'\';')
			database.execute('UPDATE rooms SET Name = \'The Tavern\' WHERE  Id = 0;')
			database.execute('UPDATE world SET Version = 1002 WHERE  Id = 0;')
		# Update from 1002 to 1003 - adding two more rooms
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1002:
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (1, \'A room outside of reality.\', "Erelyn\'s Room");')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (2, \'The storeroom behind the bar of the tavern.\', \'Tavern Storeroom\');')
			database.execute('UPDATE world SET Version = 1003 WHERE  Id = 0;')
	database.commit()

def AddRooms(database):
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (0, \'A tavern with no distinguishing features.\', \'The Tavern\');')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (1, \'A room outside of reality.\', "Erelyn\'s Room");')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (2, \'The storeroom behind the bar of the tavern.\', \'Tavern Storeroom\');')

def GetPlayerData(self, playerId):
	playerData = self.bot.database.execute(f'SELECT * FROM chars WHERE Id = {playerId};').fetchall()
	if len(playerData) > 0:
		return playerData[0]
	pass
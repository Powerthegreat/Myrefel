import myrefeldebug

def InitDB(database):
	worldVersion = database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()
	if len(worldVersion) <= 0:
		# Initialise the database
		myrefeldebug.DebugLog('Initialised database')
		database.execute('CREATE TABLE rooms (Id INT NOT NULL, \
			Description VARCHAR(2048) NOT NULL DEFAULT \'\', \
			Name VARCHAR(255) NOT NULL DEFAULT \'\', \
				PRIMARY KEY (Id));')
		database.execute('CREATE TABLE chars (Id INT NOT NULL, \
			Name VARCHAR(255) NOT NULL DEFAULT \'\', \
			Room INT NOT NULL DEFAULT 0, \
			Hugs INT NOT NULL DEFAULT 0, \
				PRIMARY KEY (Id), \
				CONSTRAINT Room FOREIGN KEY (Room) REFERENCES rooms (Id));')
		database.execute('CREATE TABLE world (Id INT NOT NULL, \
			Version INT NOT NULL DEFAULT 0, \
				PRIMARY KEY (Id));')
		database.execute('CREATE TABLE roomconns (FirstRoom INT NOT NULL DEFAULT 0, \
			SecondRoom INT NOT NULL DEFAULT 0, \
				CONSTRAINT FirstRoom FOREIGN KEY (FirstRoom) REFERENCES rooms(Id), \
				CONSTRAINT SecondRoom FOREIGN KEY (SecondRoom) REFERENCES rooms(Id));')
		database.execute('CREATE TABLE items (Id INT NOT NULL, \
			Name VARCHAR(255) NOT NULL DEFAULT \'\', \
			Description VARCHAR(255) NOT NULL DEFAULT \'\');')
		database.execute('CREATE TABLE inventory (CharId INT NOT NULL DEFAULT 0, \
			ItemId INT NOT NULL DEFAULT 0, \
			Count INT NOT NULL DEFAULT 0, \
				CONSTRAINT CharId FOREIGN KEY (CharId) REFERENCES chars (Id), \
				CONSTRAINT ItemId FOREIGN KEY (ItemId) REFERENCES items (Id));')
		database.execute('INSERT INTO world (Id, Version) VALUES (0, 1010);')
		AddRooms(database)
		AddRoomConnections(database)
		AddItems(database)
	else:
		# Update from 1000 to 1001 - adding room descriptions, added tavern room
		if worldVersion[0][0] == 1000:
			myrefeldebug.DebugLog('Updated database to 1001')
			database.execute('ALTER TABLE rooms \
				ADD COLUMN Description VARCHAR(2048) NOT NULL DEFAULT \'\';')
			database.execute('UPDATE world SET Version = 1001 WHERE  Id = 0;')
			database.execute('INSERT INTO rooms (Id, Description) VALUES (0, \'A tavern with no distinguishing features.\');')
		# Update from 1001 to 1002 - adding names to rooms
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1001:
			myrefeldebug.DebugLog('Updated database to 1002')
			database.execute('ALTER TABLE rooms \
				ADD COLUMN Name VARCHAR(255) NOT NULL DEFAULT \'\';')
			database.execute('UPDATE rooms SET Name = \'The Tavern\' WHERE  Id = 0;')
			database.execute('UPDATE world SET Version = 1002 WHERE  Id = 0;')
		# Update from 1002 to 1003 - adding two more rooms
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1002:
			myrefeldebug.DebugLog('Updated database to 1003')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (1, \'A room outside of reality.\', "Erelyn\'s Room");')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (2, \'The storeroom behind the bar of the tavern.\', \'Tavern Storeroom\');')
			database.execute('UPDATE world SET Version = 1003 WHERE  Id = 0;')
		# Update from 1003 to 1004 - adding room connections, adding the pit
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1003:
			myrefeldebug.DebugLog('Updated database to 1004')
			database.execute('CREATE TABLE roomconns (Id INT NOT NULL, \
				FirstRoom INT NOT NULL DEFAULT 0, \
				SecondRoom INT NOT NULL DEFAULT 0, \
					PRIMARY KEY (Id), \
					CONSTRAINT FirstRoom FOREIGN KEY (FirstRoom) REFERENCES rooms(Id), \
					CONSTRAINT SecondRoom FOREIGN KEY (SecondRoom) REFERENCES rooms(Id));')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (3, \'A dark, dank pit.\', \'The Pit\');')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (0, 0, 2);')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (1, 2, 0);')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (2, 2, 3);')
			database.execute('UPDATE world SET Version = 1004 WHERE  Id = 0;')
		# Update from 1004 to 1005 - adding the flame altar
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1004:
			myrefeldebug.DebugLog('Updated database to 1005')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (4, \'A corridor lit by purple flames.\', \'Corridor\');')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (5, \'An altar of flame.\nPurple lights dance through the air.\', \'Altar\');')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (3, 3, 4);')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (4, 4, 3);')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (5, 4, 5);')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (6, 5, 4);')
			database.execute('UPDATE world SET Version = 1005 WHERE  Id = 0;')
		# Update from 1005 to 1006 - adding the flame
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1005:
			myrefeldebug.DebugLog('Updated database to 1006')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (6, \'Purple flame surrounding you, enveloping your entire being.\', \'Flame\');')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (7, 5, 6);')
			database.execute('INSERT INTO roomconns (Id, FirstRoom, SecondRoom) \
				VALUES (8, 6, 0);')
			database.execute('UPDATE world SET Version = 1006 WHERE  Id = 0;')
		# Update from 1006 to 1007 - hug counter
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1006:
			myrefeldebug.DebugLog('Updated database to 1007')
			database.execute('ALTER TABLE chars \
				ADD COLUMN Hugs INT NOT NULL DEFAULT 0;')
			database.execute('UPDATE world SET Version = 1007 WHERE  Id = 0;')
		# Update from 1007 to 1008 - removing unnecessary column from room connection table
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1007:
			myrefeldebug.DebugLog('Updated database to 1008')
			database.execute('ALTER TABLE roomconns \
				RENAME TO roomconns_old;')
			database.execute('CREATE TABLE roomconns (FirstRoom INT NOT NULL DEFAULT 0, \
				SecondRoom INT NOT NULL DEFAULT 0, \
					CONSTRAINT FirstRoom FOREIGN KEY (FirstRoom) REFERENCES rooms(Id), \
					CONSTRAINT SecondRoom FOREIGN KEY (SecondRoom) REFERENCES rooms(Id));')
			database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
				SELECT FirstRoom, SecondRoom FROM roomconns_old;')
			database.execute('DROP TABLE roomconns_old;')
			database.execute('UPDATE world SET Version = 1008 WHERE  Id = 0;')
		# Update from 1008 to 1009 - adding new rooms for the village
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1008:
			myrefeldebug.DebugLog('Updated database to 1009')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (7, \'A small village.\', \'The Village\');')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (8, \'The blacksmith of the town.\', \'Blacksmith\');')
			database.execute('INSERT INTO rooms (Id, Description, Name) \
				VALUES (9, \'A store selling all manner of goods.\', \'General Store\');')
			database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
				VALUES (0, 7);')
			database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
				VALUES (7, 0);')
			database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
				VALUES (7, 8);')
			database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
				VALUES (8, 7);')
			database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
				VALUES (7, 9);')
			database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
				VALUES (9, 7);')
			database.execute('UPDATE world SET Version = 1009 WHERE  Id = 0;')
		# Update from 1009 to 1010 - adding items
		if database.execute('SELECT Version FROM world WHERE Id = 0').fetchall()[0][0] == 1009:
			database.execute('CREATE TABLE items (Id INT NOT NULL, \
				Name VARCHAR(255) NOT NULL DEFAULT \'\', \
				Description VARCHAR(255) NOT NULL DEFAULT \'\');')
			database.execute('CREATE TABLE inventory (CharId INT NOT NULL DEFAULT 0, \
				ItemId INT NOT NULL DEFAULT 0, \
				Count INT NOT NULL DEFAULT 0, \
					CONSTRAINT CharId FOREIGN KEY (CharId) REFERENCES chars (Id), \
					CONSTRAINT ItemId FOREIGN KEY (ItemId) REFERENCES items (Id));')
			database.execute('INSERT INTO items (Id, Name, Description) \
				VALUES (0, \'Test Item\', \'A test item\');')
			database.execute('UPDATE world SET Version = 1010 WHERE  Id = 0;')
	database.commit()

def AddRooms(database):
	# The tavern
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (0, \'A tavern with no distinguishing features.\', \'The Tavern\');')
	# Erelyn's room
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (1, \'A room outside of reality.\', "Erelyn\'s Room");')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (2, \'The storeroom behind the bar of the tavern.\', \'Tavern Storeroom\');')
	# The pit and rooms beyond
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (3, \'A dark, dank pit.\', \'The Pit\');')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (4, \'A corridor lit by purple flames.\', \'Corridor\');')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (5, \'An altar of flame.\nPurple lights dance through the air.\', \'Altar\');')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (6, \'Purple flame surrounding you, enveloping your entire being.\', \'Flame\');')
	# The village
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (7, \'A small village.\', \'The Village\');')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (8, \'The blacksmith of the town.\', \'Blacksmith\');')
	database.execute('INSERT INTO rooms (Id, Description, Name) \
		VALUES (9, \'A store selling all manner of goods.\', \'General Store\');')


def AddRoomConnections(database):
	# Connecting the tavern with its storeroom
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (0, 2);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (2, 0);')
	# Connecting the tavern to the pit
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (2, 3);')
	# Pit to flame altar
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (3, 4);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (4, 3);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (4, 5);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (5, 4);')
	# Flame altar through the flame back to the tavern
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (5, 6);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (6, 0);')
	# The village
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (0, 7);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (7, 0);')
	# Blacksmith
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (7, 8);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (8, 7);')
	# General store
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (7, 9);')
	database.execute('INSERT INTO roomconns (FirstRoom, SecondRoom) \
		VALUES (9, 7);')

def AddItems(database):
	database.execute('INSERT INTO items (Id, Name, Description) \
		VALUES (0, \'Test Item\', \'A test item\');')

def GetPlayerData(self, playerId):
	# Gets a player's data from the database
	playerData = self.bot.database.execute(f'SELECT * FROM chars WHERE Id = {playerId};').fetchall()
	if len(playerData) > 0:
		return playerData[0]
	pass
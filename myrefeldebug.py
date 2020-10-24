from time import strftime

def DebugLog(message):
	time = str(strftime('%H:%M:%S'))
	print('[' + time + '] ' + message)

def GetPlayerData(self, playerId):
	playerData = self.bot.database.execute(f'SELECT * FROM chars WHERE Id = {playerId};').fetchall()
	if len(playerData) > 0:
		return playerData[0]
	pass
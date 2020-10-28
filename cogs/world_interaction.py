from discord.ext import commands
import myrefeldebug
import myrefeldb
import discord

# Cogs-related commands
class WorldInteraction(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(
		name='inspect',
		description='Shows a description of your current location'
	)
	async def inspect(self, ctx):
		playerData = myrefeldb.GetPlayerData(self, ctx.message.author.id)
		if playerData != None:
			roomName = self.bot.database.execute(f'SELECT name FROM rooms WHERE Id = {playerData[2]};').fetchall()[0][0]
			roomDescription = self.bot.database.execute(f'SELECT description FROM rooms WHERE Id = {playerData[2]};').fetchall()[0][0]
			await ctx.send(f'{roomName}\n{roomDescription}')
		else:
			await ctx.send('You are not registered!')
	
	@commands.command(
		name='move',
		description='Moves you to a different location\nIf no location is specified, shows a list of accessible locations',
		usage='[destination id]'
	)
	async def move(self, ctx, *args):
		playerData = myrefeldb.GetPlayerData(self, ctx.message.author.id)
		if playerData != None:
			connections = self.bot.database.execute(f'SELECT FirstRoom, SecondRoom from roomconns WHERE FirstRoom = {playerData[2]};').fetchall()
			message = ''
			if not args:
				if len(connections) > 0:
					message = 'Available locations:\n'
					for i in range(0, len(connections)):
						message += str(i) + ': ' + self.bot.database.execute(f'SELECT name FROM rooms WHERE Id = {connections[i][1]};').fetchall()[0][0] + '\n'
				else:
					message = 'No available locations'
			else:
				if int(args[0]) < len(connections):
					destination = connections[int(args[0])][1]
					destinationName = self.bot.database.execute(f'SELECT name FROM rooms WHERE Id = {destination};').fetchall()[0][0]
					message = 'Moved to ' + destinationName
					self.bot.database.execute(f'UPDATE chars SET Room = \'{destination}\' WHERE Id = {ctx.message.author.id};')
					self.bot.database.commit()
					myrefeldebug.DebugLog(f'{ctx.message.author} moved to {destinationName}')
				else:
					message = 'Invalid destination!'
			await ctx.send(message)
		else:
			await ctx.send('You are not registered!')
	
def setup(bot):
	bot.add_cog(WorldInteraction(bot))

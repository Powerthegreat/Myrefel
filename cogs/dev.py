from discord.ext import commands
import importlib
import myrefeldebug
import myrefeldb
import discord

class Dev(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(
		name='teleport',
		description='Teleports to a room',
		aliases=['tp'],
		usage='<room id>',
		hidden=True
	)
	@commands.is_owner()
	async def teleport(self, ctx, *args):
		# Teleports a dev to a room by id
		if myrefeldb.GetPlayerData(self, ctx.author.id) != None:
			if not args:
				await ctx.send('You must specify a room id.')
				return

			roomId = int(args[0])
			roomName = self.bot.database.execute(f'SELECT name FROM rooms WHERE Id = {roomId};').fetchall()
			if len(roomName) > 0:
				roomName = roomName[0][0]
				# The teleport itself
				self.bot.database.execute(f'UPDATE chars SET Room = \'{roomId}\' WHERE Id = {ctx.author.id};')
				self.bot.database.commit()
				await ctx.send(f'Teleported you to {roomName}')
				myrefeldebug.DebugLog(f'{ctx.author} teleported to room {roomName}')
			else:
				await ctx.send(f'Invalid room id!')
		else:
			await ctx.send('You are not registered!')
	
	@teleport.error
	async def teleport_error(self, ctx, error):
		myrefeldebug.DebugLog(str(error))
		if isinstance(error, commands.NotOwner):
			myrefeldebug.DebugLog(f'{ctx.author} tried to teleport')
	
	@commands.command(
		name='reload_db',
		description='Loads changes to the database.',
		aliases=['reload_database', 'rdb'],
		hidden=True
	)
	@commands.is_owner()
	async def reload_db(self, ctx):
		# Loads any changes to the database that have been made since the bot started
		importlib.reload(myrefeldb)
		myrefeldb.InitDB(self.bot.database)
		myrefeldebug.DebugLog('Loaded database changes')
		await ctx.send('Loaded database changes')
	
	@reload_db.error
	async def reload_db_error(self, ctx, error):
		myrefeldebug.DebugLog(str(error))
		if isinstance(error, commands.NotOwner):
			myrefeldebug.DebugLog(f'{ctx.author} tried to load database changes')
	
	@commands.command(
		name='moveother',
		description='Moves another user.',
		aliases=['tpother', 'tpo'],
		usage='<room id> <@target>',
		hidden=True
	)
	@commands.is_owner()
	async def moveother(self, ctx, *args):
		# Teleports another player
		if len(ctx.message.mentions) != 1:
			await ctx.send('You must mention exactly one user to teleport.')
			return
		if myrefeldb.GetPlayerData(self, ctx.message.mentions[0].id) != None:
			if not args:
				await ctx.send('You must specify a room id.')
				return

			roomId = int(args[0])
			roomName = self.bot.database.execute(f'SELECT name FROM rooms WHERE Id = {roomId};').fetchall()
			target = ctx.message.mentions[0]
			if len(roomName) > 0:
				roomName = roomName[0][0]
				# The teleport itself
				self.bot.database.execute(f'UPDATE chars SET Room = \'{roomId}\' WHERE Id = {target.id};')
				self.bot.database.commit()
				await ctx.send(f'Teleported {target.mention} to {roomName}')
				myrefeldebug.DebugLog(f'{ctx.author} teleported {target} to room {roomName}')
			else:
				await ctx.send(f'Invalid room id!')
		else:
			await ctx.send('The target is not registered!')
	
	@moveother.error
	async def moveother_error(self, ctx, error):
		myrefeldebug.DebugLog(str(error))
		if isinstance(error, commands.NotOwner):
			myrefeldebug.DebugLog(f'{ctx.author} tried to move another user')

def setup(bot):
	bot.add_cog(Dev(bot))

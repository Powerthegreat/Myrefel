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
	async def register(self, ctx):
		playerData = myrefeldb.GetPlayerData(self, ctx.message.author.id)
		if playerData != None:
			await ctx.send(self.bot.database.execute(f'SELECT description FROM rooms WHERE Id = {playerData[2]};').fetchall()[0][0])
		else:
			await ctx.send('You are not registered!')

def setup(bot):
	bot.add_cog(WorldInteraction(bot))

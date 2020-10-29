from discord.ext import commands
import myrefeldebug
import myrefeldb
import discord

class PlayerInteraction(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(
		name='hug',
		description='Hugs someone',
		aliases=['cuddle', 'snuggle'],
		usasge='<@user>'
	)
	async def hug(self, ctx):
		if len(ctx.message.mentions) > 0:
			secondPlayerData = myrefeldb.GetPlayerData(self, ctx.message.mentions[0].id)
			if secondPlayerData != None:
				secondPlayerName = secondPlayerData[1]
			else:
				secondPlayerName = ctx.message.mentions[0].name

			firstPlayerData = myrefeldb.GetPlayerData(self, ctx.author.id)
			if firstPlayerData != None:
				firstPlayerName = firstPlayerData[1]
			else:
				firstPlayerName = ctx.author.name
			
			if (firstPlayerName == secondPlayerName):
				await ctx.send(f'{firstPlayerName} hugged themself')
			else:
				self.bot.database.execute(f'UPDATE chars SET Hugs = {firstPlayerData[3] + 1} WHERE Id = {firstPlayerData[1]};')
				self.bot.database.execute(f'UPDATE chars SET Hugs = {secondPlayerData[3] + 1} WHERE Id = {secondPlayerData[0]};')
				await ctx.send(f'{firstPlayerName} hugged {secondPlayerName}')
		else:
			await ctx.send('You need to mention someone to hug them!')
	
def setup(bot):
	bot.add_cog(PlayerInteraction(bot))

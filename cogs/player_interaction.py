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
			playerData = myrefeldb.GetPlayerData(self, ctx.message.mentions[0].id)
			if playerData != None:
				secondPlayerName = playerData[1]
			else:
				secondPlayerName = ctx.message.mentions[0].name

			playerData = myrefeldb.GetPlayerData(self, ctx.author.id)
			if playerData != None:
				firstPlayerName = playerData[1]
			else:
				firstPlayerName = ctx.author.name
			
			if (firstPlayerName == secondPlayerName):
				await ctx.send(f'{firstPlayerName} hugged themself')
			else:
				await ctx.send(f'{firstPlayerName} hugged {secondPlayerName}')
		else:
			await ctx.send('You need to mention someone to hug them!')
	
def setup(bot):
	bot.add_cog(PlayerInteraction(bot))

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
			# Get the name of the person being hugged
			secondPlayerData = myrefeldb.GetPlayerData(self, ctx.message.mentions[0].id)
			if secondPlayerData != None:
				secondPlayerName = secondPlayerData[1]
			else:
				secondPlayerName = ctx.message.mentions[0].name

			# Get the name of the person hugging
			firstPlayerData = myrefeldb.GetPlayerData(self, ctx.author.id)
			if firstPlayerData != None:
				firstPlayerName = firstPlayerData[1]
			else:
				firstPlayerName = ctx.author.name
			
			# Check if it's the same person
			if firstPlayerData != None and secondPlayerData != None and firstPlayerData[0] == secondPlayerData[0]:
				await ctx.send(f'{firstPlayerName} hugged themself')
			else:
				# Check if the huggees are in the same room
				if firstPlayerData != None and secondPlayerData != None:
					if firstPlayerData[2] != secondPlayerData[2]:
						await ctx.send(f'You can only hug people in the same room!\n(and unregistered people)')
						return
				
				# Increment their hug counters
				if firstPlayerData != None:
					self.bot.database.execute(f'UPDATE chars SET Hugs = {firstPlayerData[3] + 1} WHERE Id = {firstPlayerData[0]};')
				if secondPlayerData != None:
					self.bot.database.execute(f'UPDATE chars SET Hugs = {secondPlayerData[3] + 1} WHERE Id = {secondPlayerData[0]};')
				
				# "Display" the hug
				await ctx.send(f'{firstPlayerName} hugged {secondPlayerName}')
				myrefeldebug.DebugLog(f'{firstPlayerName} hugged {secondPlayerName}')
		else:
			await ctx.send('You need to mention someone to hug them!')
	
def setup(bot):
	bot.add_cog(PlayerInteraction(bot))

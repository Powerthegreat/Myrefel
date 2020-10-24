from discord.ext import commands
import discord

# Cogs-related commands
class Account(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(
		name='register',
		description='Registers a user',
		aliases=['start']
	)
	async def register(self, ctx):
		print(f'{ctx.message.author} registered')
		await ctx.send('Welcome to Myrefel!')

def setup(bot):
	bot.add_cog(Account(bot))

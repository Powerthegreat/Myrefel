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
		if len(self.bot.database.execute(f'SELECT Id FROM chars WHERE Id=\'{ctx.message.author.id}\';').fetchall()) <= 0:
			self.bot.database.execute(f'INSERT INTO chars (Id, Name) VALUES ({ctx.message.author.id}, \'{ctx.message.author.name}\');')
			print(f'{ctx.message.author} registered')
			await ctx.send('Welcome to Myrefel!')
		else:
			await ctx.send('You have already registered!')
	
	@commands.command(
		name='rename',
		description='Changes your name within Myrefel',
		usage='<name>'
	)
	async def rename(self, ctx, *args):
		if len(self.bot.database.execute(f'SELECT Id FROM chars WHERE Id = {ctx.message.author.id};').fetchall()) > 0:
			if not args:
				await ctx.send('You must specify a name.')
				return
			
			self.bot.database.execute(f'UPDATE chars SET Name = \'{args[0]}\' WHERE Id = {ctx.message.author.id};')
			await ctx.send(f'Updated your name to {args[0]}')
			print(f'{ctx.message.author} updated their name to {args[0]}')
		else:
			await ctx.send('You are not registered!')

def setup(bot):
	bot.add_cog(Account(bot))

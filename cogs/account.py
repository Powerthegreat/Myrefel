from discord.ext import commands
import myrefeldebug
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
			self.bot.database.commit()
			myrefeldebug.DebugLog(f'{ctx.message.author} registered')
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
			self.bot.database.commit()
			await ctx.send(f'Updated your name to {args[0]}')
			myrefeldebug.DebugLog(f'{ctx.message.author} updated their name to {args[0]}')
		else:
			await ctx.send('You are not registered!')
	
	@commands.command(
		name='account',
		description='Displays an account\n@mention a user to view their account',
		usage='[@Mention]'
	)
	async def account(self, ctx):
		target = ctx.message.author
		if len(ctx.message.mentions):
			target = ctx.message.mentions[0]
		
		if len(self.bot.database.execute(f'SELECT Id FROM chars WHERE Id = {target.id};').fetchall()) > 0:
			await ctx.send(embed=discord.Embed(colour=discord.Colour(int('8000FF', 16)),
				title=self.bot.database.execute(f'SELECT Name FROM CHARS WHERE Id = {ctx.message.author.id}').fetchall()[0][0],
				description=f'A citizen of Myrefel'))
		else:
			await ctx.send(f'{target.mention} is not registered!')

def setup(bot):
	bot.add_cog(Account(bot))

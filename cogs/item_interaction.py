from discord.ext import commands
import myrefeldebug
import myrefeldb
import discord

class ItemInteraction(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(
		name='inventory',
		description='Checks your inventory'
	)
	async def inventory(self, ctx, *args):
		# Shows a player's inventory
		target = ctx.author
		
		playerData = myrefeldb.GetPlayerData(self, target.id)
		if playerData != None:
			inventory = self.bot.database.execute(f'SELECT ItemId, Count FROM inventory WHERE CharId = {playerData[0]};').fetchall()

			if not args:
				# Display the whole inventory
				embedToSend = discord.Embed(colour=discord.Colour(int('8000FF', 16)),
					title=f'{playerData[1]}\'s inventory')
				for x in range(0, len(inventory)):
					itemData = self.bot.database.execute(f'SELECT Name, Description FROM items WHERE Id = {inventory[x][0]};').fetchall()[0]
					embedToSend.add_field(name=f'{x + 1}: {itemData[0]}',
						value=f'{itemData[1]}.\nYou have {inventory[x][1]}')
				await ctx.send(embed=embedToSend)
			else:
				itemPosition = int(args[0]) - 1
				if itemPosition >= len(inventory) or itemPosition < 0:
					await ctx.send('You must specify an item within your inventory!')
					return
				itemData = self.bot.database.execute(f'SELECT Name, Description FROM items WHERE Id = {inventory[itemPosition][0]};').fetchall()[0]
				embedToSend = discord.Embed(colour=discord.Colour(int('8000FF', 16)),
					title=f'{itemData[0]}',
					description=f'{itemData[1]}.\nYou have {inventory[itemPosition][1]}')
				await ctx.send(embed=embedToSend)
		else:
			await ctx.send(f'You are not registered!')
	
def setup(bot):
	bot.add_cog(ItemInteraction(bot))

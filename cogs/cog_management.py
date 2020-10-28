from discord.ext import commands
import myrefeldebug
import myrefeldb
import discord

# Cogs-related commands
class Cogs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Reloads a cog
	# Written by Power 07/03/2020
	# Hidden by Power 08/03/2020
	@commands.command(
		name='reload_cog',
		description='Reloads a cog.',
		aliases=['reload_cogs', 'rc', 'reload'],
		usage='<cog>',
		hidden=True
	)
	@commands.is_owner()
	async def reload_cog(self, ctx, *args):
		if args:
			argstr = ''.join(args)
			try:
				self.bot.unload_extension('cogs.' + argstr)
			except commands.ExtensionError as e:
				myrefeldebug.DebugLog(f'Cog {argstr} not loaded')

			self.bot.load_extension('cogs.' + argstr)
			myrefeldebug.DebugLog(f'Cog cogs.{argstr} reloaded')
			await ctx.send(f'Cog {argstr} reloaded')
		else:
			myrefeldebug.DebugLog('No cog specified')
			await ctx.send('No cog specified')

	@reload_cog.error
	async def reload_cog_error(self, ctx, error):
		if isinstance(error, commands.NotOwner):
			myrefeldebug.DebugLog(f'{ctx.message.author} tried to reload a cog')

def setup(bot):
	bot.add_cog(Cogs(bot))

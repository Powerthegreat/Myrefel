from discord.ext import commands
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
			argstr = "".join(args)
			try:
				self.bot.unload_extension('cogs.' + argstr)
			except commands.ExtensionError as e:
				print('Cog {} not loaded'.format(argstr))

			self.bot.load_extension('cogs.' + argstr)
			print('Cog cogs.{} reloaded'.format(argstr))
			await ctx.send('Cog {} reloaded'.format(argstr))
		else:
			print('No cog specified')
			await ctx.send('No cog specified')

	@reload_cog.error
	async def reload_cog_error(self, ctx, error):
		if isinstance(error, commands.NotOwner):
			print('{} tried to reload a cog'.format(ctx.message.author))

def setup(bot):
	bot.add_cog(Cogs(bot))

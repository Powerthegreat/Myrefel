from discord.ext import commands, tasks
from itertools import cycle
import discord
import random
import help

bot = commands.Bot(command_prefix = commands.when_mentioned_or('!'), help_command=help.Help())
cogs = ['cogs.cog_management'
]

welcomeMessages = [
	'Myrefel awaits'
]
status = cycle([
	'Realms of Myrefel',
	'!help to get started'
])

# Displays a message when the bot loads, and loads cogs
@bot.event
async def on_ready():
	print(welcomeMessages[random.randint(0, len(welcomeMessages) - 1)])
	for cog in cogs:
		bot.load_extension(cog)
	status_cycle.start()

# Cycles through statuses	
@tasks.loop(seconds=60)
async def status_cycle():
	await bot.change_presence(activity=discord.Game(next(status)))

# Reloads all cogs
@bot.command(hidden=True)
@commands.is_owner()
async def reload_all(ctx):
	for cog in cogs:
		try:
			bot.unload_extension(cog)
		except commands.ExtensionNotLoaded as e:
			print('Cog {} not loaded'.format(cog))
		bot.load_extension(cog)
		print('Cog {} reloaded'.format(cog))

@reload_all.error
async def reload_all_error(ctx, error):
	if isinstance(error, commands.NotOwner):
		print('{} tried to reload all cogs'.format(ctx.message.author))

tokenFile = open('token')
token = tokenFile.read()
tokenFile.close()

# Run the bot
bot.run(token)
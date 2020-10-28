from discord.ext import commands, tasks
from itertools import cycle
import myrefeldebug
import myrefeldb
import discord
import sqlite3
import random
import help

bot = commands.Bot(command_prefix = commands.when_mentioned_or('!'), help_command=help.Help())
cogs = ['cogs.cog_management',
	'cogs.account',
	'cogs.world_interaction',
	'cogs.dev'
]

welcomeMessages = [
	'Myrefel awaits'
]
status = cycle([
	'Realms of Myrefel',
	'!register to get started'
])

# Displays a message when the bot loads, and loads cogs
@bot.event
async def on_ready():
	myrefeldebug.DebugLog(welcomeMessages[random.randint(0, len(welcomeMessages) - 1)])
	for cog in cogs:
		bot.load_extension(cog)
	status_cycle.start()
	bot.database = sqlite3.connect('data/myrefel.sqlite')
	myrefeldb.InitDB(bot.database)

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
			myrefeldebug.DebugLog(f'Cog {cog} not loaded')
		bot.load_extension(cog)
		myrefeldebug.DebugLog(f'Cog {cog} reloaded')
		await ctx.send(f'Cog {cog} reloaded')

@reload_all.error
async def reload_all_error(ctx, error):
	if isinstance(error, commands.NotOwner):
		myrefeldebug.DebugLog(f'{ctx.message.author} tried to reload all cogs')

tokenFile = open('token')
token = tokenFile.read()
tokenFile.close()

# Run the bot
bot.run(token)
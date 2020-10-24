from discord.ext import commands
from discord.ext.commands.help import Paginator
import discord
import itertools

# Help command
class Help(commands.HelpCommand):
	def __init__(self):
		super().__init__(command_attrs={
				'help': 'Shows usage information about the bot, a category, or command'
		})
		self.paginator = Paginator(prefix='', suffix='', max_size=2000)
		self.indent = 2
		self.sort_commands = True
		self.no_category = 'No category'
		self.commands_heading = '__**Commands**__'

	# Taken from DefaultHelpCommand
	def add_bot_commands_formatting(self, commands, heading):
		if commands:
		# U+2002 Middle Dot
			joined = '\u2002'.join(c.name for c in commands)
			self.paginator.add_line('__**%s**__' % heading)
			self.paginator.add_line(joined)

	# Adapted from DefaultHelpCommand.send_pages
	async def send_pages(self):
		destination = self.get_destination()
		for page in self.paginator.pages:
			await destination.send(embed=discord.Embed(colour=discord.Colour(int('8000FF', 16)), description=page))

	# Taken from DefaultHelpCommand
	def get_opening_note(self):
		command_name = self.invoked_with
		return 'Use `{0}{1} [command]` for more info on a command.\n' \
			'You can also use `{0}{1} [category]` for more info on a category.'.format(self.clean_prefix, command_name)

	# Taken from DefaultHelpCommand
	def add_indented_commands(self, commands, *, heading, max_size=None):
		if not commands:
			return

		self.paginator.add_line(heading)
		max_size = max_size or self.get_max_size(commands)

		get_width = discord.utils._string_width
		for command in commands:
			name = command.name
			width = max_size - (get_width(name) - len(name))
			entry = '{0}{1:<{width}} {2}'.format(self.indent * ' ', name, command.short_doc, width=width)
			self.paginator.add_line(entry)

	# Taken from DefaultHelpCommand
	def add_command_formatting(self, command):
		if command.description:
			self.paginator.add_line(command.description, empty=True)

		signature = self.get_command_signature(command)
		self.paginator.add_line(signature, empty=True)

		if command.help:
			try:
				self.paginator.add_line(command.help, empty=True)
			except RuntimeError:
				for line in command.help.splitlines():
					self.paginator.add_line(line)
				self.paginator.add_line()

	# Adapted from DefaultHelpCommand.send_bot_help
	async def send_bot_help(self, mapping):
		ctx = self.context
		bot = ctx.bot

		if bot.description:
			self.paginator.add_line(bot.description, empty=True)

		note = self.get_opening_note()
		if note:
			self.paginator.add_line(note, empty=True)

		no_category = '\u200b{0.no_category}'.format(self)
		def get_category(command, *, no_category=no_category):
			cog = command.cog
			return cog.qualified_name if cog is not None else no_category

		filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
		to_iterate = itertools.groupby(filtered, key=get_category)

		for category, commands in to_iterate:
			commands = sorted(commands, key=lambda c: c.name) if self.sort_commands else list(commands)
			self.add_bot_commands_formatting(commands, category)

		await self.send_pages()

	# Adapted from DefaultHelpCommand.send_cog_help
	async def send_cog_help(self, cog):
		note = self.get_opening_note()
		if note:
			self.paginator.add_line(note, empty=True)

		if cog.description:
			self.paginator.add_line(cog.description, empty=True)

		filtered = await self.filter_commands(cog.get_commands(), sort=self.sort_commands)
		self.add_indented_commands(filtered, heading=self.commands_heading)

		await self.send_pages()

	# Adapted from DefaultHelpCommand.send_group_help
	async def send_group_help(self, group):
		self.add_command_formatting(group)

		filtered = await self.filter_commands(group.commands, sort=self.sort_commands)
		if filtered:
			note = self.get_opening_note()
			if note:
				self.paginator.add_line(note, empty=True)

			self.paginator.add_line('**%s**' % self.commands_heading)
			for command in filtered:
				self.add_subcommand_formatting(command)

		await self.send_pages()

	# Adapted from DefaultHelpCommand.send_command_help
	async def send_command_help(self, command):
		self.add_command_formatting(command)
		self.paginator.close_page()
		await self.send_pages()

	# Taken from DefaultHelpCommand
	def get_command_signature(self, command):
		parent = command.full_parent_name
		if len(command.aliases) > 0:
			aliases = '|'.join(command.aliases)
			fmt = '[%s|%s]' % (command.name, aliases)
			if parent:
				fmt = parent + ' ' + fmt
			alias = fmt
		else:
			alias = command.name if not parent else parent + ' ' + command.name
		return '%s%s %s' % (self.clean_prefix, alias, command.signature)
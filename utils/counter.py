from discord.ext import commands

class Counter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.database = self.bot.get_cog("Database")


	# Listeners
	# Listens for messages in the game channel
	@commands.Cog.listener()
	async def on_message(self, message):
		guild, author = message.guild, message.author
		print(guild.id)
		channel = guild.get_channel(self.database.get_channel(guild.id))
		if message.author != client.user:
			if channel and message.channel == channel:
				try:
					count = int(message.content)
					previous_author, previous_count = self.database.get_last_message(guild.id)
					if count != previous_count + 1 or author.id == previous_author:
						await message.delete
					else:
						self.database.update_score(guild.id, author.id)
						self.database.update_last_message(guild.id, author.id, count)
				except ValueError:
					await message.delete()


def setup(bot):
	bot.add_cog(Counter(bot))

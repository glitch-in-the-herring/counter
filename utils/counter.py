from discord.ext import commands

class Counter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# Listeners
	# Listens for messages in the game channel
	@commands.Cog.listener()
	async def on_message(self, message):
		database = self.bot.get_cog("Database")		
		guild, author = message.guild, message.author
		channel = guild.get_channel(database.get_channel(guild.id))
		if message.author != self.bot.user:
			if channel and message.channel == channel:
			#try:
				count = int(message.content)
				previous_author, previous_count = database.get_last_message(guild.id)
				print(previous_author)
				if count != previous_count + 1 or author.id == previous_author:
					print("why")
					await message.delete
				else:
					database.update_score(guild.id, author.id)
					database.update_last_message(guild.id, author.id, count)
					database.commit()
			#except ValueError:
				#print("oh it went her")
				#await message.delete()


def setup(bot):
	bot.add_cog(Counter(bot))

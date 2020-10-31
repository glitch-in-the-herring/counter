import discord
from discord.ext import commands

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.database = bot.get_cog("Database")


	# Checks
	# Checks if the user invoking the command is an admin
	# Currently hardcoded
	def is_admin():
		async def predicate(ctx):
			member = ctx.author
			return member.id in [284481404992094209]	
		return commands.check(predicate)


	# Commands
	# Sets the game channel
	@commands.command(
		name="setchannel",
		help="Sets the text channel for the counting game. You can only have one channel per server.",
		brief="Set the server's counting channel."
	)
	@is_admin()
	async def setchannel(self, ctx, channel:discord.TextChannel):
		self.database.update_channel(ctx.guild.id, channel.id)
		self.database.commit()
		await ctx.send(f"Successfully set <#{channel.id}> as the counting channel for this server.")

	@commands.command(
		name="update",
		help="Updates the score table for the counting game. Must be performed after a reset or a setchannel.",
		brief="Forces the score to update."
	)
	@is_admin()
	async def update(self, ctx):
		guild = ctx.guild
		channel = guild.get_channel(self.database.get_channel(guild.id))
		self.database.clear_score(guild.id)
		async for message in channel.history(limit=None, oldest_first=True):
			try:
				count = int(message.content)
				self.database.update_score(guild.id, message.author.id)
				self.databae.update_last_message(guild.id, message.author.id, content)
			except ValueError:
				pass
		self.database.commit()
		await ctx.send("Successfully updated the game channel.")


def setup(bot):
	bot.add_cog(Updater(bot))

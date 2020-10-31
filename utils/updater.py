import discord
from discord.ext import commands

class Updater(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


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
		database = self.bot.get_cog("Database")	
		database.update_channel(ctx.guild.id, channel.id)
		database.commit()
		await ctx.send(f"Successfully set <#{channel.id}> as the counting channel for this server.")

	@commands.command(
		name="update",
		help="Updates the score table for the counting game. Must be performed after a reset or a setchannel.",
		brief="Forces the score to update."
	)
	@is_admin()
	async def update(self, ctx):
		guild = ctx.guild
		database = self.bot.get_cog("Database")	
		channel = guild.get_channel(database.get_channel(guild.id))
		database.clear_score(guild.id)
		async for message in channel.history(limit=None, oldest_first=True):
			try:
				count = int(message.content)
				database.update_score(guild.id, message.author.id)
				database.update_last_message(guild.id, message.author.id, count)
			except ValueError:
				pass
		database.commit()
		await ctx.send("Successfully updated the game channel.")

	@commands.command(
		name="purge",
		help="Purges the messages in the game channel.",
		brief="Purges the messages in the game channel"
	)
	@is_admin()
	async def purge(self, ctx, count:int):
		guild = ctx.guild
		database = self.bot.get_cog("Database")	
		channel = guild.get_channel(database.get_channel(guild.id))		
		deleted = await channel.purge(limit=count)
		await ctx.send(f'Successfully deleted {len(deleted)} messages')		


def setup(bot):
	bot.add_cog(Updater(bot))

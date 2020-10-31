import discord
from discord.ext import commands

ranks = [
			":first_place: **1st Place**", 
			":second_place: **2nd Place**", 
			":third_place: **3rd Place**", 
			":medal: **4th Place**", 
			":military_medal: **5th Place**",
			"**6th Place**",
			"**7th Place**",
			"**8th Place**",
			"**9th Place**",
			"**10th Place**"
		]

class Leaderboard(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	# Commands
	# Retrieves the leaderboard
	@commands.command(
		name="leaderboard",
		help="Retrieves the leaderboard of the curent guild. Defaults to 10 users",
		brief="Retrieves the leaderboard"
	)
	async def leaderboard(self, ctx, *args):
		guild = ctx.guild
		database = self.bot.get_cog("Database")	
		top10 = database.get_top10(guild.id)
		embed = discord.Embed(
			title = f"Server Leaderboard for {message.guild.name}",
			timestamp = datetime.now(timezone.utc), 
			color = discord.Colour(0x4BA1C7)
		)         
		if len(args) == 0:
			for y, x in ranks:
				embed.add_field(
					name=rank[y],
					value=f"{str(guild.get_member(top10[y][0]))} - {top10[y][1]} point(s)"
				)
		elif len(args) == 1 and 1 <= args[0] <= 10:
			for y,x in ranks[0:args[0]]:
				embed.add_field(
					name=rank[y],
					value=f"{str(guild.get_member(top10[y][0]))} - {top10[y][1]} point(s)"
				)
		await ctx.send(embed=embed)				

def setup(bot):
	bot.add_cog(Leaderboard(bot))

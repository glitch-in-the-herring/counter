import sqlite3
from discord.ext import commands

conn = sqlite3.connect("counter.db")
c = conn.cursor()

class Dabatase(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	def commit(self):
		conn.commit()


	def update_channel(self, guild_id, channel_id):
		c.execute("INSERT OR REPLACE INTO guilds (guild_id, channel_id, last_author_id, last_count) VALUES (?, ?, ?, ?)", [guild_id, channel_id, None, None])


	def get_channel(self, guild_id):
		try:
			return c.execute("SELECT channel_id FROM guilds WHERE guild_id = ?", [guild_id]).fetchone()[0]
		except TypeError:
			return None


	def update_last_message(self, guild_id, last_author_id, last_count):
		c.execute("UPDATE guilds SET last_author_id = ?, last_count = ? WHERE guild_id = ?", [last_author_id, last_count, guild_id])


	def get_last_message(self, guild_id):
		return list(c.execute("SELECT last_author_id, last_count FROM guilds WHERE guild_id = ?", [guild_id]))


	def get_score(self, guild_id, user_id):
		try:
			return c.execute("SELECT score FROM scores WHERE guild_id = ? AND user_id = ?", [guild_id, user_id]).fetchone()[0]
		except TypeError:
			return 0

	def update_score(self, guild_id, user_id):
		previous_score = get_score(guild_id, user_id)
		c.execute("UPDATE scores SET score = ? WHERE guild_id = ? AND user_id = ?", [previous_score + 1, guild_id, user_id])


	def clear_score(self, guild_id):
		c.execute("DELETE FROM scores WHERE guild_id = ?", [guild_id])


	def get_top10(self, guild_id):
		return list(c.execute("SELECT user_id, score FROM scores where guild_id = ? ORDER BY score DESC, user_id DESC LIMIT 10", [guild_id]))

def setup(bot):
	bot.add_cog(Database(bot))

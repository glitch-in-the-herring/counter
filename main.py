import os, argparse, logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", metavar='TOKEN', help="Bot token. Keep this secret")
parser.add_argument("-p", "--prefix", metavar='PREFIX', default="/", help="Bot prefix. Used to invoke the bot commands. Defaults to /")
args = parser.parse_args()
token, prefix = args.token, args.prefix

intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.change_presence(activity=discord.Game(name=f"{prefix}help for info"))


for filename in os.listdir("./utils"):
	if filename.endswith(".py"):
		bot.load_extension(f"utils.{filename[:-3]}")


bot.run(token)

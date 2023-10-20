import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs.newgame import NewGameCog

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():

    await bot.add_cog(NewGameCog(bot))
    print("NewGameCog :: LOADED")
    print("Bot is ready to be used!")

if __name__ == "__main__":
    bot.run(token)
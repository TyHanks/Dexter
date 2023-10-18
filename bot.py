import discord 
import os
import requests
import json
from random import randrange
from discord.ext import commands
from dotenv import load_dotenv 

load_dotenv() 
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ::Tells if bot is ready::
@bot.event
async def on_ready():
    print("Bot is ready to be used!")

# ::Commands::
#-INFO- Start new game of whos that pokemon
@bot.command()
async def new_game(ctx):

    '''Selects random pokemon number from 0 to 1017'''
    pokemon_number = randrange(1018)

    '''Pull Main Pokemon data from api'''
    pokemon_res_main = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/')
    pokemon_data_main = pokemon_res_main.text
    parse_main = json.loads(pokemon_data_main)

    '''Pokemon Name'''
    pokemon_name = parse_main['name']

    '''Pokemon Image'''
    pokemon_url = parse_main['sprites']['other']['official-artwork']['front_default']
    pokemon_image = pokemon_url

    await ctx.send(f"Pokemon to guess would be {pokemon_name} which is number {pokemon_number}")
    await ctx.send(pokemon_image)

# ::Handles messages if not from the bot::
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

bot.run(token)
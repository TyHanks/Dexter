import requests
import sqlite3
from discord.ext import commands
from random import randrange

class NewGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startgame(self, ctx):
        print("::COMMAND:: -!startgame- Triggered")

        '''Selects random pokemon number from 0 to 1017'''
        pokemon_number = randrange(1018)

        '''Connect to database and create table if needed'''
        connection = sqlite3.connect("data/pokeapi_logged.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pokemon_data (id INTEGER PRIMARY KEY, name TEXT, pokedex_number INTEGER, hint1 TEXT, hint2 TEXT, hint3 TEXT, pokedex_image TEXT)''')

        '''Check if there is a exsisting user in db table log'''
        cursor.execute("SELECT id FROM pokemon_data WHERE pokedex_number = ?", (pokemon_number,))
        exsisting_pokedex_number = cursor.fetchone()

        if exsisting_pokedex_number: # Pull pokemon data from database
            cursor.execute("SELECT * FROM pokemon_data WHERE pokedex_number = ?", (pokemon_number,))
        else: # Otherwise log pokemon data into database

            # Pull main pokemon data from api
            pokemon_res_main = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/')

            if pokemon_res_main.status_code == 200: # Connection to api sucessful 
                pokemon_data_main = pokemon_res_main.json()
            else: # Connection to api failed
                await ctx.send("Failed to fetch Pokémon data.")
                return

            '''Pokemon Name'''
            pokemon_name = pokemon_data_main['name']

            '''Pokemon Hint 1 ability'''
            pokemon_hint1 = pokemon_data_main['abilities'][0]['ability']['name']

            '''Pokemon Hint 2 type'''
            pokemon_hint2 = pokemon_data_main['types'][0]['type']['name']

            '''Pokemon Hint 3 type 2'''
            if len(pokemon_data_main['types']) >= 2:
                pokemon_hint3 = pokemon_data_main['types'][1]['type']['name']
            else:
                pokemon_hint3 = "No more hints"

            '''Pokemon Image'''
            pokemon_url = pokemon_data_main['sprites']['other']['official-artwork']['front_default']
            pokemon_image = pokemon_url

            '''Insert Pokemon data to db'''
            cursor.execute("INSERT INTO pokemon_data (name, pokedex_number, hint1, hint2, hint3, pokedex_image) VALUES (?, ?, ?, ?, ?, ?)", (pokemon_name, pokemon_number, pokemon_hint1, pokemon_hint2, pokemon_hint3, pokemon_image))

        '''Process data into db and close connection to db'''
        connection.commit()
        connection.close()

        await ctx.send("New game of Who's that pokemon? has started if you need a list of commands enter !howtoplay")
        

def setup(bot):
    bot.add_cog(NewGameCog(bot))


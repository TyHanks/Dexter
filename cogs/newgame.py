from discord.ext import commands
import requests
from random import randrange

class NewGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newgame(self, ctx):
        print("::COMMAND:: -!newgame- Triggered")

        '''Selects random pokemon number from 0 to 1017'''
        pokemon_number = randrange(1018)

        '''Pull Main Pokemon data from api'''
        pokemon_res_main = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/')
        if pokemon_res_main.status_code == 200:
            pokemon_data_main = pokemon_res_main.json()
        else:
            await ctx.send("Failed to fetch Pokémon data.")
            return

        '''Pokemon Name'''
        pokemon_name = pokemon_data_main['name']

        '''Pokemon Image'''
        pokemon_url = pokemon_data_main['sprites']['other']['official-artwork']['front_default']
        pokemon_image = pokemon_url

        await ctx.send(f"Pokemon to guess would be {pokemon_name} which is number {pokemon_number}")
        await ctx.send(pokemon_image)

def setup(bot):
    bot.add_cog(NewGameCog(bot))


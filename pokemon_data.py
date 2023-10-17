import urllib.request
import json

def get_pokemon_info(dexnum: int) -> dict:
    """
    Returns a dict with information from PokeAPI about specified Pokemon
    num: int
    name: str
    genus: str
    entry: str
    """
    link = f"https://pokeapi.co/api/v2/pokemon-species/{dexnum}"
    request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(request)
    result = json.loads(response.read())

    data = dict()
    data["num"] = dexnum

    name_information = result["names"]
    for name in name_information:
        if name["language"]["name"] == "en":
            data["name"] = name["name"].strip()
            break

    general_information = result["genera"]
    for information in general_information:
        if information["language"]["name"] == "en":
            data["genus"] = information["genus"].strip()
            break

    dex_entry = result["flavor_text_entries"]
    for entry in dex_entry:
        if entry["language"]["name"] == "en":
            data["entry"] = entry["flavor_text"].strip().replace("\n", " ").replace("\x0c", " ")
            break

    return data

if __name__ == "__main__":
    print(get_pokemon_info(6))

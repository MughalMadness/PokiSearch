import requests
from http import HTTPStatus

def fetch_data(url):
    r = requests.get(url)
    return r

def checkResponseStatus(status):
    print(HTTPStatus(status).phrase)

base = 'https://pokeapi.co/api/v2/'

if __name__ == "__main__":

    print("Welcome to the Pokemon Database!")
    while True:
        print("\n1. Fetch Pokemon Data")
        print("2. Fetch Ability Data")
        print("3. Exit")
        choice = str(input("Enter your choice (1-3): "))

        if choice == '1':
            pokemon_name = input("Enter the name of Pokemon:(i.e pikachu,ditto)")
            url = base + "pokemon/" + pokemon_name.lower()

        elif choice == '2':
            pokemon_ability = input("Enter the name/id of Ability:(i.e limber)")
            url = base + "ability/" + pokemon_ability.lower()

        elif choice == '3':
            print("Thanks for using pokemon Database!")
            break
        else:
            print("Invalid Input(Enter a number from 1-3)")
            continue

        r = fetch_data(url)
        if r.status_code != 200:
            checkResponseStatus(r.status_code)

        data = r.json()

        if choice == '1':
            print(f"\nThe Information about {pokemon_name}")
            print(f"Name:",data['forms'][0]['name'],f"(ID:{data['id']})")
            print("Abilities:")
            for i,a in enumerate(data['abilities'],1):
                print(f"{i}:",a['ability']['name'],f"(isHidden:{a['is_hidden']})")

        if choice == '2':
            print(f"\nThe Information about {pokemon_ability}")
            print(f"Name:{data['name']}(ID:{data['id']})")
            print("\nDescription:",data['effect_entries'][1]['effect'])
            print("\nPokemon with this Ability:")
            for i,a in enumerate(data['pokemon'],1):
                name = a['pokemon']['name']
                print(f"{i}:",name)
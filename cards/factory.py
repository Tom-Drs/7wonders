import json
from cards import PrimaryRessource

def get_cards_per_age(age):
    cards = []
    cards_data = get_cards_data()
    ages_data = get_ages_data()
    if age == 1:
        for card in ages_data.get("1").get("3 players"):
            name = card
            production = {ressource for ressource in cards_data.get(card).get("production")}
            cost = {ressource for ressource in cards_data.get(card).get("cost")}
            cards.append(PrimaryRessource(production, name, age, "brown", cost=cost))
    return cards

def get_cards_data():
    with open("cards_details.json", "r") as file:
        return json.load(file)


def get_ages_data():
    with open("ages_details.json", "r") as file:
        return json.load(file)

if __name__ == "__main__":
    print(get_cards_per_age(1))

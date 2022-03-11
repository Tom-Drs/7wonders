import json

from cards import *


def get_cards_per_age(age):
    cards = []
    cards_data = get_cards_data()
    ages_data = get_ages_data()
    if age == 1:
        for card in ages_data.get("1").get("3 players"):
            if cards_data.get(card).get("type") == "Raw Materials":
                name = card
                production = {key:value for key, value in cards_data.get(card).get("production").items()}
                cost = {key:value for key,value in cards_data.get(card).get("cost").items()}
                cards.append(RawMaterials(production, name, age, "brown", cost=cost))
            if cards_data.get(card).get("type") == "Manufactured Goods":
                name = card
                production = {key:value for key, value in cards_data.get(card).get("production").items()}
                cost = {key:value for key,value in cards_data.get(card).get("cost").items()}
                cards.append(ManufacturedGoods(production, name, age, "grey", cost=cost))

    return cards

def get_cards_data():
    with open("P:\\Documents\\Terminale\\NSI\\7Wonders\\cards\\cards_details.json", "r") as file:
        return json.load(file)


def get_ages_data():
    with open("P:\\Documents\\Terminale\\NSI\\7Wonders\\cards\\ages_details.json", "r") as file:
        return json.load(file)

if __name__ == "__main__":
    print(get_cards_per_age(1))

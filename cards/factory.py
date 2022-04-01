import json
from cards.cards import *


def get_cards_per_age(age):
    cards = []
    cards_data = get_cards_data()
    ages_data = get_ages_data()
    if age == 1:
        for card in ages_data.get("1").get("3 players"):
            if cards_data.get(card).get("type") == "Raw Materials":
                cards.append(get_raw_materials(cards_data, card, age))
            elif cards_data.get(card).get("type") == "Manufactured Goods":
                cards.append(get_manufactured_goods(cards_data, card, age))
            elif cards_data.get(card).get("type") == "Civilian Structures":
                cards.append(get_civilian_structures(cards_data, card, age))
            elif cards_data.get(card).get("type") == "Military Structures":
                cards.append(get_military_structures(cards_data, card, age))
            elif cards_data.get(card).get("type") == "Scientific Structures":
                cards.append(get_scientific_structures(cards_data, card, age))
            elif cards_data.get(card).get("type") == "Commercial Structures":
                cards.append(get_commercial_structures(cards_data, card, age))
    return cards


def get_cards_data():
    with open("cards/cards_details.json", "r") as file:
        return json.load(file)


def get_ages_data():
    with open("cards/ages_details.json", "r") as file:
        return json.load(file)


def get_raw_materials(cards_data, card, age):
    production = {key: value for key, value in cards_data.get(card).get("production").items()}
    cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
    return RawMaterials(production, card, age, "brown", cost=cost)


def get_manufactured_goods(cards_data, card, age):
    production = {key: value for key, value in cards_data.get(card).get("production").items()}
    cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
    return ManufacturedGoods(production, age, age, "grey", cost=cost)


def get_civilian_structures(cards_data, card, age):
    victory_points = cards_data.get(card)["victory_points"]
    cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
    return CivilianStructures(victory_points, card, age, "blue", cost=cost)


def get_military_structures(cards_data, card, age):
    war_points = cards_data.get(card)["war_points"]
    cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
    return MilitaryStructures(war_points, card, age, "red", cost=cost)


def get_scientific_structures(cards_data, card, age):
    symbol = cards_data.get(card)["symbol"]
    cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
    return ScientificStructures(symbol, card, age, "green", cost=cost)


def get_commercial_structures(cards_data, card, age):
    effect = cards_data.get(card)["effect"]
    cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
    return CommercialStructures(effect, card, age, "yellow", cost=cost)


if __name__ == "__main__":
    print(get_cards_per_age(1))

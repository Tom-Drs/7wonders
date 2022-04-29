import json
from cards.cards import *


class Factory():
    def __init__(self):
        self.cards = []
        self.cards_data = self.get_cards_data()
        self.ages_data = self.get_ages_data()

    def get_cards_per_age(self, age, number_players):
        if age == 1:
            for card in self.ages_data.get("1").get(f"{number_players} players"):
                if self.cards_data.get(card).get("type") == "Raw Materials":
                    self.cards.append(self.get_raw_materials(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Manufactured Goods":
                    self.cards.append(self.get_manufactured_goods(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Civilian Structures":
                    self.cards.append(self.get_civilian_structures(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Military Structures":
                    self.cards.append(self.get_military_structures(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Scientific Structures":
                    self.cards.append(self.get_scientific_structures(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Reduction Structures":
                    self.cards.append(self.get_reduction_structures(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Gold Card Structures":
                    self.cards.append(self.get_gold_card_structures(self.cards_data, card, age)) 
                elif self.cards_data.get(card).get("type") == "Product Commercial Structures":
                    self.cards.append(self.get_product_commercial_structures(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Gold Card Neighbour Structures":
                    self.cards.append(self.get_gold_card_neighbour_structures(self.cards_data, card, age))
                elif self.cards_data.get(card).get("type") == "Gold Structures":
                    self.cards.append(self.get_gold_structures(self.cards_data, card, age))        


    def get_cards_data(self):
        with open("cards/cards_details.json", "r") as file:
            return json.load(file)


    def get_ages_data(self):
        with open("cards/ages_details.json", "r") as file:
            return json.load(file)


    def get_raw_materials(self, cards_data, card, age):
        production = {key: value for key, value in cards_data.get(card).get("production").items()}
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return RawMaterials(production, card, age, "brown", cost=cost)


    def get_manufactured_goods(self, cards_data, card, age):
        production = {key: value for key, value in cards_data.get(card).get("production").items()}
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return ManufacturedGoods(production, card, age, "grey", cost=cost)


    def get_civilian_structures(self, cards_data, card, age):
        victory_points = cards_data.get(card)["victory points"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return CivilianStructures(victory_points, card, age, "blue", cost=cost)


    def get_military_structures(self, cards_data, card, age):
        war_points = cards_data.get(card)["war points"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return MilitaryStructures(war_points, card, age, "red", cost=cost)


    def get_scientific_structures(self, cards_data, card, age):
        symbol = cards_data.get(card)["symbol"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return ScientificStructures(symbol, card, age, "green", cost=cost)


    def get_reduction_structures(self, cards_data, card, age):
        effect = cards_data.get(card)["effect"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return ReductionStructures(effect, card, age, "yellow", cost=cost)


    def get_gold_structures(self, cards_data, card, age):
        effect = cards_data.get(card)["effect"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return GoldStructures(effect, card, age, "yellow", cost=cost) 


    def get_gold_card_structures(self, cards_data, card, age):
        effect = cards_data.get(card)["effect"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return GoldCardStructures(effect, card, age, "yellow", cost=cost) 


    def get_product_commercial_structures(self, cards_data, card, age):
        effect = cards_data.get(card)["effect"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return ProductCommercialStructures(effect, card, age, "yellow", cost=cost)  


    def get_gold_card_neighbour_structures(self, cards_data, card, age):
        effect = cards_data.get(card)["effect"]
        cost = {key: value for key, value in cards_data.get(card).get("cost").items()}
        return GoldCardNeighbourStructures(effect, card, age, "yellow", cost=cost)            

import copy
import inspect
from decks import Deck

class Player:
    """ Player class to get all information"""

    def __init__(self, id, hand_cards, wonder, engine, left_neighbor_id, right_neighbor_id):

        self.id = id
        self.gold = 3
        self.hand_cards = hand_cards
        self.placed_cards = Deck()
        self.bought_cards = Deck()
        self.engine = engine
        self.wonder = wonder
        self.victory_points = 0
        self.symbols = {}
        self.war_points = 0

        self.reduction_rawmaterials = {"left_neighbor": 0, "right_neighbor": 0}
        self.reduction_manufactured_goods = 0
        self.left_neighbor_id = left_neighbor_id
        self.right_neighbor_id = right_neighbor_id

    def play(self):
        self.print_data()
        card_number = input(f"Quelle carte voulez vous jouer ? ({self.id})")
        if card_number == "b":
            return self.engine.create_backup()
        card_number = int(card_number)
        while not 0 <= card_number < len(self.hand_cards):
            card_number = int(
                input(f"Quelle carte voulez vous jouer ? ({self.id})"))
        return self.send_card(card_number)

    def send_card(self, card_number):
        self.engine.receive_card(self.id, self.hand_cards[card_number])

    def print_data(self):
        print("------------")
        for i in inspect.getmembers(self):
            i = list(i)
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    if i[0] == "hand_cards" or i[0] == "placed_cards":
                        i[1] = [card.name for card in i[1]]
                    print(i)

    def get_data(self):
        player_data = {}
        for data in inspect.getmembers(self):
            if not data[0].startswith('_') and not inspect.ismethod(data[1]):
                player_data.update({data[0]: data[1]})
        return player_data

    def can_put_card(self, card):
        cost = card.cost
        if self.placed_cards.has_card(card):
            return False
        if cost == {}:
            return True
        elif cost.get("gold"):
            if cost.get("gold") > self.gold:
                return False
            else:
                cost.pop("gold")
        result_placed_cards = self.placed_cards.has_ressources(cost)
        if result_placed_cards is True:
            return True
        else:
            return self.bought_cards.has_ressources(result_placed_cards[1])

    def buy(self, other, indice_card):
        card = other.placed_cards.cards[indice_card]
        if self.engine.has_already_buy(self, other, card):
            return f"Tu as déjà acheté cette carte voleur !"
        if other.id == self.left_neighbor_id:
            reduction_raw_materials = self.reduction_rawmaterials["left_neighbor"]
        else:
            reduction_raw_materials = self.reduction_rawmaterials["right_neighbor"]
        if card.color == 'brown':
            price = 2 - reduction_raw_materials
            if self.gold >= price:
                self.bought_cards.add_card(other.placed_cards.cards[indice_card])
                self.gold -= price
                self.engine.receive_buy_order(self, other, card, price)
                return f"Le joueur {self.id} à acheté la carte {card.name} pour {price} gold au joueur {other.id}"
            else:
                return f"Le joueur {self.id} n'a pas assez d'argent pour acheter cette carte"
        if card.color == 'grey':
            price = 2 - self.reduction_manufactured_goods
            if self.gold >= price:
                self.bought_cards.add_card(card)
                self.gold -= price
                self.engine.receive_buy_order(self, other, card, price)
                return f"Le joueur {self.id} à acheté la carte {card.name} pour {price} gold au joueur {other.id}"
            else:
                return f"Le joueur {self.id} n'a pas assez d'argent pour acheter cette carte"
        else:
            return f"Le joueur {self.id} ne peut pas acheter cette carte"


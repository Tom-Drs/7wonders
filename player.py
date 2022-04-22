import copy
import inspect


class Player:
    """ Player class to get all information"""

    def __init__(self, id, hand_cards, wonder, engine, gold=3, war_points=0):

        self.id = id
        self.gold = gold
        self.hand_cards = hand_cards
        self.war_points = war_points
        self.placed_cards = []
        self.engine = engine
        self.wonder = wonder
        self.bought_card = []
        self.reduction_rawmaterials = 0
        self.reduction_manufacturedgoods = 0

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

    def get_all_resources(self):
        resources_in_possession = {}
        for card in self.placed_cards:
            if card.color == "brown" or card.color == "grey":
                for key, value in card.production.items():
                    if resources_in_possession.get(key) == None:
                        resources_in_possession[key] = value
                    else:
                        resources_in_possession[key] += value
        for index_card in range(len(self.bought_card)):
            if self.bought_card[index_card][0].color == "brown" or self.bought_card[index_card][0].color == "grey":
                for key, value in self.bought_card[index_card][0].production.items():
                    if resources_in_possession.get(key) == None:
                        resources_in_possession[key] = value
                    else:
                        resources_in_possession[key] += value
        resources_in_possession["gold"] = self.gold
        return resources_in_possession

    def is_double(self, card):
        for card_placed in self.placed_cards:
            if card_placed.name == card.name:
                return True
        return False

    def can_put_card(self, card): #A test
        resource = self.get_all_resources()
        cost = card.cost
        if cost == {}:
            return True
        elif list(cost.items())[0][0] == "gold":
            return self.put_with_gold(resource, cost)
        del resource["gold"]
        cost = self.put_with_resource(resource, cost)
        if cost != {}:
            cost = self.put_with_split_resource(resource, cost)
        if cost == {}:
            return True
        return False, cost

    """retrieve information on war points"""

    def current_war_points(self):
        total_war_points = 0
        for card in self.placed_cards:
            if card.color == 'red':
                total_war_points += card.war_points
        self.war_points = total_war_points

    def put_with_gold(self, resource, cost):
        if resource["gold"] >= cost["gold"]:
            return True
        return False

    def put_with_resource(self, resource, cost):
        cost_copy = copy.copy(cost)
        for key, value in resource.items():
            if cost_copy.get(key) != None:
                cost_copy[key] -= value
                if cost_copy[key] == 0:
                    del cost_copy[key]
        return cost_copy

    def put_with_split_resource(self, player_ressources: dict,
                                card_cost: dict) -> dict:
        player_ressources = {key: value for key, value in player_ressources.items() if len(key.split("/")) > 1}
        ensemble = [ressource.split("/") for ressource in player_ressources]
        total_uplets = []
        for number in range(2 ** len(player_ressources)):
            binary_uplet = self.convert_binary(number, bits=len(player_ressources))
            uplet = self.binary_to_uplet(binary_uplet, ensemble)
            total_uplets.append(uplet)
        for uplet in total_uplets:
            if len(self.put_with_resource(uplet, card_cost)) == 0:
                return {}
        if len(total_uplets) == 1:
            return card_cost
        else:
            return min(total_uplets, key=lambda uplet: len(self.put_with_resource(uplet, card_cost)))

    def binary_to_uplet(self, binary_list: list, ensemble: list) -> dict:
        result = {}
        for index, value in enumerate(binary_list):
            if result.get(ensemble[index][value]) is None:
                result.update({ensemble[index][value]: 1})
            else:
                result[ensemble[index][value]] += 1
        return result


    def convert_binary(self, number, bits=8):
        binary = [0 for i in range(bits)]
        index = 0
        while number > 0:
            binary[index] = number % 2
            number //= 2
            index += 1
        return binary

    def buy(self, other, indice_card):
        if other.placed_cards[indice_card].color == 'brown':
            if self.gold >= 2 + self.reduction_rawmaterials:
                self.bought_card.append((other.placed_cards[indice_card],
                                         self.reduction_rawmaterials + 2))
                self.gold -= self.reduction_rawmaterials + 2
            else:
                return f"Le joueur {self.id} n'a pas assez d'argent pour acheter cette carte"
        if other.placed_cards[indice_card].color == 'grey':
            if self.gold >= 2 + self.reduction_manufacturedgoods:
                self.bought_card.append((other.placed_cards[indice_card],
                                         self.reduction_manufacturedgoods + 2))
                self.gold -= self.reduction_manufacturedgoods + 2
            else:
                return f"Le joueur {self.id} n'a pas assez d'argent pour acheter cette carte"
        else:
            return f"Le joueur {self.id} ne peut pas acheter cette carte"

if __name__ == "__main__":
    a = {"ore": 1, "clay": 2}
    b = {"ore": 1}
    t = Player(1, 2, 3, 4)
    t.put_with_resource(a, b)
    print(a)
    print(b)

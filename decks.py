import copy


class Deck:

    def __init__(self):
        self.cards = []
        self.bought_cards = []

    def get_all_resources(self):
        resources_in_possession = {}
        for card in self.cards:
            if card.color == "brown" or card.color == "grey":
                for key, value in card.production.items():
                    if resources_in_possession.get(key) == None:
                        resources_in_possession[key] = value
                    else:
                        resources_in_possession[key] += value
        for index_card in range(len(self.bought_cards)):
            if self.bought_cards[index_card][0].color == "brown" or \
                    self.bought_cards[index_card][0].color == "grey":
                for key, value in self.bought_cards[index_card][0].production.items():
                    if resources_in_possession.get(key) == None:
                        resources_in_possession[key] = value
                    else:
                        resources_in_possession[key] += value
        return resources_in_possession

    def has_card(self, card):
        for deck_card in self.cards:
            if deck_card.name == card.name:
                return True
        return False

    def put_with_resource(self, ressources: dict, cost: dict) -> dict:
        cost_copy = copy.copy(cost)
        for key, value in ressources.items():
            if cost_copy.get(key) != None:
                cost_copy[key] -= value
                if cost_copy[key] == 0:
                    del cost_copy[key]
        return cost_copy

    def put_with_split_resource(self, player_ressources: dict,
                                card_cost: dict) -> dict:
        player_ressources = {key: value for key, value in
                             player_ressources.items() if
                             len(key.split("/")) > 1}
        ensemble = [ressource.split("/") for ressource in player_ressources]
        total_uplets = []
        for number in range(2 ** len(player_ressources)):
            binary_uplet = self.convert_binary(number,
                                               bits=len(player_ressources))
            uplet = self.binary_to_uplet(binary_uplet, ensemble)
            total_uplets.append(uplet)
        for uplet in total_uplets:
            if len(self.put_with_resource(uplet, card_cost)) == 0:
                return {}
        if len(total_uplets) == 1:
            return card_cost
        else:
            return min(total_uplets, key=lambda uplet: len(
                self.put_with_resource(uplet, card_cost)))

    def binary_to_uplet(self, binary_list: list, ensemble: list) -> dict:
        result = {}
        for index, value in enumerate(binary_list):
            if result.get(ensemble[index][value]) is None:
                result.update({ensemble[index][value]: 1})
            else:
                result[ensemble[index][value]] += 1
        return result

    def convert_binary(self, number: int, bits: int = 8) -> list:
        binary = [0 for i in range(bits)]
        index = 0
        while number > 0:
            binary[index] = number % 2
            number //= 2
            index += 1
        return binary

    def has_ressources(self, cost):
        resource = self.get_all_resources()
        if cost == {}:
            return True
        cost = self.put_with_resource(resource, cost)
        if cost != {}:
            cost = self.put_with_split_resource(resource, cost)
        if cost == {}:
            return True
        return False, cost

    def add_card(self, card):
        self.cards.append(card)

    def delete_card(self, card_name: str):
        for index_card in range(len(self.cards)):
            if self.cards[index_card].name == card_name:
                return self.cards.pop(index_card)

    def add_bought_card(self, card):
        self.bought_cards.append(card)

    def clear_bought_cards(self):
        self.bought_cards = []


    def count_card_by_color(self, color: str) -> int:
        pass
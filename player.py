import inspect 
from pprint import pprint
from typing import List

class Player:
    """ Player class to get all information"""
    def __init__(self, id: int, hand_cards: list, wonder, engine, gold: int=3,
                 war_points: int=0):
        self.id = id
        self.gold = gold
        self.hand_cards = hand_cards
        self.war_points = war_points
        self.placed_cards = []
        self.engine = engine
        self.wonder = wonder

    def play(self):
        self.print_data()
        card_number = input(f"Quelle carte voulez vous jouer ? ({self.id})")
        if card_number == "b":
            return self.engine.create_backup()
        card_number = int(card_number)
        while not 0 <= card_number < len(self.hand_cards):
            card_number = int(input(f"Quelle carte voulez vous jouer ? ({self.id})"))
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


    def get_all_resources(self):
        resources_in_possession = {}
        for card in self.placed_cards:
            if card.color == "brown" or card.color == "grey":
                for key, value in card.production.items():
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
            if resource["gold"] >= cost["gold"]:
                return True
            return False
        del resource["gold"]
        for key, value in resource.items():
            if cost.get(key) != None:
                cost[key] -= value
                if cost[key] == 0:
                    del cost[key]
        resource_split = []
        dico_resource_split = {}
        cpt = 0                      
        for key, value in resource.items():            
            if len(key) > 6:
                resource_split.append(resource[key].split("/"))
                for index in range(len(resource_split[cpt])):
                    if dico_resource_split.get(resource_split[cpt][index]) == None:
                        dico_resource_split[resource_split[cpt][index]] = value
                    else:
                        dico_resource_split[resource_split[cpt][index]] += value
                cpt += 1
        for elt in resource_split:
            if cost.get(elt[0]) != None and cost.get(elt[1]) != None:
                if dico_resource_split[elt[0]] >= dico_resource_split[elt[1]]:
                    cost[elt[1]] -= 1
                    if cost[elt[1]] == 0:
                        del cost[elt[1]] 
                else:
                    cost[elt[0]] -= 1
                    if cost[elt[0]] == 0:
                        del cost[elt[0]]
            elif cost.get(elt[0]) != None:
                cost[elt[0]] -= 1
                if cost[elt[0]] == 0:
                    del cost[elt[0]] 
            elif cost.get(elt[1]) != None:
                cost[elt[1]] -= 1
                if cost[elt[1]] == 0:
                    del cost[elt[1]]                 
        if cost == {}:
            return True
        return False

    """retrieve information on war points"""
    def current_war_points():
        pass

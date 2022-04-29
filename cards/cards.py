import inspect
from abc import ABC, abstractmethod


class Card(ABC):
    """Create card """
    def __init__(self, name, age, color, cost=None, chain_list=None):
        self.name = name
        self.age = age
        self.color = color
        self.cost = cost
        self.chain_list = chain_list


    def get_data(self):
        player_data = {}
        for data in inspect.getmembers(self):
            if not data[0].startswith('_') and not inspect.ismethod(data[1]):
                player_data.update({data[0]: data[1]})
        return player_data


    @abstractmethod
    def play(self, player):
        pass    


class RawMaterials(Card):
    """Create card of primary resource"""
    def __init__(self, production, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.production = production


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        if self.cost.get("gold") != None:
            self.player.gold -= self.cost.get("gold")    


class ManufacturedGoods(Card):
    """Create card of advanced resource"""
    def __init__(self, production, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.production = production


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)    


class CivilianStructures(Card):
    """Create card of civil building"""
    def __init__(self, victory_points, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.victory_points = victory_points


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        player.victory_points += self.victory_points    


class MilitaryStructures(Card):
    """Create card of military building"""
    def __init__(self, war_points, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.war_points = war_points

        
    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        player.war_points += self.war_points     


class ScientificStructures(Card):
    """Create card of scientific building"""
    def __init__(self, symbol, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.symbol = symbol


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        if player.symbol.get(self.symbol) == None:
            player.symbol.update({self.symbol: 1})
        else:
            player.symbol[self.symbol] += 1       


class ReductionStructures(Card):
    def __init__(self, effect, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.effect = effect
        

    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        if self.effect == "reduction_rawmaterials_nl":
            player.reduction_rawmaterials["left_neighbour"] -= 1
        elif self.effect == "reduction_rawmaterials_nr":
            player.reduction_rawmaterials["right_neighbour"] -= 1
        elif self.effect == "reduction_manufactured":
            player.reduction_manufacturedgoods -= 1


class GoldStructures(Card):
    def __init__(self, effect, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.effect = effect


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        player.gold += self.effect


class GoldCardStructures(Card):
    def __init__(self, effect, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.effect = effect


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        if self.effect == "brown":
            number_brown_card = player.placed_cards.count_card_by_color("brown")
            player.gold += number_brown_card
            player.victory_points += number_brown_card
        elif self.effect == "yellow":    
            number_yellow_card = player.placed_cards.count_card_by_color("yellow")
            player.gold += number_yellow_card
            player.victory_points += number_yellow_card
        elif self.effect == "grey":    
            number_grey_card = player.placed_cards.count_card_by_color("grey")
            player.gold += 2*number_grey_card
            player.victory_points += 2*number_grey_card    


class ProductCommercialStructures(Card):
    def __init__(self, effect, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.effect = effect


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        ##################################################################################################################################################### A voir avec Tom    


class GoldCardNeighbourStructures(Card):
    def __init__(self, effect, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.effect = effect


    def play(self, player):
        player.placed_cards.add_card(self) 
        player.hand_cards.delet_card(self.name)
        if self.effect == "brown":
            number_brown_card = player.placed_cards.count_card_by_color("brown")
            left_neighbour = player.engine.get_player_by_id(player.id-1%player.engine.number_player, player.engine.players)
            number_brown_left_neighbour_card = left_neighbour.placed_cards.count_card_by_color("brown")
            right_neighbour = player.engine.get_player_by_id(player.id+1%player.engine.number_player, player.engine.players)
            number_brown_right_neighbour_card = right_neighbour.placed_cards.count_card_by_color("brown")
            player.gold += number_brown_card + number_brown_left_neighbour_card + number_brown_right_neighbour_card
        elif self.effect == "grey":
            number_grey_card = player.placed_cards.count_card_by_color("grey")
            left_neighbour = player.engine.get_player_by_id(player.id-1%player.engine.number_player, player.engine.players)
            number_grey_left_neighbour_card = left_neighbour.placed_cards.count_card_by_color("grey")
            right_neighbour = player.engine.get_player_by_id(player.id+1%player.engine.number_player, player.engine.players)
            number_grey_right_neighbour_card = right_neighbour.placed_cards.count_card_by_color("grey")
            player.gold += 2*(number_grey_card + number_grey_left_neighbour_card + number_grey_right_neighbour_card) 
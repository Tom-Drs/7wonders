class Card:
    """Create card """
    def __init__(self, name, age, color, cost=None, chain_list=None):
        self.name = name
        self.age = age
        self.color = color
        self.cost = cost
        self.chain_list = chain_list


class RawMaterials(Card):
    """Create card of primary resource"""
    def __init__(self, production, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.production = production


class ManufacturedGoods(Card):
    """Create card of advanced resource"""
    def __init__(self, production, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.production = production


class CivilianStructures(Card):
    """Create card of civil building"""
    def __init__(self, victory_points, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.victory_points = victory_points


class MilitaryStructures(Card):
    """Create card of military building"""
    def __init__(self, war_points, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.war_points = war_points


class ScientificStructures(Card):
    """Create card of scientific building"""
    def __init__(self, symbol, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.symbol = symbol


class CommercialStructures(Card):
    """Create card of trade building"""
    def __init__(self, effect, name, age, color, cost=None, chain_list=None):
        Card.__init__(self, name, age, color, cost, chain_list)
        self.effect = effect


class Wonder:
    def __init__(self, name, production):
        self.name = name
        self.production = production

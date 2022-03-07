class Card():
    """Create card """
    def __init__(self, name, age, color, cost=None, chain_list=None, players=None):
        self.name = name
        self.age = age
        self.color = color
        self.cost = cost
        self.chain_list = chain_list
        self.players = players


class PrimaryRessource(Card):
    """Create card of primary ressource"""
    def __init__(self, production, name, age, color, cost=None, chain_list=None, players=None):
        Card.__init__(self, name, age, color, cost, chain_list, players)
        self.production = production


class AdvancedRessource(Card):
    """Create card of advanced ressource"""
    def __init__(self, production, name, age, color, cost=None, chain_list=None, players=None):
        Card.__init__(self, name, age, color, cost, chain_list, players)
        self.production = production


class CivilBuilding(Card):
    """Create card of civil building"""
    def __init__(self, victory_points, name, age, color, cost=None, chain_list=None, players=None):
        Card.__init__(self, name, age, color, cost, chain_list, players)
        self.victory_points = victory_points


class MilitaryBuilding(Card):
    """Create card of military building"""
    def __init__(self, war_points, name, age, color, cost=None, chain_list=None, players=None):
        Card.__init__(self, name, age, color, cost, chain_list, players)
        self.war_points = war_points


class ScientificBuilding(Card):
    """Create card of scientific building"""
    def __init__(self, symbol, name, age, color, cost=None, chain_list=None, players=None):
        Card.__init__(self, name, age, color, cost, chain_list, players)
        self.symbol = symbol


class TradeBuilding(Card):
    """Create card of trade building"""
    def __init__(self, effect, name, age, color, cost=None, chain_list=None, players=None):
        Card.__init__(self, name, age, color, cost, chain_list, players)


class Wonder():
    def __init__(self, name, production):
        self.name = name
        self.production = production


def create_card():
    return [PrimaryRessource(('wood', 1), 'chantier', 1, 'brown'), PrimaryRessource(('stone', 1), 'cavité', 1, 'brown'),
    PrimaryRessource(('clay', 1), 'bassin argilleux', 1, 'brown'), PrimaryRessource(('ore', 1), 'filon', 1, 'brown'),
    PrimaryRessource((('clay', 'ore'), 1), 'fosse argilleuse', 1, 'brown', cost={'gold': 1}),
    PrimaryRessource((('stone', 'wood'), 1), 'exploitation forestière', 1, 'brown', cost={'gold': 1})]

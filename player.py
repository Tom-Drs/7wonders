class Player():
    """ Player class to get all information"""
    def __init__(self, id, hand_cards, wonder, engine, gold=3, war_points=0,
                 placed_cards=0):

        self.id = id
        self.gold = gold
        self.hand_cards = hand_cards
        self.war_points = war_points
        self.placed_cards = placed_cards
        self.engine = engine
        self.wonder = wonder

    def play(self):
        card_number = int(input(f"Quelle carte voulez vous jouer ? ({self.id})"))
        while not 0 <= card_number < len(self.hand_cards):
            card_number = int(input(f"Quelle carte voulez vous jouer ? ({self.id})"))
        return self.send_card(card_number)

    def send_card(self, card_number):
        self.engine.receive_card(self, self.hand_cards[card_number])
        
    def print_data(self):
        print("------------")
        for i in inspect.getmembers(self):
            i = list(i)
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    if i[0] == "hand_cards" or i[0] == "placed_cards":
                        i[1] = [card.name for card in i[1]]
                    print(i)



#fonction non testée et pas sûre
    def get_all_resources(self):
        resources_in_possession = {}
        for card in self.placed_cards:
            card.production
            resources_in_possession [card] = card.production
        return resources_in_possession

    def is_double(self, card):
        for card_placed in self.placed_cards():
            if card_placed.name == card.name:
                return False
        return False


    """retrieve information on war points"""
    def current_war_points():
        pass

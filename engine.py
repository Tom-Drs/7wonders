from player import Player
from cards.cards import create_card
from pprint import pprint


class GameEngine:

    def __init__(self, number_player=3):
        self.number_player = number_player
        self.players = []
        self.cards = []
        self.current_age = 1
        self.create_players()
        self.cards_deposit = []

    def create_players(self):
        for player_id in range(self.number_player):
            cards = create_card()
            new_player = Player(id=player_id, hand_cards=cards, engine=self,
                                wonder=None)
            self.players.append(new_player)

    def wait_players(self):
        for player in self.players:
            player.play()

    def receive_card(self, player_id: int, card):
        player = self.get_player_by_id(player_id)
        if player is None:
            raise Exception("Player not found with id.")
        if player.can_put_card(card):
            self.cards_deposit.append(card, player)

    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def play_current_round(self):
        for i in range(7):
            self.wait_players()
            if len(self.cards_deposit) == self.number_player:
                self.copy_state = self.get_copy_state()
                for card, player in self.cards_deposit:
                    player.placed_cards.append(card)
                    for card_index in range(len(player.hand_cards)):
                        if card.name == player.hand_cards[card_index]:
                            player.hand_cards.pop(card_index)
                    player.print_data()
            self.next_state()
            self.cards_deposit = []

    
    def next_state(self):
        self.players = []
        for player in self.copy_state:
            self.players.append(player)

    def get_copy_state(self):
        return [player for player in self.players]

    # def get_player_in_copy_state(self, player):
    #     for new_player in self.copy_state:
    #         if player.id == new_player.id:
    #             return new_player
    #     return None
    
    def creat_stack_cards(self, age, players):
        cards = get_cards_per_age(age)
        number_cards = len(cards)/players
        for player in range(players):
            for k in range(number_cards):
                random = randint(0, len(cards)-1)           
                self.get_player_by_id(player).hand_cards.append(cards[random])
                cards.pop(random)



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
        self.wait_players()
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
            self.cards_deposit.append(card)

    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def play_current_round(self):



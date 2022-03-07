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

    def create_players(self):
        for player_id in range(self.number_player):
            cards = create_card()
            new_player = Player(id=player_id, hand_cards=cards, engine=self,
                                wonder=None)
            self.players.append(new_player)

    def wait_players(self):
        for player in self.players:
            player.play()

    def receive_card(self, player, card):
        print(card.name)
        print(player.id)
        for hand_card_index in range(len(player.hand_cards)):
            if player.hand_cards[hand_card_index].name == card.name:
                player.hand_cards.pop(hand_card_index)
                pprint(player.hand_cards)
                return


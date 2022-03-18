from player import Player
from pprint import pprint
from cards.factory import get_cards_per_age
from random import randint


class GameEngine:

    def __init__(self, number_player=3):
        self.number_player = number_player
        self.players = []
        self.cards = []
        self.current_age = 1
        self.copy_state
        self.create_players()
        self.cards_deposit = []
        self.allocate_decks(1, 3)
        self.play_current_round()

    def create_players(self):
        for player_id in range(self.number_player):
            new_player = Player(id=player_id, hand_cards=[], engine=self,
                                wonder=None)
            self.players.append(new_player)

    def wait_players(self):
        for player in self.players:
            player.play()

    def receive_card(self, player_id: int, card):
        player = self.get_player_by_id(player_id, self.players)
        if player is None:
            raise Exception("Player not found with id.")
        if not player.is_double(card):
            self.cards_deposit.append((card, player))

    def get_player_by_id(self, player_id: int, players_list: list):
        """Method to get player in a list with an id."""
        for player in players_list:
            if player.id == player_id:
                return player
        return None

    def play_current_round(self):
        for i in range(7):
            self.wait_players()
            if len(self.cards_deposit) == self.number_player:
                self.copy_state = self.get_copy_state()
                for card, player in self.cards_deposit:
                    current_player = self.get_player_by_id(player.id,
                                                           self.copy_state)
                    current_player.placed_cards.append(card)
                    for card_index in range(len(player.hand_cards)):
                        if card.name == current_player.hand_cards[
                            card_index].name:
                            current_player.hand_cards.pop(card_index)
                            break
                    current_player.print_data()
            self.next_state()
            self.cards_deposit = []
            self.switch_decks()

    def next_state(self):
        self.players = []
        for player in self.copy_state:
            self.players.append(player)

    def get_copy_state(self) -> list:
        return [player for player in self.players]

    def allocate_decks(self):
        """Method to allocate decks for each player."""
        cards = get_cards_per_age(self.current_age)
        number_cards = int(len(cards) / self.number_player)
        for player in range(self.number_player):
            for _ in range(number_cards):
                random = randint(0, len(cards) - 1)
                self.get_player_by_id(player, self.players).hand_cards.append(
                    cards[random])
                cards.pop(random)

    def switch_decks(self):
        """Method to switching decks between players."""
        decks = []
        if self.current_age % 2 == 1:
            for player_index in range(len(self.players) - 1):
                decks.append(self.players[player_index].hand_cards)
            decks.insert(0, self.players[-1].hand_cards)
        if self.current_age % 2 == 0:
            for player_index in range(len(self.players) - 1, 0, -1):
                decks.insert(0, self.players[player_index].hand_cards)
            decks.append(self.players[0].hand_cards)
        for index in range(len(self.players)):
            self.players[index].hand_cards = decks[index]

    def can_put_card(self, card, player):
        resource = player.get_all_resources()
        cost = card.cost
        pass  # comparer les ressources avec le prix de la carte

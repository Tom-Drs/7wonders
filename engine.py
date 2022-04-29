from player import Player
from cards.factory import Factory


from random import randint
from os import path
import pickle


class GameEngine:

    def __init__(self, number_player: int=3):
        self.number_player = number_player
        self.players = []
        self.cards = []
        self.current_age = 1
        self.round = 1
        self.copy_state = 0
        self.discard = []
        self.create_players()
        self.cards_deposit = []
        self.allocate_decks()

    def create_players(self):
        """Method to create player objects."""
        for player_id in range(self.number_player):
            new_player = Player(id=player_id, hand_cards=[], engine=self,
                                wonder=None)
            self.players.append(new_player)

    def wait_players(self):
        """Method to call the play method for each player."""
        for player in self.players:
            player.play()

    def receive_card(self, player_id: int, card):
        """Method call when a player wants to play a card."""
        player = self.get_player_by_id(player_id, self.players)
        card = player.hand_cards[card]
        if player is None:
            raise Exception("Player not found with id.")
        if self.player_has_already_played(player_id):
            return f"Le joueur {player_id} a deja verouille un coup"
        if player.is_double(card):
            return f"Le joueur {player_id} ne peut pas poser 2x la meme carte sur le plateau"
        result_can_put_card = player.can_put_card(card)
        if type(result_can_put_card) == tuple:
            return f"Le joueur {player_id} ne peut pas jouer la carte {card.name} car il lui manque {result_can_put_card[1]}"
        self.cards_deposit.append((card, player))
        player.bought_card = []
        if len(self.cards_deposit) == self.number_player:
            self.play_current_round()
            return(f"Le joueur {player.id} a vérouillé la carte {card.name} et la manche a ete joue")
        return(f"Le joueur {player.id} a vérouillé la carte {card.name}")

    def player_has_already_played(self, player_id):
        locked_player = [move[1].id for move in self.cards_deposit]
        if player_id in locked_player:
            return True
        return False

    def get_player_by_id(self, player_id: int, players_list: list=None):
        """Method to get player in the player list with an id."""
        if players_list is None:
            players_list = self.players
        for player in players_list:
            if player.id == player_id:
                return player
        return None

    def play_current_round(self):
        """Method to play a round."""
        if len(self.cards_deposit) == self.number_player:
            self.copy_state = self.get_copy_state()
            for card, player in self.cards_deposit:
                current_player = self.get_player_by_id(player.id,
                                                       self.copy_state)
                current_player.placed_cards.append(card)
                current_player.current_war_points()
                for card_index in range(len(player.hand_cards)):
                    if card.name == current_player.hand_cards[card_index].name:
                        current_player.hand_cards.pop(card_index)
                        break
        self.next_state()
        self.cards_deposit = []
        self.set_next_round()

    def set_next_round(self):
        self.round += 1
        if self.round == 7:
            for player in self.players:
                self.discard.append(player.hand_cards[0])
            self.allocate_decks()
            self.current_age += 1
            self.round = 1
        else:
            self.switch_decks()

    def next_state(self):
        """Method to transfert the state copy in the main state."""
        self.players = []
        for player in self.copy_state:
            self.players.append(player)

    def get_copy_state(self) -> list:
        return [player for player in self.players]

    def allocate_decks(self):
        """Method to allocate decks for each player."""
        factory = Factory()
        cards = factory.get_cards_per_age(self.current_age, self.number_player)
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
        
    def create_backup(self, name):
        index = 0
        if path.exists(f"backups/{name}.pickle"):
            return "Une backup porte deja ce nom"
        with open(f"backups/{name}.pickle", "wb") as file:
            game = pickle.dump(self, file)
        print(f"Etat copie dans le fichier backups/{name}.pickle")
        exit(0)
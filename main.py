import pickle

from engine import GameEngine


if __name__ == '__main__':
    answer_backup = input("Voulez vous charger une backup ? (n / index) ")
    if answer_backup == "n":
        game = GameEngine()
    else:
        with open(f"backups/state{answer_backup}.pickle", "rb") as file:
            game = pickle.load(file)
            game.play_current_round()
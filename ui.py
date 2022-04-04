import sys
from PySide6 import QtWidgets
from PySide6.QtGui import QShortcut, QKeySequence
from cards.factory import get_cards_per_age
import inspect
from engine import GameEngine
from cards.cards import Card
import pickle

class MainWindow(QtWidgets.QWidget):
    def __init__(self):

        super().__init__()
        self.resize(1000, 1000)
        self.setWindowTitle("Seven Wonders")
        self.engine = GameEngine()
        self.setup_ui()


    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.button = QtWidgets.QPushButton("Valider")
        self.input = QtWidgets.QLineEdit()

        self.player_0_tree = self.create_player_tree(0)
        self.player_1_tree = self.create_player_tree(1)
        self.player_2_tree = self.create_player_tree(2)

    def modify_widgets(self):
        pass

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.player_0_tree, 0, 0)
        self.main_layout.addWidget(self.player_1_tree, 0, 1)
        self.main_layout.addWidget(self.player_2_tree, 1, 0)
        self.main_layout.addWidget(self.button, 2, 1)
        self.main_layout.addWidget(self.input, 2, 0)

    def setup_connections(self):
        self.button.clicked.connect(self.play)
        QShortcut(QKeySequence("Enter"), self, self.play)

    def play(self):
        result = self.input.text().split()
        if result[0] == "b":
            self.engine.create_backup()
        if result[0] == "l":
            with open(f"backups/state{result[1]}.pickle", "rb") as file:
                self.engine = pickle.load(file)
                self.reload()
                return
        if len(self.engine.cards_deposit) == 2:
            self.engine.receive_card(int(result[0]), int(result[1]))
            self.reload()
            return
        self.engine.receive_card(int(result[0]), int(result[1]))

    def reload(self):
        self.clearLayout()
        self.create_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def clearLayout(self, layout=0):
        layout = self.main_layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def create_player_tree(self, player_id):
        player = self.engine.get_player_by_id(player_id)
        player_data = player.get_data()
        items = []
        for key, value in player_data.items():
            if key == "hand_cards" or key == "placed_cards":
                item = QtWidgets.QTreeWidgetItem(None, [key])
                for card in value:
                    card_item = QtWidgets.QTreeWidgetItem(None, [card.name])
                    card_data = card.get_data()
                    for attribute_key, attribute_value in card_data.items():
                        content = QtWidgets.QTreeWidgetItem(None, [f"{attribute_key} : {attribute_value}"])
                        card_item.addChild(content)
                    item.addChild(card_item)
                items.append(item)
            else:
                items.append(QtWidgets.QTreeWidgetItem(None, [f"{key} : {value}"]))
        widget = QtWidgets.QTreeWidget()
        widget.setHeaderLabel(f"Player {player_id}")
        widget.insertTopLevelItems(0, items)
        return widget
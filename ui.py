import sys
from PySide6 import QtWidgets
from cards.factory import get_cards_per_age
import inspect
from engine import GameEngine
from cards.cards import Card

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
        self.main_layout.addWidget(self.player_0_tree)
        self.main_layout.addWidget(self.player_1_tree)
        self.main_layout.addWidget(self.player_2_tree)
        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.input)

    def setup_connections(self):
        return self.button.clicked.connect(self.play)

    def play(self):
        result = self.input.text().split()
        if len(self.engine.cards_deposit) == 2:
            self.engine.receive_card(int(result[0]), int(result[1]))
            self.clearLayout()
            self.create_widgets()
            self.add_widgets_to_layouts()
            self.setup_connections()
            return
        self.engine.receive_card(int(result[0]), int(result[1]))

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
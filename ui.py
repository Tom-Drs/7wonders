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
        self.label_info = QtWidgets.QLabel("")

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
        self.main_layout.addWidget(self.label_info, 3, 0)

    def setup_connections(self):
        self.button.clicked.connect(self.play)
        QShortcut(QKeySequence("Enter"), self, self.play)

    def mouseDoubleClickEvent(self, e):
        print(e)

    def play(self):
        result = self.input.text().split()
        if result[0] == "b":
            self.engine.create_backup()
        if result[0] == "l":
            with open(f"backups/state{result[1]}.pickle", "rb") as file:
                self.engine = pickle.load(file)
                self.reload()
                self.label_info.setText(f"La backup {result[1]}.pickle a ete load")
                return
        if len(self.engine.cards_deposit) == 2:
            response = self.engine.receive_card(int(result[0]), int(result[1]))
            self.reload()
            self.label_info.setText(response)
            return
        response = self.engine.receive_card(int(result[0]), int(result[1]))
        self.label_info.setText(response)

    def reload(self):
        self.clear_layout()
        self.create_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def clear_layout(self, layout=0):
        layout = self.main_layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def create_player_tree(self, player_id: int):
        player = self.engine.get_player_by_id(player_id)
        player_data = player.get_data()
        attributes = []
        for player_key, player_value in player_data.items():
            if player_key == "hand_cards" or player_key == "placed_cards":
                item = QtWidgets.QTreeWidgetItem(None, [player_key])
                card_index = 0
                for card in player_value:
                    card_item = QtWidgets.QTreeWidgetItem(None, [f"{card_index} {card.name}"])
                    card_index += 1
                    card_data = card.get_data()
                    for card_key, card_value in card_data.items():
                        content = QtWidgets.QTreeWidgetItem(None, [f"{card_key} : {card_value}"])
                        card_item.addChild(content)
                    item.addChild(card_item)
                attributes.append(item)
            else:
                attributes.append(QtWidgets.QTreeWidgetItem(None, [f"{player_key} : {player_value}"]))
        widget = QtWidgets.QTreeWidget()
        widget.itemDoubleClicked.connect(self.test)
        widget.setHeaderLabel(f"Player {player_id}")
        widget.insertTopLevelItems(0, attributes)
        return widget

    def test(self, d):
        player_id = d.treeWidget().headerItem().text(0).split()[1]
        card_id = d.text(0).split()[0]
        if player_id.isdigit() and card_id.isdigit():
            self.play_double_click(int(player_id), int(card_id))


    def play_double_click(self, player_id, card_id):
        if len(self.engine.cards_deposit) == 2:
            response = self.engine.receive_card(player_id, card_id)
            self.reload()
            self.label_info.setText(response)
            return
        response = self.engine.receive_card(player_id, card_id)
        self.label_info.setText(response)
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class Blackjack(QWidget):
    def __init__(self):
        super().__init__()
        self.balance = 1000
        self.bet = 0

        self.cards = [
            ("cards/2_of_spades.png",2),("cards/3_of_spades.png",3),("cards/4_of_spades.png",4),("cards/5_of_spades.png",5),
            ("cards/6_of_spades.png",6),("cards/7_of_spades.png",7),("cards/8_of_spades.png",8),("cards/9_of_spades.png",9),
            ("cards/10_of_spades.png",10),("cards/jack_of_spades.png",10),("cards/queen_of_spades.png",10),("cards/king_of_spades.png",10),
            ("cards/ace_of_spades.png",11),
            ("cards/2_of_hearts.png",2),("cards/3_of_hearts.png",3),("cards/4_of_hearts.png",4),("cards/5_of_hearts.png",5),
            ("cards/6_of_hearts.png",6),("cards/7_of_hearts.png",7),("cards/8_of_hearts.png",8),("cards/9_of_hearts.png",9),
            ("cards/10_of_hearts.png",10),("cards/jack_of_hearts.png",10),("cards/queen_of_hearts.png",10),("cards/king_of_hearts.png",10),
            ("cards/ace_of_hearts.png",11),
            ("cards/2_of_diamonds.png",2),("cards/3_of_diamonds.png",3),("cards/4_of_diamonds.png",4),("cards/5_of_diamonds.png",5),
            ("cards/6_of_diamonds.png",6),("cards/7_of_diamonds.png",7),("cards/8_of_diamonds.png",8),("cards/9_of_diamonds.png",9),
            ("cards/10_of_diamonds.png",10),("cards/jack_of_diamonds.png",10),("cards/queen_of_diamonds.png",10),("cards/king_of_diamonds.png",10),
            ("cards/ace_of_diamonds.png",11),
            ("cards/2_of_clubs.png",2),("cards/3_of_clubs.png",3),("cards/4_of_clubs.png",4),("cards/5_of_clubs.png",5),
            ("cards/6_of_clubs.png",6),("cards/7_of_clubs.png",7),("cards/8_of_clubs.png",8),("cards/9_of_clubs.png",9),
            ("cards/10_of_clubs.png",10),("cards/jack_of_clubs.png",10),("cards/queen_of_clubs.png",10),("cards/king_of_clubs.png",10),
            ("cards/ace_of_clubs.png",11)
        ]

        self.player_hand = []
        self.dealer_hand = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Blackjack")
        self.setGeometry(400, 150, 600, 700)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

#bet label
        bet_layout = QHBoxLayout()
        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("Enter bet amount")
        self.bet_input.setFixedWidth(120)
        self.start_button = QPushButton("Start Round")
        self.start_button.clicked.connect(self.start_round)
        bet_layout.addWidget(QLabel("Bet:"))
        bet_layout.addWidget(self.bet_input)
        bet_layout.addWidget(self.start_button)
        main_layout.addLayout(bet_layout)

#dealer label
        self.dealer_label = QLabel("Dealer: 0")
        self.dealer_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(self.dealer_label)

        self.dealer_card_layout = QHBoxLayout()
        main_layout.addLayout(self.dealer_card_layout)

        self.balance_label = QLabel(f"Balance: ${self.balance}")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(self.balance_label)

#user label
        self.user_label = QLabel("You: 0")
        self.user_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(self.user_label)

        self.player_card_layout = QHBoxLayout()
        main_layout.addLayout(self.player_card_layout)

#buttons
        button_layout = QHBoxLayout()
        self.hit_button = QPushButton("Hit")
        self.stand_button = QPushButton("Stand")
        self.fold_button = QPushButton("Fold")
        for btn in [self.hit_button, self.stand_button, self.fold_button]:
            btn.setFixedSize(80, 40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px; font-weight: bold; border-radius: 20px;
                    background-color: #4CAF50; color: white;
                }
                QPushButton:hover { background-color: #45a049; }
                QPushButton:pressed { background-color: #3e8e41; }
            """)
        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)
        self.fold_button.clicked.connect(self.fold)
        button_layout.addWidget(self.hit_button)
        button_layout.addWidget(self.stand_button)
        button_layout.addWidget(self.fold_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def start_round(self):
        try:
            self.bet = int(self.bet_input.text())
            if self.bet > self.balance or self.bet <= 0:
                QMessageBox.warning(self, "Invalid Bet", "You cant afford this")
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Bet", "Enter a valid number")
            return

        self.player_hand = []
        self.dealer_hand = []
        self.clear_layout(self.player_card_layout)
        self.clear_layout(self.dealer_card_layout)

        for _ in range(2):
            self.player_hand.append(random.choice(self.cards))
            self.dealer_hand.append(random.choice(self.cards))

        for card in self.player_hand:
            self.add_card_gui(card, self.player_card_layout)
        for card in self.dealer_hand:
            self.add_card_gui(card, self.dealer_card_layout)

        self.update_totals()

    def update_totals(self, hide_dealer_second=False):
        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand) if not hide_dealer_second else self.dealer_hand[0][1]
        self.user_label.setText(f"You: {player_total}")
        self.dealer_label.setText(f"Dealer: {dealer_total}")

    def calculate_total(self, hand):
        total = sum(card[1] for card in hand)
        aces = sum(1 for card in hand if card[1] == 11)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def hit(self):
        new_card = random.choice(self.cards)
        self.player_hand.append(new_card)
        self.add_card_gui(new_card, self.player_card_layout)
        total = self.calculate_total(self.player_hand)
        self.user_label.setText(f"You: {total}")

        if total > 21:
            QMessageBox.information(self, "Bust", "House Wins")
            self.balance -= self.bet
            self.balance_label.setText(f"Balance: {self.balance}")
            self.reset_round()

    def stand(self):
        while self.calculate_total(self.dealer_hand) < 17:
            card = random.choice(self.cards)
            self.dealer_hand.append(card)
            self.add_card_gui(card, self.dealer_card_layout)
        self.update_totals()

        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)

        if player_total == 21 and len(self.player_hand) == 2 and dealer_total != 21:
            QMessageBox.information(self, "Blackjack!", "Blackjack! You Win!")
            self.balance += int(self.bet * 1.5)
        elif dealer_total > 21:
            QMessageBox.information(self, "Result", "Dealer Busts! You Win!")
            self.balance += self.bet
        elif player_total > dealer_total:
            QMessageBox.information(self, "Result", "You Win!")
            self.balance += self.bet
        elif dealer_total == player_total:
            QMessageBox.information(self, "Result", "Tie!")
        else:
            QMessageBox.information(self, "Result", "House Wins!")
            self.balance -= self.bet

        self.balance_label.setText(f"Balance: {self.balance}")
        self.reset_round()

    def fold(self):
        self.balance -= self.bet
        self.balance_label.setText(f"Balance: {self.balance}")
        self.reset_round()

    def reset_round(self):
        self.player_hand = []
        self.dealer_hand = []
        self.clear_layout(self.player_card_layout)
        self.clear_layout(self.dealer_card_layout)
        self.user_label.setText("You: 0")
        self.dealer_label.setText("Dealer: 0")

    def add_card_gui(self, card, layout):
        card_label = QLabel()
        card_label.setFixedSize(120,180)
        card_label.setScaledContents(True)
        card_label.setPixmap(QPixmap(card[0]))
        card_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(card_label)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Blackjack()
    window.show()
    sys.exit(app.exec_())

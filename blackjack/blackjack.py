import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap

class Blackjack(QWidget):
    def __init__(self):
        super().__init__()
        self.balance = 1000
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []
        self.dealer_score = 0
        self.user_score = 0
        self.cards = [
            ("cards/2_of_spades.png",2), ("cards/3_of_spades.png",3), ("cards/4_of_spades.png",4),
            ("cards/5_of_spades.png",5), ("cards/6_of_spades.png",6), ("cards/7_of_spades.png",7),
            ("cards/8_of_spades.png",8), ("cards/9_of_spades.png",9), ("cards/10_of_spades.png",10),
            ("cards/jack_of_spades.png",10), ("cards/queen_of_spades.png",10), ("cards/king_of_spades.png",10),
            ("cards/ace_of_spades.png",11),
            ("cards/2_of_hearts.png",2), ("cards/3_of_hearts.png",3), ("cards/4_of_hearts.png",4),
            ("cards/5_of_hearts.png",5), ("cards/6_of_hearts.png",6), ("cards/7_of_hearts.png",7),
            ("cards/8_of_hearts.png",8), ("cards/9_of_hearts.png",9), ("cards/10_of_hearts.png",10),
            ("cards/jack_of_hearts.png",10), ("cards/queen_of_hearts.png",10), ("cards/king_of_hearts.png",10),
            ("cards/ace_of_hearts.png",11),
            ("cards/2_of_diamonds.png",2), ("cards/3_of_diamonds.png",3), ("cards/4_of_diamonds.png",4),
            ("cards/5_of_diamonds.png",5), ("cards/6_of_diamonds.png",6), ("cards/7_of_diamonds.png",7),
            ("cards/8_of_diamonds.png",8), ("cards/9_of_diamonds.png",9), ("cards/10_of_diamonds.png",10),
            ("cards/jack_of_diamonds.png",10), ("cards/queen_of_diamonds.png",10), ("cards/king_of_diamonds.png",10),
            ("cards/ace_of_diamonds.png",11),
            ("cards/2_of_clubs.png",2), ("cards/3_of_clubs.png",3), ("cards/4_of_clubs.png",4),
            ("cards/5_of_clubs.png",5), ("cards/6_of_clubs.png",6), ("cards/7_of_clubs.png",7),
            ("cards/8_of_clubs.png",8), ("cards/9_of_clubs.png",9), ("cards/10_of_clubs.png",10),
            ("cards/jack_of_clubs.png",10), ("cards/queen_of_clubs.png",10), ("cards/king_of_clubs.png",10),
            ("cards/ace_of_clubs.png",11)
        ]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Blackjack")
        self.adjustSize()
        self.move(0, 0)
        self.setStyleSheet("QWidget { background-color: #732532; }")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        #  Bet Widget 
        bet_widget = QWidget()
        bet_layout = QGridLayout(bet_widget)

        self.bet_label = QLabel("Bet:")
        self.bet_label.setStyleSheet(
            "color: #d1a23d; font-size: 18px; font-weight: bold; padding: 10px; text-stroke: 4px black;"
        )

        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("Enter bet amount")
        self.bet_input.setFixedWidth(120)
        self.bet_input.setStyleSheet(
            "color: #d1a23d; padding: 5px; font-weight:bold; background-color: #631f2a;"
        )
        self.bet_input.returnPressed.connect(self.start_round)
        self.bet_input.installEventFilter(self)
        self.installEventFilter(self)

        self.start_button = QPushButton("Start\nRound")
        self.start_button.setFixedSize(80, 40)
        self.start_button.clicked.connect(self.start_round)
        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 14px; font-weight: bold; border-radius: 20px;
                background-color: #2b8f2e; color: #d1a23d;
            }
            QPushButton:hover { background-color: #257a27; }
            QPushButton:pressed { background-color: #1e631f; }
        """)

        bet_layout.addWidget(self.bet_label, 0, 0, alignment=Qt.AlignRight)
        bet_layout.addWidget(self.bet_input, 0, 1, alignment=Qt.AlignLeft)
        bet_layout.addWidget(self.start_button, 0, 2, alignment=Qt.AlignLeft)
        main_layout.addWidget(bet_widget, alignment=Qt.AlignHCenter)

        #  Dealer Label & Cards 
        self.dealer_label = QLabel("Dealer: 0")
        self.dealer_label.setStyleSheet("color: #d1a23d; font-size: 18px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(self.dealer_label)

        self.dealer_card_layout = QHBoxLayout()
        main_layout.addLayout(self.dealer_card_layout)

        #  Balance & Score 
        self.balance_label = QLabel(f"Balance: ${self.balance}")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet("color: #d1a23d; font-size: 18px; font-weight: bold; padding: 2px;")
        main_layout.addWidget(self.balance_label)

        self.score_label = QLabel(f"Score: {self.user_score} - {self.dealer_score}")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("color: #d1a23d; font-size: 18px; font-weight: bold; padding: 2px;")
        main_layout.addWidget(self.score_label)

        #  Player Label & Cards 
        self.user_label = QLabel("You: 0")
        self.user_label.setStyleSheet("color: #d1a23d; font-size: 18px; font-weight: bold; padding: 2px;")
        main_layout.addWidget(self.user_label)

        self.player_card_layout = QHBoxLayout()
        main_layout.addLayout(self.player_card_layout)

        #  Buttons 
        button_layout = QHBoxLayout()
        self.hit_button = QPushButton("Hit\n(1)")
        self.stand_button = QPushButton("Stand\n(2)")
        self.fold_button = QPushButton("Fold\n(3)")
        for btn in [self.hit_button, self.stand_button, self.fold_button]:
            btn.setHidden(True)
            btn.setFixedSize(80, 40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px; font-weight: bold; border-radius: 20px;
                    background-color: #2b8f2e; color: #d1a23d;
                }
                QPushButton:hover { background-color: #257a27; }
                QPushButton:pressed { background-color: #1e631f; }
            """)
        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)
        self.fold_button.clicked.connect(self.fold)
        button_layout.addWidget(self.hit_button)
        button_layout.addWidget(self.stand_button)
        button_layout.addWidget(self.fold_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and not self.hit_button.isHidden():
            key = event.key()
            if key == Qt.Key_1:
                self.hit()
            elif key == Qt.Key_2:
                self.stand()
            elif key == Qt.Key_3:
                self.fold()
            return True
        return super().eventFilter(source, event)

    def show_message(self, title, text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.NoButton)

        btn = QPushButton("Continue")
        btn.clicked.connect(msg.accept)
        msg.layout().addWidget(btn, msg.layout().rowCount(), 0, 1, msg.layout().columnCount(), Qt.AlignCenter)
        btn.setFixedSize(80, 40)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 14px; font-weight: bold; border-radius: 20px;
                background-color: #2b8f2e; color: #d1a23d;
            }
            QPushButton:hover { background-color: #257a27; }
            QPushButton:pressed { background-color: #1e631f; }
        """)

        msg.setStyleSheet("""
            QMessageBox { background-color: #732532; }
            QLabel { color: #d1a23d; font-size: 16px; font-weight: bold; text-align: center; }
        """)
        msg.exec_()

    def quit_message(self, title, text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.NoButton)

        btn = QPushButton("Quit")
        btn.clicked.connect(self.close)
        msg.layout().addWidget(btn, msg.layout().rowCount(), 0, 1, msg.layout().columnCount(), Qt.AlignCenter)
        btn.setFixedSize(80, 40)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 14px; font-weight: bold; border-radius: 20px;
                background-color: #2b8f2e; color: #d1a23d;
            }
            QPushButton:hover { background-color: #257a27; }
            QPushButton:pressed { background-color: #1e631f; }
        """)

        msg.setStyleSheet("""
            QMessageBox { background-color: #732532; }
            QLabel { color: #d1a23d; font-size: 16px; font-weight: bold; text-align: center; }
        """)
        msg.exec_()

    def start_round(self):
        try:
            self.bet = int(self.bet_input.text())
            if self.bet <= 0:
                self.show_message("Invalid Bet", "Bet must be higher than 0")
                return
            elif self.bet > self.balance:
                self.show_message("Invalid Bet", "You can't afford this")
                return
        except ValueError:
            self.show_message("Invalid Bet", "Enter a valid number")
            return

        self.hit_button.setHidden(False)
        self.stand_button.setHidden(False)
        self.fold_button.setHidden(False)

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
            self.show_message("Bust", f"House Wins, You Lose ${self.bet}")
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

        if player_total == 21 and dealer_total != 21:
            self.show_message("Blackjack!", f"Blackjack, You Win ${int(self.bet*1.5)}!")
            self.balance += int(self.bet*1.5)
        elif dealer_total > 21:
            self.show_message("Result", f"Dealer Busts, You Win ${self.bet}!")
            self.balance += self.bet
        elif player_total > dealer_total:
            self.show_message("Result", f"You Win ${self.bet}!")
            self.balance += self.bet
        elif dealer_total == player_total:
            self.show_message("Result", "Tie!")
        else:
            self.show_message("Result", f"House Wins, You Lose ${self.bet}")
            self.balance -= self.bet

        self.balance_label.setText(f"Balance: {self.balance}")
        self.reset_round()

    def fold(self):
        self.balance -= self.bet
        self.balance_label.setText(f"Balance: {self.balance}")
        self.reset_round()

    def add_score(self):
        player_total = self.calculate_total(self.player_hand)
        dealer_total = self.calculate_total(self.dealer_hand)
        if player_total <= 21 and (player_total > dealer_total or dealer_total > 21):
            self.user_score += 1
        if dealer_total <= 21 and (dealer_total > player_total or player_total > 21):
            self.dealer_score += 1
        self.score_label.setText(f"Score: {self.user_score} - {self.dealer_score}")

    def reset_round(self):
        if self.balance == 0:
            self.quit_message("Result", f"You are Bankrupt\nFinal Score: {self.user_score} - {self.dealer_score}")
        self.hit_button.setHidden(True)
        self.stand_button.setHidden(True)
        self.fold_button.setHidden(True)
        self.add_score()
        self.player_hand = []
        self.dealer_hand = []
        self.clear_layout(self.player_card_layout)
        self.clear_layout(self.dealer_card_layout)
        self.user_label.setText("You: 0")
        self.dealer_label.setText("Dealer: 0")
        self.score_label.setText(f"Score: {self.user_score} - {self.dealer_score}")
        self.adjustSize()

    def add_card_gui(self, card, layout):
        card_label = QLabel()
        card_label.setFixedSize(120, 180)
        card_label.setScaledContents(True)
        card_label.setPixmap(QPixmap(card[0]))
        card_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(card_label)

    #  Clear Layout 
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

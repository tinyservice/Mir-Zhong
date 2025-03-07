from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QTextEdit
from chess_board import ChessBoard
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中国象棋")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.chess_board = ChessBoard()
        self.layout.addWidget(self.chess_board)

        self.turn_label = QLabel(f"当前轮次: {self.chess_board.game_mgr.turn}")
        self.layout.addWidget(self.turn_label)

        self.move_log = QTextEdit()
        self.move_log.setReadOnly(True)
        self.layout.addWidget(self.move_log)

        self.chess_board.game_mgr.turn_changed.connect(self.update_turn_label)
        self.chess_board.game_mgr.move_logged.connect(self.update_move_log)

    def update_turn_label(self):
        self.turn_label.setText(f"当前轮次: {self.chess_board.game_mgr.turn}")

    def update_move_log(self, move_entry):
        self.move_log.append(move_entry)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

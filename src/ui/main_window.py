from PySide6.QtWidgets import QMainWindow, QApplication
from chess_board import ChessBoard
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中国象棋")
        self.chess_board = ChessBoard()
        self.setCentralWidget(self.chess_board)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

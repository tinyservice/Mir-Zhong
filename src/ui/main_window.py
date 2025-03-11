from PySide6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton, QFileDialog
from PySide6.QtCore import QTimer
from chess_board import ChessBoard
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中国象棋")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setSpacing(0)  # Set spacing between widgets to 10

        self.chess_board = ChessBoard()
        self.layout.addWidget(self.chess_board)

        self.side_panel = QVBoxLayout()
        self.layout.addLayout(self.side_panel)

        self.turn_label = QLabel(f"当前轮次: {self.chess_board.game_mgr.turn}")
        self.side_panel.addWidget(self.turn_label)

        self.move_log = QTextEdit()
        self.move_log.setReadOnly(True)
        self.move_log.setFixedWidth(self.turn_label.sizeHint().width() * 1.5)
        self.side_panel.addWidget(self.move_log)

        self.load_moves_button = QPushButton("载入棋谱")
        self.load_moves_button.clicked.connect(self.load_moves)
        self.side_panel.addWidget(self.load_moves_button)

        self.save_moves_button = QPushButton("保存棋谱")
        self.save_moves_button.clicked.connect(self.save_moves)
        self.side_panel.addWidget(self.save_moves_button)

        self.chess_board.game_mgr.turn_changed.connect(self.update_turn_label)
        self.chess_board.game_mgr.move_logged.connect(self.update_move_log)

    def update_turn_label(self):
        self.turn_label.setText(f"当前轮次: {self.chess_board.game_mgr.turn}")

    def update_move_log(self, move_entry):
        self.move_log.append(move_entry)

    def load_moves(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择棋谱文件", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.moves = file.readlines()
            self.current_move_index = 0
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.play_next_move)
            self.timer.setInterval(1000) # 5 seconds interval
            self.timer.start()

    def play_next_move(self):
        if self.current_move_index < len(self.moves):
            move = self.moves[self.current_move_index].strip()
            if move:
                self.chess_board.play_move(move)
                self.move_log.append(move)
            self.current_move_index += 1
        else:
            self.timer.stop()

    def save_moves(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存棋谱文件", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.move_log.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

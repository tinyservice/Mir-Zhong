from PySide6.QtCore import QObject, Signal

class ChessGameMgr(QObject):
    turn_changed = Signal()
    move_logged = Signal(str)

    def __init__(self):
        super().__init__()
        self.turn = "red"  # 红方先走
        self.move_log = []

    def switch_turn(self):
        self.turn = "black" if self.turn == "red" else "red"
        self.turn_changed.emit()

    def log_move(self, piece, old_position, new_position):
        move_entry = f"{piece.color} {piece.name} from {old_position} to {new_position}"
        self.move_log.append(move_entry)
        self.move_logged.emit(move_entry)
        print(move_entry)

    def get_move_log(self):
        return self.move_log
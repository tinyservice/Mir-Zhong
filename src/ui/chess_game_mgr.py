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
        move_entry = self.generate_move_entry(piece, old_position, new_position)
        self.move_log.append(move_entry)
        self.move_logged.emit(move_entry)
        print(move_entry)

    def generate_move_entry(self, piece, old_position, new_position):
        columns_red = "九八七六五四三二一"
        columns_black = "123456789"
        piece_name = piece.name
        old_col, old_row = old_position
        new_col, new_row = new_position
        # print(f"old_col: {old_col}, old_row: {old_row}, new_col: {new_col}, new_row: {new_row}")
        if piece.color == "red":
            old_col_str = columns_red[old_col]
            new_col_str = columns_red[new_col]
            if new_row < old_row:
                if new_col == old_col:
                    move_entry = f"{piece_name}{old_col_str}进{columns_red[9 - (old_row - new_row)]}"
                else:
                    move_entry = f"{piece_name}{old_col_str}进{columns_red[new_col]}"
            elif new_row > old_row:
                if new_col == old_col:
                    move_entry = f"{piece_name}{old_col_str}退{columns_red[9 - (new_row - old_row)]}"
                else:
                    move_entry = f"{piece_name}{old_col_str}退{columns_red[new_col]}"
            else:
                move_entry = f"{piece_name}{old_col_str}平{new_col_str}"
        else:
            old_col_str = columns_black[old_col]
            new_col_str = columns_black[new_col]
            if new_row > old_row:
                if new_col == old_col:
                    move_entry = f"{piece_name}{old_col_str}进{columns_black[new_row - old_row - 1]}"
                else:
                    move_entry = f"{piece_name}{old_col_str}进{columns_black[new_col]}"
            elif new_row < old_row:
                if new_col == old_col:
                    move_entry = f"{piece_name}{old_col_str}退{columns_black[old_row - new_row - 1]}"
                else:
                    move_entry = f"{piece_name}{old_col_str}退{columns_black[new_col]}"
            else:
                move_entry = f"{piece_name}{old_col_str}平{new_col_str}"

        return move_entry

    def get_move_log(self):
        return self.move_log
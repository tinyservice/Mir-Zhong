import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt
from chess_piece import Rook, Knight, Cannon, Pawn, Guard, Elephant, King
from chess_game_mgr import ChessGameMgr

class ChessBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 640)
        self.intersections = []
        self.selected_piece = None
        self.row = 10
        self.col = 9
        self.game_mgr = ChessGameMgr()
        # Print intersection points
        self.board_size = min(self.width(), self.height() - 40)
        self.cell_size =  self.board_size // 10
        self.offset_y = -20  # 向上移动20个像素
        self.intersections = []
        self.init_intersections()
        self.init_pieces()

    def init_intersections(self):
        for i in range(self.col):
            for j in range(self.row):
                posx = (i + 1) * self.cell_size
                posy = (j + 1) * self.cell_size + self.offset_y
                self.intersections.append((i, j, posx, posy, None))

    def init_pieces(self):
        self.pieces = [
            # Red pieces
            Rook("車", "red", (0, 0)), Rook("車", "red", (8, 0)),
            Knight("馬", "red", (1, 0)), Knight("馬", "red", (7, 0)),
            Cannon("炮", "red", (1, 2)), Cannon("炮", "red", (7, 2)),
            Pawn("兵", "red", (0, 3)), Pawn("兵", "red", (2, 3)), Pawn("兵", "red", (4, 3)), Pawn("兵", "red", (6, 3)), Pawn("兵", "red", (8, 3)),
            Guard("仕", "red", (3, 0)), Guard("仕", "red", (5, 0)),
            Elephant("相", "red", (2, 0)), Elephant("相", "red", (6, 0)),
            King("帅", "red", (4, 0)),
            # Black pieces
            Rook("车", "black", (0, 9)), Rook("车", "black", (8, 9)),
            Knight("马", "black", (1, 9)), Knight("马", "black", (7, 9)),
            Cannon("炮", "black", (1, 7)), Cannon("炮", "black", (7, 7)),
            Pawn("卒", "black", (0, 6)), Pawn("卒", "black", (2, 6)), Pawn("卒", "black", (4, 6)), Pawn("卒", "black", (6, 6)), Pawn("卒", "black", (8, 6)),
            Guard("士", "black", (3, 9)), Guard("士", "black", (5, 9)),
            Elephant("象", "black", (2, 9)), Elephant("象", "black", (6, 9)),
            King("将", "black", (4, 9)),
        ]
        self.update_intersections()

    def update_intersections(self):
        for piece in self.pieces:
            for i, (x, y, posx, posy, _color) in enumerate(self.intersections):
                if (x, y) == piece.position:
                    self.intersections[i] = (x, y, posx, posy, piece.color)

    def log_board(self):
        for i, (x, y, posx, posy, color) in enumerate(self.intersections):
            print(f'({x},{y}) = {color}')
            
    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBoard(painter)
        self.drawPieces(painter)

    def drawBoard(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))

        # Draw outer frame (two layers)
        painter.drawRect(self.cell_size - 3, self.cell_size - 3 + self.offset_y, self.cell_size * 8 + 6, self.cell_size * 9 + 6)
        painter.drawRect(self.cell_size, self.cell_size + self.offset_y, self.cell_size * 8, self.cell_size * 9)

        # Draw horizontal lines
        for i in range(12):
            painter.drawLine(self.cell_size, self.cell_size * (i + 1) + self.offset_y, self.cell_size * 9, self.cell_size * (i + 1) + self.offset_y)

        # Draw vertical lines
        for i in range(9):
            if i == 0 or i == 8:
                painter.drawLine(self.cell_size * (i + 1), self.cell_size + self.offset_y, self.cell_size * (i + 1), self.cell_size * 10 + self.offset_y)
            else:
                painter.drawLine(self.cell_size * (i + 1), self.cell_size + self.offset_y, self.cell_size * (i + 1), self.cell_size * 5 + self.offset_y)
                painter.drawLine(self.cell_size * (i + 1), self.cell_size * 6 + self.offset_y, self.cell_size * (i + 1), self.cell_size * 10 + self.offset_y)

        # Draw the palace (九宫格)
        painter.drawLine(self.cell_size * 4, self.cell_size + self.offset_y, self.cell_size * 6, self.cell_size * 3 + self.offset_y)
        painter.drawLine(self.cell_size * 6, self.cell_size + self.offset_y, self.cell_size * 4, self.cell_size * 3 + self.offset_y)
        painter.drawLine(self.cell_size * 4, self.cell_size * 8 + self.offset_y, self.cell_size * 6, self.cell_size * 10 + self.offset_y)
        painter.drawLine(self.cell_size * 6, self.cell_size * 8 + self.offset_y, self.cell_size * 4, self.cell_size * 10 + self.offset_y)

        # Draw the river
        font = painter.font()
        font.setPointSize(font.pointSize() * 2)
        painter.setFont(font)
        painter.drawText(self.cell_size * 2.0, self.cell_size * 5.7 + self.offset_y, "楚      河")
        painter.drawText(self.cell_size * 6.5, self.cell_size * 5.7 + self.offset_y, "汉      界")

        # Draw L shapes at specified positions
        l_size = self.cell_size // 12
        positions = [(2, 3), (8, 3), (2, 8), (8, 8), (3, 4), (5, 4), (7, 4), (3, 7), (5, 7), (7, 7)]
        for (col, row) in positions:
            x = self.cell_size * col
            y = self.cell_size * row + self.offset_y
            painter.drawLine(x - l_size, y - l_size, x - l_size, y - l_size * 2)
            painter.drawLine(x - l_size, y - l_size, x - l_size * 2, y - l_size)
            painter.drawLine(x + l_size, y - l_size, x + l_size, y - l_size * 2)
            painter.drawLine(x + l_size, y - l_size, x + l_size * 2, y - l_size)
            painter.drawLine(x - l_size, y + l_size, x - l_size, y + l_size * 2)
            painter.drawLine(x - l_size, y + l_size, x - l_size * 2, y + l_size)
            painter.drawLine(x + l_size, y + l_size, x + l_size, y + l_size * 2)
            painter.drawLine(x + l_size, y + l_size, x + l_size * 2, y + l_size)

        # Draw left L shape at (9, 4)
        left_positions = [(9,4),(9,7)]
        for (col, row) in left_positions:
            x = self.cell_size * col
            y = self.cell_size * row + self.offset_y
            painter.drawLine(x - l_size, y - l_size, x - l_size, y - l_size * 2)
            painter.drawLine(x - l_size, y - l_size, x - l_size * 2, y - l_size)
            painter.drawLine(x - l_size, y + l_size, x - l_size, y + l_size * 2)
            painter.drawLine(x - l_size, y + l_size, x - l_size * 2, y + l_size)

        # Draw right L shape at (1, 4)
        right_positions = [(1,4),(1,7)]
        for (col, row) in right_positions:
            x = self.cell_size * col
            y = self.cell_size * row + self.offset_y
            painter.drawLine(x + l_size, y - l_size, x + l_size, y - l_size * 2)
            painter.drawLine(x + l_size, y - l_size, x + l_size * 2, y - l_size)
            painter.drawLine(x + l_size, y + l_size, x + l_size, y + l_size * 2)
            painter.drawLine(x + l_size, y + l_size, x + l_size * 2, y + l_size)


    def mousePressEvent(self, event):
        x, y = None, None
        for (i, j, posx, posy, _) in self.intersections:
            if (event.position().x() - posx) ** 2 + (event.position().y() - posy) ** 2 <= 20 ** 2:
                x = i
                y = j
                break

        if x is None or y is None:
            print('无效操作')
            return

        clicked_piece = None
        for piece in self.pieces:
            if piece.position == (x, y):
                clicked_piece = piece
                break
        
        print(f'点击的位置为:{x},{y}, color = {self.intersections[x * self.col + y][4]}')
        if self.selected_piece:
            if clicked_piece:
                if clicked_piece.color == self.selected_piece.color:
                    self.selected_piece = clicked_piece
                    print(f'切换选中的棋子为:{self.selected_piece.name}')
                else:
                    self.pieces.remove(clicked_piece)
                    if self.move_piece(self.selected_piece, (x, y)) == True:
                        print(f'吃掉对方棋子:{clicked_piece.name}, 移动选中的棋子到:{x},{y}')
                        self.game_mgr.log_move(self.selected_piece, self.selected_piece.position, (x, y))
                        self.game_mgr.switch_turn()
            else:
                if self.move_piece(self.selected_piece, (x, y)) == True:
                    print(f'移动选中的棋子到:{x},{y}')
                    self.game_mgr.log_move(self.selected_piece, self.selected_piece.position, (x, y))
                    self.game_mgr.switch_turn()
            self.selected_piece = None
        else:
            if clicked_piece and clicked_piece.color == self.game_mgr.turn:
                self.selected_piece = clicked_piece
                print(f'选中的棋子为:{self.selected_piece.name}')
            else:
                print('无效操作')

    def mouseReleaseEvent(self, event):
        # No action needed on mouse release
        pass

    def move_piece(self, piece, new_position):
        is_can_move = False
        if piece.can_move_to(self, new_position):
            old_position = piece.position
            piece.move(new_position)
            is_can_move =  True
            self.update_intersections_after_move(old_position, new_position, piece.color)
        else:
            print(f'{piece.name}不能移动到位置: {new_position}')
        self.update()
        return is_can_move

    def update_intersections_after_move(self, old_position, new_position, color):
        for i, (x, y, posx, posy, _) in enumerate(self.intersections):
            if (x, y) == old_position:
                self.intersections[i] = (x, y, posx, posy, None)
            if (x, y) == new_position:
                self.intersections[i] = (x, y, posx, posy, color)

    def drawPieces(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        font = painter.font()
        font.setPointSize(font.pointSize() * 1.0)
        painter.setFont(font)
        board_size = min(self.width(), self.height() - 40)
        self.offset_y = -20  # 向上移动20个像素
        for piece in self.pieces:
            x, y = piece.position
            self.cell_size = board_size // 10
            piece_size = self.cell_size * 0.6
            piece_x = (x + 1) * self.cell_size - piece_size / 2 
            piece_y = (y + 1) * self.cell_size - piece_size / 2 + self.offset_y
            painter.setBrush(QColor(255, 255, 255))  # Set brush to non-transparent white
            painter.drawEllipse(piece_x, piece_y, piece_size, piece_size)
            painter.drawText(piece_x, piece_y, piece_size, piece_size, Qt.AlignCenter, piece.name)
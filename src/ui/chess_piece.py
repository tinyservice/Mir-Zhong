#######棋子#######
# 棋子类，包括棋子的名字、颜色、位置、移动方法、判断是否能移动到目标位置的方法、获取所有可移动位置的方法
# 棋子类的子类包括车、马、炮、兵、士、象、帅
# 每个子类实现了获取所有可移动位置的方法，根据棋子的移动规则，判断棋子是否能移动到目标位置
# 棋子的移动规则参考中国象棋的规则  https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E8%B1%A1%E6%A3%8B
class ChessPiece:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def can_move_to(self, board, new_position):
        """判断棋子是否能移动到目标位置"""
        return new_position in self.get_moves(board)

    def get_moves(self, board):
        raise NotImplementedError("This method should be overridden by subclasses")

#######车#######
class Rook(ChessPiece):
    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, down, up
        for direction in directions:
            x, y = self.position
            while True:
                x += direction[0]
                y += direction[1]
                if not (0 <= x < board.col and 0 <= y < board.row):
                    break  # Out of bounds
                if board.intersections[x * board.row + y ][4] is None:
                    moves.append((x, y))
                elif board.intersections[x * board.row + y ][4] != self.color:
                    moves.append((x, y))
                    break  # Can capture opponent piece but can't move further
                else:
                    break  # Can't move to a square occupied by a friendly piece
        return moves

#######马#######
class Knight(ChessPiece):
    def get_moves(self, board):
        moves = []
        x, y = self.position
        knight_moves = [
            (2, 1, 1, 0), (2, -1, 1, 0), (-2, 1, -1, 0), (-2, -1, -1, 0),
            (1, 2, 0, 1), (1, -2, 0, -1), (-1, 2, 0, 1), (-1, -2, 0, -1)
        ]
        board.log_board()
        for move in knight_moves:
            new_x, new_y, block_x, block_y = x + move[0], y + move[1], x + move[2], y + move[3]
            if 0 <= new_x < board.col and 0 <= new_y < board.row:
                if board.intersections[block_x * board.row + block_y][4] is None:  # Check if the horse leg is blocked              
                    if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                        moves.append((new_x, new_y))
        return moves

#######炮#######
class Cannon(ChessPiece):
    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, down, up
        for direction in directions:
            x, y = self.position
            jumped = False
            while True:
                x += direction[0]
                y += direction[1]
                if not (0 <= x < board.col and 0 <= y < board.row):
                    break  # Out of bounds
                if not jumped:
                    if board.intersections[x * board.row + y][4] is None:
                        moves.append((x, y))
                    else:
                        jumped = True
                else:
                    if board.intersections[x * board.row + y][4] is not None:
                        if board.intersections[x * board.row + y][4] != self.color:
                            moves.append((x, y))
                        break  # Can capture opponent piece but can't move further
        return moves

#######兵#######
class Pawn(ChessPiece):
    def get_moves(self, board):
        moves = []
        x, y = self.position
        directions = []

        if self.color == 'red':
            if y < 5:  # Before crossing the river
                directions = [(0, 1)]  # Move forward
            else:  # After crossing the river
                directions = [(0, 1), (1, 0), (-1, 0)]  # Move forward, left, right
        else:  # Black pawn
            if y > 4:  # Before crossing the river
                directions = [(0, -1)]  # Move forward
            else:  # After crossing the river
                directions = [(0, -1), (1, 0), (-1, 0)]  # Move forward, left, right

        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if 0 <= new_x < board.col and 0 <= new_y < board.row:
                if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                    moves.append((new_x, new_y))

        return moves

#######士#######
class Guard(ChessPiece):
    def get_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal moves

        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if self.color == 'red':
                if 3 <= new_x <= 5 and 0 <= new_y <= 2:  # Red guard's palace area
                    if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                        moves.append((new_x, new_y))
                        print(f'red Guard can move to {new_x, new_y}')
            else:  # Black guard
                if 3 <= new_x <= 5 and 7 <= new_y <= 9:  # Black guard's palace area
                    if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                        moves.append((new_x, new_y))
                        print(f'black Guard can move to {new_x, new_y}')

        return moves

#######象#######
class Elephant(ChessPiece):
    def get_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(2, 2, 1, 1), (2, -2, 1, -1), (-2, 2, -1, 1), (-2, -2, -1, -1)]  # Diagonal moves

        for direction in directions:
            new_x, new_y, block_x, block_y = x + direction[0], y + direction[1], x + direction[2], y + direction[3]
            if self.color == 'red':
                if 0 <= new_x <= 8 and 0 <= new_y <= 4:  # Red elephant's area
                    if board.intersections[block_x * board.row + block_y][4] is None:  # Check if the elephant eye is blocked
                        if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                            moves.append((new_x, new_y))
            else:  # Black elephant
                if 0 <= new_x <= 8 and 5 <= new_y <= 9:  # Black elephant's area
                    if board.intersections[block_x * board.row + block_y][4] is None:  # Check if the elephant eye is blocked
                        if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                            moves.append((new_x, new_y))

        return moves

#######帅#######
class King(ChessPiece):
    def get_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, down, up

        for direction in directions:
            new_x, new_y = x + direction[0], y + direction[1]
            if self.color == 'red':
                if 3 <= new_x <= 5 and 0 <= new_y <= 2:  # Red king's palace area
                    if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                        moves.append((new_x, new_y))
            else:  # Black king
                if 3 <= new_x <= 5 and 7 <= new_y <= 9:  # Black king's palace area
                    if board.intersections[new_x * board.row + new_y][4] is None or board.intersections[new_x * board.row + new_y][4] != self.color:
                        moves.append((new_x, new_y))

        return moves

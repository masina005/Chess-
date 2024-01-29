import pygame
import os

class Piece:
    def __init__(self, pos, color):
        self.pos = pos
        self.x, self.y = pos[0], pos[1]
        self.color = color
        self.size = (90, 90)

        self.legal_moves = []

    def change_pos(self, new_pos):
        self.pos = new_pos
        self.x, self.y = new_pos[0], new_pos[1]
        
class Pawn(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.img = pygame.transform.scale(pygame.image.load(self.get_img_path()), self.size)

    def get_img_path(self):
        if self.color == "white":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\white-pawn.png"
        elif self.color == "black":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\black-pawn.png"
        
    def update_legal_moves(self, grid):
        self.legal_moves.clear()

        # Check if the color is white
        if self.color == "white":
            # Iterate through the rows of the grid
            for y in range(len(grid)):
                # Iterate through the columns of the grid
                for x in range(len(grid[y])):

                    # Check if moving forward
                    moving_forward = y == self.y - 1 and isinstance(grid[x][y], EmptySquare)
                    # Check if moving by 1
                    moving_by_1 = x == self.x
                    # Check if taking a piece
                    taking_piece = (x == self.x + 1 or x == self.x - 1) and grid[x][y].color == "black"
                    not_taking_same_color = grid[x][y].color != self.color
                    # Check if starting a jump
                    start_jump = y == self.y - 2 and x == self.x and self.y == 6
                    # Check if the move is legal
                    if ((moving_forward and (moving_by_1 or taking_piece)) or start_jump) and not_taking_same_color:
                        # Add the move to the list of legal moves
                        self.legal_moves.append([x, y])

        if self.color == "black":
            # Iterate through the rows of the grid
            for y in range(len(grid)):
                # Iterate through the columns of the grid
                for x in range(len(grid[y])):

                    # Check if moving forward
                    moving_forward = y == self.y + 1 and isinstance(grid[x][y], EmptySquare)
                    # Check if moving by 1
                    moving_by_1 = x == self.x
                    # Check if taking a piece
                    taking_piece = (x == self.x + 1 or x == self.x - 1) and grid[x][y].color == "white"
                    not_taking_same_color = grid[x][y].color != self.color
                    # Check if starting a jump
                    start_jump = y == self.y + 2 and x == self.x and self.y == 1
                    # Check if the move is legal
                    if ((moving_forward and (moving_by_1 or taking_piece)) or start_jump) and not_taking_same_color:
                        # Add the move to the list of legal moves
                        self.legal_moves.append([x, y])


class Rook(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.img = pygame.transform.scale(pygame.image.load(self.get_img_path()), self.size)

    def get_img_path(self):
        if self.color == "white":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\white-rook.png"
        elif self.color == "black":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\black-rook.png"


    def update_legal_moves(self, grid):
        self.legal_moves.clear()
        # Iterate through the rows of the grid
        for y in range(len(grid)):
            # Iterate through the columns of the grid
            for x in range(len(grid[y])):
                moving_in_row = y == self.y
                moving_in_column = x == self.x
                moving = not (self.x == x and self.y == y)
                not_taking_same_color = grid[x][y].color != self.color
                # Check if the move is legal
                if (moving_in_row or moving_in_column) and moving and not_taking_same_color and self.clear_path(grid, [x, y]):
                    # Add the move to the list of legal moves
                    self.legal_moves.append([x, y])
        
    def clear_path(self, grid, pos):
        if pos[0] == self.x:
            # Check if moving vertically
            step = 1 if pos[1] > self.y else -1
            for y in range(self.y + step, pos[1], step):
                if isinstance(grid[self.x][y], Piece):
                    return False

        elif pos[1] == self.y:
            # Check if moving horizontally
            step = 1 if pos[0] > self.x else -1
            for x in range(self.x + step, pos[0], step):
                if isinstance(grid[x][self.y], Piece):
                    return False
                
        return True

class Knight(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.img = pygame.transform.scale(pygame.image.load(self.get_img_path()), self.size)

    def get_img_path(self):
        if self.color == "white":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\white-knight.png"
        elif self.color == "black":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\black-knight.png"
        
    def update_legal_moves(self, grid):
        self.legal_moves.clear()
        # Iterate through the rows of the grid
        for y in range(len(grid)):
            # Iterate through the columns of the grid
            for x in range(len(grid[y])):
                move_1 = abs(self.x - x) == 2 and abs(self.y - y) == 1
                move_2 = abs(self.x - x) == 1 and abs(self.y - y) == 2
                not_taking_same_color = grid[x][y].color != self.color
                if (move_1 or move_2) and not_taking_same_color:
                    self.legal_moves.append([x, y])

class Bishop(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.img = pygame.transform.scale(pygame.image.load(self.get_img_path()), self.size)

    def get_img_path(self):
        if self.color == "white":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\white-bishop.png"
        elif self.color == "black":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\black-bishop.png"

    def update_legal_moves(self, grid):
        self.legal_moves.clear()
        # Iterate through the rows of the grid
        for y in range(len(grid)):
            # Iterate through the columns of the grid
            for x in range(len(grid[y])):
                legal_moves = abs(self.x - x) == abs(self.y - y)
                moving = not (self.x == x and self.y == y)
                not_taking_same_color = grid[x][y].color != self.color
                if moving and legal_moves and not_taking_same_color and self.clear_path(grid, [x, y]):
                    self.legal_moves.append([x, y])

    def clear_path(self, grid, pos):
        if abs(pos[0] - self.x) == abs(pos[1] - self.y):
            # Check if moving diagonally
            step_x = 1 if pos[0] > self.x else -1
            step_y = 1 if pos[1] > self.y else -1
            for i in range(1, abs(pos[0] - self.x)):
                if isinstance(grid[self.x + i * step_x][self.y + i * step_y], Piece):
                    return False
        return True        
        
class Queen(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.img = pygame.transform.scale(pygame.image.load(self.get_img_path()), self.size)

    def get_img_path(self):
        if self.color == "white":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\white-queen.png"
        elif self.color == "black":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\black-queen.png"

    def update_legal_moves(self, grid):
        self.legal_moves.clear()
        # Iterate through the rows of the grid
        for y in range(len(grid)):
            # Iterate through the columns of the grid
            for x in range(len(grid[y])):
                moving = not (self.x == x and self.y == y)

                bishop_moves = abs(self.x - x) == abs(self.y - y)
                moving_in_row = y == self.y
                moving_in_column = x == self.x
                not_taking_same_color = grid[x][y].color != self.color

                if moving and (bishop_moves or moving_in_row or moving_in_column) and not_taking_same_color and self.clear_path(grid, [x, y]):
                    self.legal_moves.append([x, y])

    def clear_path(self, grid, pos):
        if pos[0] == self.x:
            # Check if moving vertically
            step = 1 if pos[1] > self.y else -1
            for y in range(self.y + step, pos[1], step):
                if isinstance(grid[self.x][y], Piece):
                    return False
        elif pos[1] == self.y:
            # Check if moving horizontally
            step = 1 if pos[0] > self.x else -1
            for x in range(self.x + step, pos[0], step):
                if isinstance(grid[x][self.y], Piece):
                    return False
        elif abs(pos[0] - self.x) == abs(pos[1] - self.y):
            # Check if moving diagonally
            step_x = 1 if pos[0] > self.x else -1
            step_y = 1 if pos[1] > self.y else -1
            for i in range(1, abs(pos[0] - self.x)):
                if isinstance(grid[self.x + i * step_x][self.y + i * step_y], Piece):
                    return False
        return True

                
class King(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, color)
        self.img = pygame.transform.scale(pygame.image.load(self.get_img_path()), self.size)

    def get_img_path(self):
        if self.color == "white":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\white-king.png"
        elif self.color == "black":
            return r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\black-king.png"
        
    def update_legal_moves(self, grid):
        self.legal_moves.clear()
        # Iterate through the rows of the grid
        for y in range(len(grid)):
            # Iterate through the columns of the grid
            for x in range(len(grid[y])):     
                legal_move = abs(self.x - x) <= 1 and abs(self.y - y) <= 1
                moving = not (self.x == x and self.y == y)
                not_taking_same_color = grid[x][y].color != self.color

                if legal_move and moving and not_taking_same_color:
                    self.legal_moves.append([x, y])

class EmptySquare():
    def __init__(self):
        self.color = "e"
        self.legal_moves = []

    def update_legal_moves(self, grid):
        self.legal_moves = self.legal_moves

class Chessboard():
    def __init__(self):
        self.grid = self.clear_chessboard()
        self.img = pygame.transform.scale(pygame.image.load(r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\chessboard.jpg"), (800, 800))

        self.highlite_img = pygame.transform.scale(pygame.image.load(r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\images\selected.png"), (90, 90))

    def clear_chessboard(self):
        self.board = self.grid = [[EmptySquare(), EmptySquare(), EmptySquare(), EmptySquare(), EmptySquare(), EmptySquare(), EmptySquare(), EmptySquare()] for i in range(8)]

    def set_starting_position(self):
        # Set starting position
        self.clear_chessboard()
        # White pieces
        self.grid[0][7] = Rook([0, 7], "white")
        self.grid[1][7] = Knight([1, 7], "white")
        self.grid[2][7] = Bishop([2, 7], "white")
        self.grid[3][7] = Queen([3, 7], "white")
        self.grid[4][7] = King([4, 7], "white")
        self.grid[5][7] = Bishop([5, 7], "white")
        self.grid[6][7] = Knight([6, 7], "white")
        self.grid[7][7] = Rook([7, 7], "white")

        for i in range(8):
            self.grid[i][6] = Pawn([i, 6], "white")

        # Black pieces
        self.grid[0][0] = Rook([0, 0], "black")
        self.grid[1][0] = Knight([1, 0], "black")
        self.grid[2][0] = Bishop([2, 0], "black")
        self.grid[3][0] = Queen([3, 0], "black")
        self.grid[4][0] = King([4, 0], "black")
        self.grid[5][0] = Bishop([5, 0], "black")
        self.grid[6][0] = Knight([6, 0], "black")
        self.grid[7][0] = Rook([7, 0], "black")

        for i in range(8):
            self.grid[i][1] = Pawn([i, 1], "black")

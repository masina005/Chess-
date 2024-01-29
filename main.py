import pygame
from chessboard import Chessboard
from chessboard import EmptySquare

pygame.init()

# Set up font
font = pygame.font.Font(r"C:\Users\ADMIN\OneDrive\Plocha\Coding\Python\Chess!\AldotheApache.ttf", 25)

# Set up window dimensions
width, height = 800, 900
win = pygame.display.set_mode((width, height))

class DataSection:
    def __init__(self, font):
        self.font = font

    def get_chess_coords(self, position):
        # Map chess positions to coordinates
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H"]
        if position != None:
            letter = alphabet[position[0]]
            number = 8 - position[1]
            return f"{letter}{number}"
        else:
            return ""

    def update(self, selection, piece):
        # Update the data section with selected position and legal moves
        txt_selected = f"[{self.get_chess_coords(selection)}] selected"
        if piece != None:
            txt_legal_moves = f"legal moves: {[self.get_chess_coords(i) for i in piece.legal_moves]}"
        else:
            txt_legal_moves = ""
        win.blit(self.font.render(txt_legal_moves, True, (255, 255, 255)), (20, 850))
        win.blit(self.font.render(txt_selected, True, (255, 255, 255)), (20, 820))

class ChessGame:
    def __init__(self):
        self.fps = 60
        self.square_size, self.edge_size = 90, 40
        self.selection = None

        self.data_section = DataSection(font)

        self.run = True

        self.board = Chessboard()
        self.board.set_starting_position()

    def get_selected_piece(self):
        if self.selection != None:
            return self.board.grid[self.selection[0]][self.selection[1]]
        else:
            return EmptySquare()


    def get_chessboard_coords(self, click):
        # Convert screen coordinates to chessboard position
        x = int((click[0] - self.edge_size) / self.square_size)
        y = int((click[1] - self.edge_size) / self.square_size)
        return (x, y)

    def get_screen_coords(self, position):
        # Convert chessboard position to screen coordinates
        x = position[0] * self.square_size + self.edge_size
        y = position[1] * self.square_size + self.edge_size
        return (x, y)

    def mouse_handle(self, position):
        x, y = position[0], position[1]

        # If click is within the chessboard
        if (self.edge_size < x < height - self.edge_size) and (self.edge_size < y < 800 - self.edge_size):
            click_coords = self.get_chessboard_coords(position)

            if list(click_coords) in self.get_selected_piece().legal_moves:
                # Move the selected piece to the clicked coordinates
                self.board.grid[click_coords[0]][click_coords[1]] = self.get_selected_piece()
                self.get_selected_piece().change_pos([click_coords[0], click_coords[1]])
                self.board.grid[self.selection[0]][self.selection[1]] = EmptySquare()
                self.selection = None
            else:
                self.selection = click_coords
                self.get_selected_piece().update_legal_moves(self.board.grid)

    def print_ass():
        pass

    def key_handle(self, key):
        if key == pygame.K_LEFT:
            self.selection_x -= 1

    def chessboard_update(self): #Updates chessboard
        win.blit(self.board.img, (0, 0))
        if self.selection != None:
            win.blit(self.board.highlite_img, self.get_screen_coords(self.selection))
        for row in self.board.grid:
            for piece in row:
                if piece.color != "e":
                    win.blit(piece.img, self.get_screen_coords(piece.pos))

    def screen_update(self):
        win.fill((0, 0, 0))

        self.chessboard_update() #Handles chessboard updates
        self.data_section.update(self.selection, self.get_selected_piece())

        pygame.display.update()

    def main(self):
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mouse_handle(event.pos)

            self.screen_update()

if __name__ == "__main__":
    game = ChessGame()
    game.main()
    
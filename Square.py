import pygame

class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        # x, y: Position of tile on board, e.g. 1d <-> 1, 4
        self.width = width
        self.height = height
        # width, height: size of tile to be drawn(shown)
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        
        self.color = 'light' if (x + y) % 2 == 0 else 'dark' # check for correction
        self.draw_color = (243, 229, 171) if self.color == 'light' else (34, 139, 34)
        self.highlight_color = (137, 207, 240) if self.color == 'light' else (115, 147, 179)
        self.check_color = (248, 131, 121)
        self.checkmate_color = (255, 36, 0)
        
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        self.check = False
        self.checkmate = False
        self.rect = pygame.Rect(
            self.abs_x, self.abs_y,
            self.width, self.height
        )

    # Get the formal notation of the tile
    def get_coord(self):
        columns = 'abcdefgh'
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        # Configures if tile should be light or dark or highlighted tile
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        elif self.checkmate:
            pygame.draw.rect(display, self.checkmate_color, self.rect)
        elif self.check:
            pygame.draw.rect(display, self.check_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)
        
        # Adds the chess piece icons
        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)
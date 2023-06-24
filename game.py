import pygame

from controllers.grid import create_game
from controllers.move import MoveController
from schemas.player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH = 50
HEIGHT = 50
MARGIN = 5
Y_SHIFT = 25

grid = create_game()

pygame.init()

WINDOW_SIZE = [555, 580]
screen = pygame.display.set_mode(WINDOW_SIZE)
screen.fill(BLACK)

pygame.display.set_caption("PolytopiaPy")

escaped = False

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 12)
move_font = pygame.font.SysFont("Arial", 24, bold=True)

while not escaped:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            escaped = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            MoveController.move(row, column)

    player_id_to_move = MoveController.get_turn_player_id()
    move_queue_text = move_font.render(f'Turn to move: Player {player_id_to_move}', False, WHITE)
    screen.blit(
        move_queue_text, (WINDOW_SIZE[0] // 4, WINDOW_SIZE[1] - 30)
    )
    


    for row in range(10):
        for column in range(10):
            color = WHITE
            if isinstance(grid[row][column], Player):
                color = RED
            pygame.draw.rect(
                screen,
                color,
                [
                    (MARGIN + WIDTH) * column + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN,
                    WIDTH,
                    HEIGHT,
                ],
            )
            if isinstance(grid[row][column], Player):
                # XXX: draw player info
                img = font.render(str(grid[row][column]), True, BLACK)
                screen.blit(
                    img, ((MARGIN + WIDTH) * column + 12, (MARGIN + HEIGHT) * row + 25)
                )

    # 100 FPS
    clock.tick(100)
    pygame.display.flip()
pygame.quit()

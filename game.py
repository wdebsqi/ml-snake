import pygame, sys
from enum import Enum
from pygame import draw, Color, Rect

SIZE = width, height = 640, 480
POINT_SIZE = 20
MIDDLE_X, MIDDLE_Y = int(width / 2) - POINT_SIZE, int(height / 2) - POINT_SIZE

WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
FPS = 10

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

class Directions(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"


class Point():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Food():
    def __init__(self, position: Point = Point(MIDDLE_X + 3 * POINT_SIZE, MIDDLE_Y + 3 * POINT_SIZE), color: Color = RED):
        self.position = position
        self.color = color

class Snake():
    def __init__(self, starting_point: Point = Point(MIDDLE_X, MIDDLE_Y), color: Color = WHITE):
        self.body = [starting_point]
        self.color = color
        self.direction = Directions.RIGHT

def move_snake(snake: Snake, direction: Directions) -> None:
    current_head = snake.body.pop()

    if direction == Directions.RIGHT:
        new_head = Point(current_head.x + POINT_SIZE, current_head.y)
    elif direction == Directions.LEFT:
        new_head = Point(current_head.x - POINT_SIZE, current_head.y)
    elif direction == Directions.UP:
        new_head = Point(current_head.x, current_head.y - POINT_SIZE)
    else:
        new_head = Point(current_head.x, current_head.y + POINT_SIZE)

    snake.body.insert(0, new_head)

snake = Snake(color=WHITE)

food = Food()

continue_game = True

while continue_game:
    
    screen.fill(BLACK)

    draw.rect(screen, food.color, (food.position.x, food.position.y, POINT_SIZE, POINT_SIZE))

    move_snake(snake, snake.direction)

    for point in snake.body:
        draw.rect(screen, snake.color, (point.x, point.y, POINT_SIZE, POINT_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.direction = Directions.LEFT
            elif event.key == pygame.K_RIGHT:
                snake.direction = Directions.RIGHT
            elif event.key == pygame.K_DOWN:
                snake.direction = Directions.DOWN
            elif event.key == pygame.K_UP:
                snake.direction = Directions.UP
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
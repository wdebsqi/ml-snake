import pygame, sys
from pygame import draw, Color, Rect
from PIL import Image
from src.config import *
from src.Directions import *
from src.Point import *
from src.Snake import *
from src.Food import *

#Game configuration
pygame.init()
pygame.display.set_caption('Snake')
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

#Load images
papaj = pygame.image.load('src/images/papaj.jpg')
papaj = pygame.transform.scale(papaj, (POINT_SIZE, POINT_SIZE))

kremowka = pygame.image.load('src/images/kremowka.png')
kremowka = pygame.transform.scale(kremowka, (POINT_SIZE, POINT_SIZE))


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

    #screen.blit(kremowka, (food.position.x, food.position.y, POINT_SIZE, POINT_SIZE))
    draw.rect(screen, food.color, (food.position.x, food.position.y, POINT_SIZE, POINT_SIZE))

    move_snake(snake, snake.direction)

    for point in snake.body:
        #screen.blit(papaj, (point.x, point.y, POINT_SIZE, POINT_SIZE))
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
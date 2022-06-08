from turtle import pos
import random
import pygame, sys
from pygame import draw, Color, Rect
from PIL import Image
from src.config import *
from src.Directions import *
from src.Point import *
from src.Snake import *
from src.Food import *

class Game():
    
    def __init__(self):
        #Game configuration
        pygame.init()
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0
        self.snake = Snake()
        self.font = pygame.font.Font('src/fonts/arial.ttf', 25)
        self.food = self._place_food()


    def _place_food(self) -> Food:
        x = random.randint(0, (width-POINT_SIZE)//POINT_SIZE)*POINT_SIZE
        y = random.randint(0, (height-POINT_SIZE)//POINT_SIZE)*POINT_SIZE
        position = Point(x, y)
        self.food = Food(position)
        if self.food.position in self.snake.body:
            self._place_food()
        return self.food


    def _update_frame(self):
        self.screen.fill(BLACK)

        #Display snake
        for point in self.snake.body:
            draw.rect(self.screen, self.snake.color2, (point.x, point.y, POINT_SIZE, POINT_SIZE))
            draw.rect(self.screen, self.snake.color1, (point.x+4, point.y+4, SMALL_POINT_SIZE, SMALL_POINT_SIZE))


        #Display food
        draw.rect(self.screen, self.food.color, (self.food.position.x, self.food.position.y, POINT_SIZE, POINT_SIZE))

        #Display score
        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(text, [0, 0])
        pygame.display.flip()
    

    def play_frame(self):

        # 1. Get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.direction = Directions.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.snake.direction = Directions.RIGHT
                elif event.key == pygame.K_DOWN:
                    self.snake.direction = Directions.DOWN
                elif event.key == pygame.K_UP:
                    self.snake.direction = Directions.UP
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
        # 2. Move snake
        self.snake.move(self.snake.direction)
        self.snake.body.insert(0, self.snake.head)

        # 3. Check if snake died
        if self.snake._is_collision():
            self.game_over = True
            return self.game_over, self.score

        # 4. Check if snake ate food
        if (self.snake.head.x == self.food.position.x) and (self.snake.head.y == self.food.position.y):
            #self.snake.body += self.snake.body.
            self.score += 1
            self._place_food()
        else:
            self.snake.body.pop()
            #pass

        print(f"{self.snake.head} in {self.snake.body[1:]}")

        # 5. Update frame
        self._update_frame()
        self.clock.tick(FPS)

        # 6. Return score
        return self.game_over, self.score
        
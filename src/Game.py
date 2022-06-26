import random
import pygame, sys
from pygame import draw
from config import *
from Directions import *
from Point import *
from Snake import *
from Food import *

class Game():
    def __init__(self) -> None:

        #Game configuration
        pygame.init()
        pygame.display.set_caption(WINDOW_NAME)
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('fonts/arial.ttf', 25)
        self.game_over = False
        self.food = None
        self.reset()


    def _place_food(self) -> Food:

        x = random.randint(0, (width-POINT_SIZE)//POINT_SIZE)*POINT_SIZE
        y = random.randint(0, (height-POINT_SIZE)//POINT_SIZE)*POINT_SIZE
        position = Point(x, y)
        self.food = Food(position)
        if self.food.position in self.snake.body:
            self._place_food()
        return self.food


    def _update_frame(self) -> None:

        self.screen.fill(BLACK)

        #Display snake
        for point in self.snake.body:
            draw.rect(self.screen, self.snake.color2, (point.x, point.y, POINT_SIZE, POINT_SIZE))
            draw.rect(self.screen, self.snake.color1, (point.x+SMALL_POINT_OFFSET, point.y+SMALL_POINT_OFFSET, SMALL_POINT_SIZE, SMALL_POINT_SIZE))

        #Display food
        draw.rect(self.screen, self.food.color, (self.food.position.x, self.food.position.y, POINT_SIZE, POINT_SIZE))

        #Display score
        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(text, [0, 0])
        pygame.display.flip()
    

    def play_frame(self, action) -> tuple((int, bool, int)):

        self.frame_iteration += 1

        # 1. Get events generated by user
        events = pygame.event.get()
        
        if len(events) > 0:
            # We only want one event per frame, thus we take only the last event that occured in this frame.
            # Otherwise the user can turn the snake back by quickly pressing two keys.
            event = events[-1]

            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

                
        # 2. Move snake
        self.snake.move(action)
        self.snake.body.insert(0, self.snake.head)

        # 3. Check if snake died
        reward = 0
        self.game_over = False

        if self.snake.is_collision() or self.frame_iteration > 100*len(self.snake.body):
            reward = -10
            self.game_over = True
            return reward, self.game_over, self.score

        # 4. Check if snake ate food
        if (self.snake.head.x == self.food.position.x) and (self.snake.head.y == self.food.position.y):
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.body.pop()

        # 5. Update frame
        self._update_frame()
        self.clock.tick(FPS)

        # 6. Return score
        return reward, self.game_over, self.score

    def reset(self):
        self.score = 0
        self.snake = Snake()
        self.food = self._place_food()
        self.frame_iteration = 0
        
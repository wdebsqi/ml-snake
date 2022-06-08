from src.Point import *
from src.config import *
from src.Directions import *
from src.Game import *
from pygame import Color


class Snake():
    def __init__(self, starting_point: Point = Point(MIDDLE_X, MIDDLE_Y), color1: Color = GREEN, color2: Color = GREEN2):
        self.head = starting_point
        self.body = [
            starting_point, 
            Point((starting_point.x-POINT_SIZE), starting_point.y),
            Point((starting_point.x-(POINT_SIZE*2)), starting_point.y)
            ]
        self.color1 = color1
        self.color2 = color2
        self.direction = Directions.RIGHT

    def move(self, direction: Directions):
        x = self.head.x
        y = self.head.y

        if direction == Directions.RIGHT:
            x += POINT_SIZE
        elif direction == Directions.LEFT:
            x -= POINT_SIZE
        elif direction == Directions.DOWN:
            y += POINT_SIZE
        elif direction == Directions.UP:
            y -= POINT_SIZE

        #self.body.pop()    
        self.head = Point(x, y)

    def _is_collision(self):
        #Hitting wall
        if (self.head.x > (width - POINT_SIZE)) or (self.head.x < 0) or (self.head.y > (height - POINT_SIZE)) or (self.head.y < 0):
            return True
        #Hitting self
        if (self.head.x in self.body[1:]):
            return True

        return False
    
    def can_move(self, new_direction: Directions):
        if ((self.direction == Directions.UP and new_direction == Directions.DOWN) or
            (self.direction == Directions.RIGHT and new_direction == Directions.LEFT) or
            (self.direction == Directions.DOWN and new_direction == Directions.UP) or
            (self.direction == Directions.LEFT and new_direction == Directions.RIGHT)):
            return False
        else:
            return True
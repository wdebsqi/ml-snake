from src.Point import *
from src.config import *
from src.Directions import *
from pygame import Color


class Snake():
    def __init__(self, starting_point: Point = Point(MIDDLE_X, MIDDLE_Y), color: Color = WHITE):
        self.body = [starting_point]
        self.color = color
        self.direction = Directions.RIGHT
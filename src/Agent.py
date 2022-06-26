import torch
import random
import numpy as np
from collections import deque
from Game import Game
from Directions import Directions
from Point import Point
from config import POINT_SIZE
from Model import Model
from Trainer import Trainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.01 # Learning Rate
INPUT_SIZE = 11
HIDDEN_SIZE = 256
OUTPUT_SIZE = 3

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0    # randomness
        self.gamma = 0.9    # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Model(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        self.trainer = Trainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game: Game):
        snake = game.snake
        point_l = Point(snake.head.x - POINT_SIZE, snake.head.y)
        point_r = Point(snake.head.x + POINT_SIZE, snake.head.y)
        point_u = Point(snake.head.x, snake.head.y - POINT_SIZE)
        point_d = Point(snake.head.x, snake.head.y + POINT_SIZE)

        dir_l = snake.direction == Directions.LEFT
        dir_r = snake.direction == Directions.RIGHT
        dir_u = snake.direction == Directions.UP
        dir_d = snake.direction == Directions.DOWN

        state = [
            # Danger straight
            (dir_r and snake.is_collision(point_r)) or
            (dir_l and snake.is_collision(point_l)) or
            (dir_u and snake.is_collision(point_u)) or
            (dir_d and snake.is_collision(point_d)),
            
            # Danger right
            (dir_u and snake.is_collision(point_r)) or
            (dir_d and snake.is_collision(point_l)) or
            (dir_l and snake.is_collision(point_u)) or
            (dir_r and snake.is_collision(point_d)),

            # Danger left
            (dir_d and snake.is_collision(point_r)) or
            (dir_u and snake.is_collision(point_l)) or
            (dir_r and snake.is_collision(point_u)) or
            (dir_l and snake.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food.position.x < snake.head.x,  # food left
            game.food.position.x > snake.head.x,  # food right
            game.food.position.y < snake.head.y,  # food up
            game.food.position.y > snake.head.y  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward: int, next_state, done: bool):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)    # list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward: int, next_state, done: bool):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff between exploration and exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()

    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_frame(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # rembember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
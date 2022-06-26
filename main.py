from src.Game import *

if __name__ == '__main__':
    game = Game()



    while True:
        game_over, game_score = game.play_frame()


        if game.game_over == True:
            break
from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
                

    def test_action(self, board):
        sandbox = board.clone()
        actions = ['Direction.Right']
        scores = []
        for action in actions:
            sandbox.move(action)
        sandbox.move(Direction.Drop)
        score = 1
        scores.append(score)
        index = 0
        return actions[index]
        

    def choose_action(self, board):
        # self.print_board(board)
        time.sleep(0.5)
        for cell in board.falling.cells:
            if cell[0] == 1:
                return Direction.Right
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])


SelectedPlayer = RandomPlayer

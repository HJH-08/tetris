from board import Direction, Rotation, Action
from random import Random
import time


number_of_bombs = 5
two_block_score = 9999
next_actions_list = []
rotations_list = [[],[Rotation.Clockwise],[Rotation.Clockwise,Rotation.Clockwise], [Rotation.Anticlockwise]]
actions_list = [[Direction.Left], [Direction.Left, Direction.Left], [Direction.Left, Direction.Left, Direction.Left], [Direction.Left, Direction.Left, 
Direction.Left, Direction.Left], [Direction.Left, Direction.Left, Direction.Left, Direction.Left, Direction.Left], [Direction.Right], [Direction.Right, Direction.Right], 
[Direction.Right, Direction.Right, Direction.Right], [Direction.Right, Direction.Right, Direction.Right, Direction.Right], 
[Direction.Right, Direction.Right, Direction.Right, Direction.Right, Direction.Right],[]]


class Player:
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

    def move_to_target(self, cloned_board, target_x):
        has_landed = False
        while target_x<cloned_board.falling.left and has_landed == False:
            has_landed = cloned_board.move(Direction.Left)    
        while target_x>cloned_board.falling.right and has_landed == False:
            has_landed = cloned_board.move(Direction.Right)
        return has_landed  
    
    def score(self, cloned_board):

        list_of_cells = cloned_board.cells
        sorted_list_of_cells = sorted(list(list_of_cells), key=lambda x: (x[0], x[1]))

        number_of_holes = 0
        for (x,y) in list_of_cells:
            if y==23:
                continue
            else:
                while y<=23:
                    if (x,y+1) in list_of_cells:
                        break
                    number_of_holes+=1
                    y+=1
        sum_of_heights = 0
        consecutive_height_difference = 0
        highest_y_point = 24
        highest_cell_in_each_column = {0:24, 1:24, 2:24, 3: 24, 4: 24, 5: 24, 6: 24, 7: 24, 8: 24, 9: 24}
        for (x,y) in sorted_list_of_cells:
            if highest_cell_in_each_column[x] >= y:
                highest_cell_in_each_column[x] = y
        for column in range(0,9):
            consecutive_height_difference += (abs(highest_cell_in_each_column[column] - highest_cell_in_each_column[column+1]))
        highest_y_point = min(highest_cell_in_each_column.values())
        lowest_y_point = max(highest_cell_in_each_column.values())
        greatest_height_difference = lowest_y_point - highest_y_point
        for height in highest_cell_in_each_column.values():
            sum_of_heights += (24-height)
        
        weightage_1 = 0.7
        weightage_2 = 2.5
        weightage_3 = 0.3
        weightage_4 = 0.8
        return weightage_1*(greatest_height_difference) + weightage_2*(number_of_holes) + weightage_3*(consecutive_height_difference) + weightage_4*sum_of_heights
    
    def test_action(self, board):

        global number_of_bombs
        global next_actions_list
        global two_block_score


        scores = []
        one_block_scores = []
        # sum_of_heights = 0
        # highest_cell_in_each_column = {0:24, 1:24, 2:24, 3: 24, 4: 24, 5: 24, 6: 24, 7: 24, 8: 24, 9: 24}
        # for (x,y) in board.cells:
        #     if highest_cell_in_each_column[x] >= y:
        #         highest_cell_in_each_column[x] = y
        # for height in highest_cell_in_each_column.values():
        #     sum_of_heights += (24-height)

        for rotations in rotations_list:
            for actions in actions_list:
                cloned_board = board.clone()
                has_landed = False
                for rotation in rotations:
                    cloned_board.rotate(rotation)
                for action in actions:
                    if not has_landed:
                        has_landed = cloned_board.move(action)
                if not has_landed:
                    has_landed = cloned_board.move(Direction.Drop)
                score = self.score(cloned_board)
                one_block_scores.append(score)
        # for rotations in rotations_list:
        #     for actions in actions_list:
        #         cloned_board = board.clone()
        #         has_landed = False
        #         for rotation in rotations:
        #             cloned_board.rotate(rotation)
        #         for action in actions:
        #             if not has_landed:
        #                 has_landed = cloned_board.move(action)
        #         if not has_landed:
        #             has_landed = cloned_board.move(Direction.Drop)
        #         for rotations in rotations_list:
        #             for actions in actions_list:
        #                 cloned_twice_board = cloned_board.clone()
        #                 has_landed = False
        #                 for rotation in rotations:
        #                     cloned_twice_board.rotate(rotation)
        #                 for action in actions:
        #                     if not has_landed:
        #                         has_landed = cloned_twice_board.move(action)
        #                 if not has_landed:
        #                     has_landed = cloned_twice_board.move(Direction.Drop)
        #                 score = self.score(cloned_twice_board)
        #                 scores.append(score)
        # if min(one_block_scores)>two_block_score:
        #     current_actions_list = next_actions_list
        #     next_actions_list = []
        #     print("ENTIRE TWO BLOCK SEQUENCE ACTIVE", min(one_block_scores), two_block_score)
        #     two_block_score = 9999

        # elif min(one_block_scores)<min(scores):
        index = one_block_scores.index(min(one_block_scores))
        current_actions_list = rotations_list[int(index/len(actions_list))] + actions_list[int(index%len(actions_list))] + [Direction.Drop]
            # two_block_score = 9999
            # print("ONE BLOCK SEQUENCE")
        # else:
        #     index = scores.index(min(scores))
        #     two_block_score = min(scores)
        #     current_actions_list = rotations_list[int(index/(len(actions_list) * len(actions_list) * len(rotations_list)))] + actions_list[int(index%(len(actions_list) * len(actions_list) * len(rotations_list))/(len(actions_list) * len(rotations_list)))]+ [Direction.Drop]
        #     if not next_actions_list:
        #         next_actions_list = rotations_list[int((index%(len(actions_list)*len(rotations_list)))/len(actions_list))] + actions_list[int(index%(len(actions_list)*len(rotations_list))%len(actions_list))]+[Direction.Drop]
        #     print("START OF TWO BLOCK SEQUENCE")
        return current_actions_list


    def choose_action(self, board):
        global next_actions_list
        # time.sleep(0.5)
        # # for cell in board.falling.cells:
        # #     if cell[0] == 1:
        # #         return Direction.Right
        actions = self.test_action(board)
        for action in actions:
            yield action
        


SelectedPlayer = Player

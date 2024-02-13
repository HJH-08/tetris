from board import Direction, Rotation, Action
from random import Random
import time

previous_discard = False
number_of_discards = 10
number_of_bombs = 5
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
    
    def score(self, cloned_board):
        list_of_cells = cloned_board.cells
        sorted_list_of_cells = sorted(list(list_of_cells), key=lambda x: (x[0], x[1]))
        number_of_holes = 0
        for (x,y) in list_of_cells:
            if y==23:
                continue
            else:
                while y<23:
                    if (x,y+1) in list_of_cells:
                        break
                    number_of_holes+=1
                    y+=1
        sum_of_heights = 0
        bumpiness = 0
        highest_y_point = 24
        highest_cell_in_each_column = {0:24, 1:24, 2:24, 3: 24, 4: 24, 5: 24, 6: 24, 7: 24, 8: 24, 9: 24}
        for (x,y) in sorted_list_of_cells:
            if highest_cell_in_each_column[x] >= y:
                highest_cell_in_each_column[x] = y
        for column in range(0,9):
            bumpiness += ((abs(highest_cell_in_each_column[column] - highest_cell_in_each_column[column+1]))**2)



        
        highest_y_point = min(highest_cell_in_each_column.values())
        lowest_y_point = max(highest_cell_in_each_column.values())
        greatest_height_difference = lowest_y_point - highest_y_point
        for height in highest_cell_in_each_column.values():
            sum_of_heights += (24-height)

        if highest_y_point<9:
            greatest_height_difference += 50
        if sum_of_heights>100 or highest_y_point<12:
            weightage_1 = 1.5
            weightage_2 = 150
            weightage_3 = 8
            weightage_4 = 30
        else:
            weightage_1 = 1.2
            weightage_2 = 150
            weightage_3 = 1.5
            weightage_4 = 10

        return weightage_1*(greatest_height_difference) + weightage_2*(number_of_holes) + weightage_3*(bumpiness) + weightage_4*sum_of_heights
    
    def test_action(self, board):

        global number_of_discards
        global previous_discard
        one_block_scores = []

        for rotations in rotations_list:
            for actions in actions_list:
                cloned_board = board.clone()
                previous_number_of_cells = len(cloned_board.cells)
                has_landed = False
                for rotation in rotations:
                    if not has_landed:
                        has_landed = cloned_board.rotate(rotation)
                for action in actions:
                    if not has_landed:
                        has_landed = cloned_board.move(action)
                if not has_landed:
                    has_landed = cloned_board.move(Direction.Drop)
                score = self.score(cloned_board)

                sum_of_heights = 0
                highest_cell_in_each_column = {0:24, 1:24, 2:24, 3: 24, 4: 24, 5: 24, 6: 24, 7: 24, 8: 24, 9: 24}
                for (x,y) in board.cells:
                    if highest_cell_in_each_column[x] >= y:
                        highest_cell_in_each_column[x] = y
                for height in highest_cell_in_each_column.values():
                    sum_of_heights += (24-height)

                after_number_of_cells = len(cloned_board.cells)
                
                highest_y_point = min(highest_cell_in_each_column.values())
           
                if sum_of_heights>100 or highest_y_point<12:
                    score = score
                else:
                    if after_number_of_cells-previous_number_of_cells == -6:
                        score = score * 1.33
                    elif after_number_of_cells-previous_number_of_cells == -16:
                        score = score * 1.12
                    elif after_number_of_cells-previous_number_of_cells == -26:
                        score = score * 0.7
                    elif after_number_of_cells-previous_number_of_cells == -36:
                        score = score * 0.01
                one_block_scores.append(score)
        index = one_block_scores.index(min(one_block_scores))

        current_actions_list = rotations_list[int(index/len(actions_list))] + actions_list[int(index%len(actions_list))] + [Direction.Drop]
        current_rotation_list = rotations_list[int(index/len(actions_list))]
        current_action_only_list = [action for action in current_actions_list if action not in current_rotation_list]
        
        cloned_board = board.clone()
        before_number_of_holes = 0
        for (x,y) in cloned_board.cells:
            if y==23:
                continue
            else:
                while y<23:
                    if (x,y+1) in cloned_board.cells:
                        break
                    before_number_of_holes+=1
                    y+=1
        has_landed = False
        for rotation in current_rotation_list:
            if not has_landed:
                has_landed = cloned_board.rotate(rotation)
        for action in current_action_only_list:
            if not has_landed:
                has_landed = cloned_board.move(action)
        after_number_of_holes = 0
        for (x,y) in cloned_board.cells:
            if y==23:
                continue
            else:
                while y<23:
                    if (x,y+1) in cloned_board.cells:
                        break
                    after_number_of_holes+=1
                    y+=1
        sum_of_heights = 0
        highest_cell_in_each_column = {0:24, 1:24, 2:24, 3: 24, 4: 24, 5: 24, 6: 24, 7: 24, 8: 24, 9: 24}
        for (x,y) in cloned_board.cells:
            if highest_cell_in_each_column[x] >= y:
                highest_cell_in_each_column[x] = y
        for height in highest_cell_in_each_column.values():
            sum_of_heights += (24-height)
        if number_of_discards and not previous_discard:
            if after_number_of_holes>(before_number_of_holes) and sum_of_heights>60:
                number_of_discards -= 1
                previous_discard = True
                return [Action.Discard]
        previous_discard = False
        return current_actions_list


    def choose_action(self, board):
        # time.sleep(0.5)
        actions = self.test_action(board)
        for action in actions:
            yield action
        

SelectedPlayer = Player

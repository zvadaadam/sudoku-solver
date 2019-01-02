import numpy as np

from Sudoku.solver import BacktrackingSolverStrategy
from Sudoku.solver import BackjumpingSolverStrategy


class Sudoku(object):

    def __init__(self, grid, strategy=None):
        self.grid = grid
        self.strategy = strategy

    def is_solved(self, grid):

        if self.is_valid(grid) and (0 not in grid):
            return True

        return False

    def is_valid(self, grid):

        for i in range(0, 9):

            # rows validity
            if not self.is_valid_line(axis=0, index=i, grid=grid):
                return False

            # columns validity
            if not self.is_valid_line(axis=1, index=i, grid=grid):
                return False

            # boxes validity
            row = int(i/3)*3
            column = (i % 3)*3
            if not self.is_valid_box(row, column, grid):
                return False


        return True

    def is_valid_line(self, axis, index, grid):

        line = []
        if axis == 0:
            line = grid[index, :]
        elif axis == 1:
            line = grid[:, index]
        else:
            raise Exception('Axis ut of bounds.')

        is_valid = self.check_sequence_validity(line)

        return is_valid

    def is_valid_box(self, row, column, grid):
        """3x3"""

        line = []
        for i in range(0,3):
            for j in range(0, 3):
                line.append(grid[(row + i), (column + j)])

        is_valid = self.check_sequence_validity(line)

        return is_valid

    def check_sequence_validity(self, sequence):

        if len(sequence) != 9:
            raise Exception('Sequence should be of length 9.')

        uniques, counts = np.unique(sequence, return_counts=True)

        for unique, count in zip(uniques, counts):
            if unique != 0 and count > 1:
                return False

        return True


    def solve(self):

        variables = []
        for i in range(0, 9):
            for j in range(0, 9):
                if self.grid[i][j] == 0:
                    variables.append((i, j))

        #return self.backtracking(grid, variables)
        return self.backjumping(grid, variables)

    def solve_strategy(self):

        variables = []
        for i in range(0, 9):
            for j in range(0, 9):
                if self.grid[i][j] == 0:
                    variables.append((i, j))

        return self.strategy.solve(self)
        #return self.backjumping(grid, variables)



    def used_in_axis(self, grid, axis, axis_index, num):
        for i in range(0, 9):

            if axis == 0:
                if (grid[axis_index][i] == num):
                    return True
            elif axis == 1:
                if (grid[i][axis_index] == num):
                    return True
            else:
                raise Exception('Not valid axis.')

        return False

    def used_in_box(self, grid, row, column, num):
        for i in range(3):
            for j in range(3):
                if (grid[i + row][j + column] == num):
                    return True

        return False

    def is_valid_location(self, arr, row, column, num):

        return not self.used_in_axis(arr, axis=0, axis_index=row, num=num) and \
               not self.used_in_axis(arr, axis=1, axis_index=column, num=num) and \
               not self.used_in_box(arr, row - row % 3, column - column % 3, num)

    def backtracking(self, grid, variables, num_steps=0):

        if len(variables) == 0:
            if not self.is_solved(grid):
                raise Exception('Should not happen.')
            return True, grid, num_steps+1

        # next unassigned value
        next_row, next_column = variables[0]
        new_variables = variables[1:]

        for i in range(1, 10):

            num_steps += 1

            if self.is_valid_location(grid, next_row, next_column, i):

                grid[next_row, next_column] = i

                status, new_grid, steps = self.backtracking(grid.copy(), new_variables, num_steps)
                if status:
                    return True, new_grid, steps

                num_steps = steps

                grid[next_row, next_column] = 0

        return False, grid, num_steps

    def find_conflicts(self, grid, row, column, num):

        conflicts = set()
        for i in range(9):
            if grid[row][i] == num:
                conflicts.add((row + i*8))

        for i in range(9):
            if grid[i][column] == num:
                conflicts.add((i + column*8))

        box_row = row - row % 3
        box_column = column - column % 3

        for i in range(3):
            for j in range(3):
                if (grid[i + box_row][j + box_column] == num):
                    conflicts.add(i + box_row + 8*(j + box_column))

        conflicts.add(row + 8*column)

        return conflicts

    def backjumping(self, grid, variables, num_steps=0):

        if len(variables) == 0:
            if not self.is_solved(grid):
                raise Exception('Should not happen.')
            return True, grid, num_steps + 1, set()

            # next unassigned value
        next_row, next_column = variables[0]
        new_variables = variables[1:]

        conflicts = set()

        for i in range(1, 10):

            num_steps += 1

            status = False
            new_grid = []
            steps = 0
            new_conflicts = set()
            if self.is_valid_location(grid, next_row, next_column, i):

                grid[next_row, next_column] = i

                status, new_grid, steps, new_conflicts = self.backjumping(grid.copy(), new_variables, num_steps)
            else:
                new_conflicts = self.find_conflicts(grid, next_row, next_column, i) # find all conflicts for i in (next_row, next_column)


            if status:
                return True, new_grid, steps, set()
            elif (next_row + 8*next_column) not in new_conflicts:
                return False, grid, num_steps, new_conflicts
            else:
                new_conflicts.remove(next_row + 8*next_column)
                conflicts = conflicts.union(new_conflicts)

            num_steps = steps
            grid[next_row, next_column] = 0


        return False, grid, num_steps, conflicts




if __name__ == '__main__':

    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    # grid = [
    #     [4, 0, 1, 2, 9, 0, 0, 7, 5],
    #     [2, 0, 0, 3, 0, 0, 8, 0, 0],
    #     [0, 7, 0, 0, 8, 0, 0, 0, 6],
    #     [0, 0, 0, 1, 0, 3, 0, 6, 2],
    #     [1, 0, 5, 0, 0, 0, 4, 0, 3],
    #     [7, 3, 0, 6, 0, 8, 0, 0, 0],
    #     [6, 0, 0, 0, 2, 0, 0, 3, 0],
    #     [0, 0, 7, 0, 0, 1, 0, 0, 4],
    #     [8, 9, 0, 0, 6, 5, 1, 0, 7],
    # ]

    grid = np.array(grid)
    sudoku = Sudoku(grid)
    print(sudoku.solve())

    sudoku = Sudoku(grid, strategy=BacktrackingSolverStrategy())
    print(sudoku.solve_strategy())

    sudoku = Sudoku(grid, strategy=BackjumpingSolverStrategy())
    print(sudoku.solve_strategy())

import abc


class SolverStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def solve(self, sudoku):
        pass


class BacktrackingSolverStrategy(SolverStrategy):

    def solve(self, sudoku):

        variables = []
        for i in range(0, 9):
            for j in range(0, 9):
                if sudoku.grid[i][j] == 0:
                    variables.append((i, j))

        return self.backtracking(sudoku, sudoku.grid, variables)

    def backtracking(self, sudoku, grid, variables, num_steps=0):

        if len(variables) == 0:
            if not sudoku.is_solved(grid):
                raise Exception('Should not happen.')
            return True, grid, num_steps+1

        # next unassigned value
        next_row, next_column = variables[0]
        new_variables = variables[1:]

        for i in range(1, 10):

            num_steps += 1

            if sudoku.is_valid_location(grid, next_row, next_column, i):

                grid[next_row, next_column] = i

                status, new_grid, steps = self.backtracking(sudoku, grid.copy(), new_variables, num_steps)
                if status:
                    return True, new_grid, steps

                num_steps = steps

                grid[next_row, next_column] = 0

        return False, grid, num_steps



class BackjumpingSolverStrategy(SolverStrategy):

    def solve(self, sudoku):

        variables = []
        for i in range(0, 9):
            for j in range(0, 9):
                if sudoku.grid[i][j] == 0:
                    variables.append((i, j))

        return self.backjumping(sudoku, sudoku.grid, variables)

    def backjumping(self, sudoku, grid, variables, num_steps=0):

        if len(variables) == 0:
            if not sudoku.is_solved(grid):
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
            if sudoku.is_valid_location(grid, next_row, next_column, i):

                grid[next_row, next_column] = i

                status, new_grid, steps, new_conflicts = self.backjumping(sudoku, grid.copy(), new_variables, num_steps)
            else:
                new_conflicts = sudoku.find_conflicts(grid, next_row, next_column, i) # find all conflicts for i in (next_row, next_column)

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
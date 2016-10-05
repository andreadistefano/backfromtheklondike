from itertools import product

""""
Solver for Sam Loyd's Back from the Klondike Puzzle using Heuristic Search.
For info about the rules: https://en.wikipedia.org/wiki/Back_from_the_Klondike
"""


class BackFromTheKlondikeHeuristic:

    def H(self, state):
        """" Returns the cost of a state, which is the Chebyshev distance
        (also known as chessboard distance) between the current position
        and the closest exit.
        For more info: https://en.wikipedia.org/wiki/Chebyshev_distance
        """
        return state.cost


class Board:
    """"
    This class contains 2 tuples-of-tuples and an integer:
    - board, which contains the whole game board.
        Cells marked with -1 are invalid positions.
        Cells marked with 0 are winning positions, or exits.
        Cells marked with any other number are valid positions, and the number
        indicates how many steps the player must take in the next turn, in a
        straight line in any of the 8 cardinal directions:
        north, northeast, east, southeast, south, southwest, west, northwest.
    - cost, which contains the Chebyshev distance (also known as chessboard
        distance) between each position and the closest exit. For more info
        https://en.wikipedia.org/wiki/Chebyshev_distance
    - size, which indicates the size of the board
    """
    board = (
          (-1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
          (-1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  4,  7,  7,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1),
          (-1, -1, -1, -1,  0,  0,  0,  5,  4,  4,  8,  3,  3,  4,  6,  3,  0,  0,  0, -1, -1, -1, -1),
          (-1, -1, -1,  0,  0,  1,  4,  5,  1,  1,  1,  4,  5,  1,  7,  1,  3,  5,  0,  0, -1, -1, -1),
          (-1, -1,  0,  0,  4,  9,  4,  9,  6,  7,  5,  5,  5,  8,  7,  6,  6,  8,  5,  0,  0, -1, -1),
          (-1, -1,  0,  3,  7,  2,  9,  8,  3,  5,  6,  7,  3,  9,  1,  8,  7,  5,  8,  5,  0, -1, -1),
          (-1,  0,  0,  1,  4,  7,  8,  4,  2,  9,  2,  7,  1,  1,  8,  2,  2,  7,  6,  3,  0,  0, -1),
          (-1,  0,  7,  2,  1,  8,  5,  5,  3,  1,  1,  3,  1,  3,  3,  4,  2,  8,  6,  1,  3,  0, -1),
          (-1,  0,  4,  2,  6,  7,  2,  5,  2,  4,  2,  2,  5,  4,  3,  2,  8,  1,  7,  7,  3,  0, -1),
          ( 0,  0,  4,  1,  6,  5,  1,  1,  1,  9,  1,  4,  3,  4,  4,  3,  1,  9,  8,  2,  7,  0,  0),
          ( 0,  4,  3,  5,  2,  3,  2,  2,  3,  2,  4,  2,  5,  3,  5,  1,  1,  3,  5,  5,  3,  7,  0),
          ( 0,  2,  7,  1,  5,  1,  1,  3,  1,  5,  3,  3,  2,  4,  2,  3,  7,  7,  5,  4,  2,  7,  0),
          ( 0,  2,  5,  2,  2,  6,  1,  2,  4,  4,  6,  3,  4,  1,  2,  1,  2,  6,  5,  1,  8,  8,  0),
          ( 0,  0,  4,  3,  7,  5,  1,  9,  3,  4,  4,  5,  2,  9,  4,  1,  9,  5,  7,  4,  8,  0,  0),
          (-1,  0,  4,  1,  6,  7,  8,  3,  4,  3,  4,  1,  3,  1,  2,  3,  2,  3,  6,  2,  4,  0, -1),
          (-1,  0,  7,  3,  2,  6,  1,  5,  3,  9,  2,  3,  2,  1,  5,  7,  5,  8,  9,  5,  4,  0, -1),
          (-1,  0,  0,  1,  6,  7,  3,  4,  8,  1,  1,  1,  2,  1,  2,  2,  8,  9,  4,  1,  0,  0, -1),
          (-1, -1,  0,  2,  5,  4,  7,  8,  7,  5,  6,  1,  3,  5,  7,  8,  7,  2,  9,  3,  0, -1, -1),
          (-1, -1,  0,  0,  6,  5,  6,  4,  6,  7,  2,  5,  2,  2,  6,  3,  4,  7,  4,  0,  0, -1, -1),
          (-1, -1, -1,  0,  0,  2,  3,  1,  2,  3,  3,  3,  2,  1,  3,  2,  1,  1,  0,  0, -1, -1, -1),
          (-1, -1, -1, -1,  0,  0,  0,  7,  4,  4,  5,  7,  3,  4,  4,  7,  0,  0,  0, -1, -1, -1, -1),
          (-1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  3,  3,  4,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1),
          (-1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1)
    )

    costs = (
          (-1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
          (-1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1),
          (-1, -1, -1, -1,  0,  0,  0,  1,  1,  1,  1,  2,  1,  1,  1,  1,  0,  0,  0, -1, -1, -1, -1),
          (-1, -1, -1,  0,  0,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  1,  1,  1,  0,  0, -1, -1, -1),
          (-1, -1,  0,  0,  1,  1,  2,  2,  2,  3,  3,  3,  3,  3,  2,  2,  2,  1,  1,  0,  0, -1, -1),
          (-1, -1,  0,  1,  1,  2,  2,  3,  3,  3,  4,  4,  4,  3,  3,  3,  2,  2,  1,  1,  0, -1, -1),
          (-1,  0,  0,  1,  2,  2,  3,  3,  4,  4,  4,  5,  4,  4,  4,  3,  3,  2,  2,  1,  0,  0, -1),
          (-1,  0,  1,  1,  2,  3,  3,  4,  4,  5,  5,  5,  5,  5,  4,  4,  3,  3,  2,  1,  1,  0, -1),
          (-1,  0,  1,  2,  2,  3,  4,  4,  5,  5,  6,  6,  6,  5,  5,  4,  4,  3,  2,  2,  1,  0, -1),
          ( 0,  0,  1,  2,  3,  3,  4,  5,  5,  6,  6,  7,  6,  6,  5,  5,  4,  3,  3,  2,  1,  0,  0),
          ( 0,  1,  1,  2,  3,  4,  4,  5,  6,  6,  7,  7,  7,  6,  6,  5,  4,  4,  3,  2,  1,  1,  0),
          ( 0,  1,  2,  2,  3,  4,  5,  5,  6,  7,  7,  8,  7,  7,  6,  5,  5,  4,  3,  2,  2,  1,  0),
          ( 0,  1,  1,  2,  3,  4,  4,  5,  6,  6,  7,  7,  7,  6,  6,  5,  4,  3,  3,  2,  1,  1,  0),
          ( 0,  0,  1,  2,  3,  3,  4,  5,  5,  6,  6,  7,  6,  6,  5,  5,  4,  3,  3,  2,  1,  0,  0),
          (-1,  0,  1,  2,  2,  3,  4,  4,  5,  5,  6,  6,  6,  5,  5,  4,  4,  3,  2,  2,  1,  0, -1),
          (-1,  0,  1,  1,  2,  3,  3,  4,  4,  5,  5,  5,  5,  5,  4,  4,  3,  3,  2,  1,  1,  0, -1),
          (-1,  0,  0,  1,  2,  2,  3,  3,  4,  4,  4,  5,  4,  4,  4,  3,  3,  2,  2,  1,  0,  0, -1),
          (-1, -1,  0,  1,  1,  2,  2,  3,  3,  3,  4,  4,  4,  3,  3,  3,  2,  2,  1,  1,  0, -1, -1),
          (-1, -1,  0,  0,  1,  1,  2,  2,  2,  3,  3,  3,  3,  3,  2,  2,  2,  1,  1,  0,  0, -1, -1),
          (-1, -1, -1,  0,  0,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  1,  1,  1,  0,  0, -1, -1, -1),
          (-1, -1, -1, -1,  0,  0,  0,  1,  1,  1,  1,  2,  1,  1,  1,  1,  0,  0,  0, -1, -1, -1, -1),
          (-1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1),
          (-1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1)
    )

    size = len(board)


class BackFromTheKlondikeState:

    def __init__(self, row, col, parent, heuristic):
        self.row = row
        self.col = col
        self.currentValue = Board.board[row][col]
        self.parent = parent
        self.H = heuristic

    def isAdmissible(self):
        return self.currentValue != -1

    def getValue(self):
        return self.currentValue

    @property
    def cost(self):
        return Board.costs[self.row][self.col]

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def __ne__(self, other):
        return not self == other

    def show(self):
        for i in range(Board.size):
            for j in range(Board.size):
                if (i, j) == (self.row, self.col):
                    print("X", end=" ")
                elif Board.board[i][j] != -1:
                    print(Board.board[i][j], end=" ")
                else:
                    print("_", end=" ")
            print("")
        print("")


class BackFromTheKlondikeGame:

    def __init__(self, row, col, heuristic):
        initState = BackFromTheKlondikeState(row, col, None, heuristic)
        self.state = initState
        self.heuristic = heuristic

    def neighbors(self, state):
        out = set()
        v = state.getValue()
        # Finds all possible neighbors using the Cartesian product
        # (row - v, row, row + v) x (col - v, col, col + v).
        # This gives us 9 couples of coordinates:
        # (row - v, col - v), (row - v, col), (row - v, col + v)
        # (row, col - v), (row, col), (row, col + v)
        # (row + v, col - v), (row + v, col), (row + v, col + v)
        for new_r, new_c in product((state.row-v, state.row, state.row+v),
                                    (state.col-v, state.col, state.col+v)):
            # We exclude coordinates if they are the same as the current ones
            # or if they are out of the board bounds
            if (new_r, new_c) != (state.row, state.col) and
            0 <= new_r < Board.size and
            0 <= new_c < Board.size:
                sign_r = (new_r - state.row) // v   # Normalize number of steps
                sign_c = (new_c - state.col) // v   # giving -1, 0 or 1
                # We now use these values to check if the 2nd-last cell value
                # is not 0, in order to only add states from which the player
                # can exactly exit from the board, thus winning the game
                if Board.board[new_r - sign_r][new_c - sign_c] != 0:
                    h = self.heuristic
                    new_s = BackFromTheKlondikeState(new_r, new_c, state, h)
                    # We also check if the value of that state is not -1
                    # to avoid adding invalid states
                    if new_s.isAdmissible():
                        out.add(new_s)
        return out

    def get_state(self):
        return self.state

    def solution(self, state):
        return state.currentValue == 0


dict_of_states = {}


def argMin(set_of_states):
    # We use a lambda function to get the state in the set to which
    # corresponds the entry in the dictionary with minimum value
    return min(set_of_states, key=lambda st: dict_of_states.get(st, 100))


def pick(set_of_states):
    return argMin(set_of_states)


def backpath(state):
    # Returns the path from the starting point to the winning state
    father = state.parent
    states_list = [state]
    while father is not None:
        states_list.append(father)
        father = father.parent
    return reversed(states_list)


def search(game, state0):
    horizon = set()    # Set of states to visit
    explored = set()   # Set of visited states
    horizon.add(state0)     # Add the first state to horizon before loop
    while horizon:          # We loop until there are states in the horizon
        view = pick(horizon)   # Picks the state for which the heuristic is min
        if view is not None:    # If we could pick a state from the horizon
            if game.solution(view):     # Check if the current state is final
                return backpath(view)   # If so we return the path to victory
            else:
                horizon.remove(view)       # Else, remove it from the horizon
                explored.add(view)         # We add it to the explored set
                for s in game.neighbors(view):  # Check what to add to horizon
                    if s not in explored:      # Add not visited states only
                        dict_of_states[s] = game.heuristic.H(s)  # Compute its
                        # heuristic value and add it to the dict
                        horizon.add(s)     # Finally we add it to the horizon
    return None     # If we get here we return without having found a solution


# Main
if __name__ == "__main__":
    heuristic = BackFromTheKlondikeHeuristic()
    game = BackFromTheKlondikeGame(row=11, col=11, heuristic=heuristic)
    state0 = game.get_state()
    dict_of_states[state0] = heuristic.H(state0)
    solution = search(game, state0)
    if solution:
        print("Solution found!")
        for s in solution:
            print("({:2d}, {:2d}) -> {}".format(s.row, s.col, s.getValue()))
    else:
        print("No solution found")

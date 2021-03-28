import random


# class game table
class Table:

    def __init__(self):
        self.__occupied_cells = []
        self.__count_x = 0
        self.__count_o = 0
        self.__current_state = '_' * 9  # empty table is a default state

    def get_current_state(self):
        return self.__current_state

    # updates the game table and returns last added symbol
    def update_state(self, x, y):
        state = self.get_current_state()
        rows = [state[:3], state[3:6], state[6:]]
        old_row = rows[x - 1]
        new_row = ''
        # the symbol to be used by player to make a move
        # depending on the current state
        symbol = self.get_symbol()
        # replace the '_' element with the symbol 'X' or 'O'
        for i in range(len(old_row)):
            if i == y - 1:
                new_row += old_row[i].replace('_', symbol)
            else:
                new_row += old_row[i]
        rows[x - 1] = new_row
        self.clear_occupied_cells()
        self.clear_counts()
        self.__current_state = ''.join(rows)
        return symbol

    def get_occupied_cells(self):
        return self.__occupied_cells

    def add_occupied_cells(self, x, y):
        self.__occupied_cells.append((x, y))

    def clear_occupied_cells(self):
        self.__occupied_cells = []

    def get_count_x(self):
        return self.__count_x

    def update_count_x(self):
        self.__count_x += 1

    def get_count_o(self):
        return self.__count_o

    def update_count_o(self):
        self.__count_o += 1

    def clear_counts(self):
        self.__count_x = 0
        self.__count_o = 0

    # returns the symbol to be used by player to make a move
    def get_symbol(self):
        if self.get_count_x() <= self.get_count_o():
            return 'X'
        else:
            return 'O'

    # returns the value of the cell
    def get_cell_value(self, x, y):
        state = self.get_current_state()
        rows = [state[:3], state[3:6], state[6:]]
        return rows[x - 1][y - 1]

    # parameter seq is for user input sequence of X and O
    def draw_table(self):
        # variable of table's current state
        state = self.get_current_state()
        # separate the sequence into 3 rows
        rows = [state[:3], state[3:6], state[6:]]
        # draw horizontal borders and game field (nested loops)
        print('-' * 9)
        for row_idx, row in enumerate(rows):
            table_row = '|'
            for column_idx, cell in enumerate(row):
                if cell == '_':
                    table_row += '  '
                else:
                    table_row += ' ' + cell
                    self.add_occupied_cells(row_idx + 1, column_idx + 1)
                    if cell == 'X':
                        self.update_count_x()
                    elif cell == 'O':
                        self.update_count_o()
            table_row += ' |'
            print(table_row)
        print('-' * 9)

    def get_status(self, symbol=''):
        # conditions to check for a win
        cond_1 = all(self.get_cell_value(i, i) == symbol for i in range(1, 4))
        cond_2 = all(self.get_cell_value(i, 4 - i) == symbol for i in range(1, 4))
        cond_3 = (
                all(self.get_cell_value(1, j) == symbol for j in range(1, 4))
                or all(self.get_cell_value(2, j) == symbol for j in range(1, 4))
                or all(self.get_cell_value(3, j) == symbol for j in range(1, 4))
        )
        cond_4 = (
                all(self.get_cell_value(i, 1) == symbol for i in range(1, 4))
                or all(self.get_cell_value(i, 2) == symbol for i in range(1, 4))
                or all(self.get_cell_value(i, 3) == symbol for i in range(1, 4))
        )
        if len(self.get_occupied_cells()) < 9:
            if any([cond_1, cond_2, cond_3, cond_4]):
                print(f'{symbol} wins')
                return True
            else:
                return False
        else:
            if any([cond_1, cond_2, cond_3, cond_4]):
                print(f'{symbol} wins')
                return True
            else:
                print('Draw!')
                return True


# class player
class Player:

    def __init__(self, name):
        self.name = name

    @classmethod
    def make_move(cls):
        while True:
            move = input('Enter the coordinates: ')
            if not all([coord.isdigit() for coord in move.split()]):
                print('You should enter numbers!')
            elif tuple(int(coord) for coord in move.split()) in table.get_occupied_cells():
                print('This cell is occupied! Choose another one!')
            elif any([int(coord) < 1 or int(coord) > 3 for coord in move.split()]):
                print('Coordinates should be from 1 to 3!')
            else:
                coords = tuple(int(coord) for coord in move.split())
                return coords


# class for AI
class Computer:

    # levels = ["easy", "medium", "hard"]

    def __init__(self):
        self.level = 'easy'

    def make_move(self):
        print(f'Making move level "{self.level}"')
        # comp gets a list of free cells
        free_cells = []
        for i in range(1, 4):
            for j in range(1, 4):
                if (i, j) not in table.get_occupied_cells():
                    free_cells.append((i, j))
                else:
                    continue
        coords = random.choice(free_cells)
        return coords


# main game process
if __name__ == '__main__':
    # create player, opponent(comp) and empty table
    player = Player('Aidar')
    comp = Computer()
    table = Table()
    table.draw_table()
    # game process
    while True:
        # player's move
        player_move = player.make_move()
        last_added_symbol = table.update_state(player_move[0], player_move[1])
        table.draw_table()
        if table.get_status(last_added_symbol):
            break
        # comp's move
        comp_move = comp.make_move()
        last_added_symbol = table.update_state(comp_move[0], comp_move[1])
        table.draw_table()
        if table.get_status(last_added_symbol):
            break

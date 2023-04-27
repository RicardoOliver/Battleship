import random
import os.path

# Define constants for the grid size and ship size
GRID_SIZE = 4
SHIP_SIZE = 2

# Define symbols for displaying hit and unhit cells
HIT_SYMBOL = 'X'
UNHIT_SYMBOL = '-'

# Define a function to display the grid
def display_grid(grid):
    print('   ' + ' '.join([chr(i) for i in range(ord('A'), ord('A') + GRID_SIZE)]))
    for i in range(GRID_SIZE):
        print(str(i+1).rjust(2) + ' ' + ' '.join(grid[i]))

# Define a function to place a ship on the grid
def place_ship(grid):
    while True:
        # Generate a random position and orientation for the ship
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        orientation = random.choice(['horizontal', 'vertical'])
        
        # Check if the ship fits in the chosen position and orientation
        if orientation == 'horizontal' and col + SHIP_SIZE <= GRID_SIZE and all([grid[row][col+i] == UNHIT_SYMBOL for i in range(SHIP_SIZE)]):
            for i in range(SHIP_SIZE):
                grid[row][col+i] = UNHIT_SYMBOL + 'x' + UNHIT_SYMBOL
            break
        elif orientation == 'vertical' and row + SHIP_SIZE <= GRID_SIZE and all([grid[row+i][col] == UNHIT_SYMBOL for i in range(SHIP_SIZE)]):
            for i in range(SHIP_SIZE):
                grid[row+i][col] = UNHIT_SYMBOL + 'x' + UNHIT_SYMBOL
            break

# Define a function to get the player's move
def get_player_move():
    while True:
        move = input('Enter your move (e.g. A4): ')
        if len(move) != 2 or not move[0].isalpha() or not move[1].isdigit() or ord(move[0]) < ord('A') or ord(move[0]) >= ord('A') + GRID_SIZE or int(move[1]) < 1 or int(move[1]) > GRID_SIZE:
            print('Invalid move. Please try again.')
        else:
            return (ord(move[0]) - ord('A'), int(move[1]) - 1)

# Define a function to get the computer's move
def get_computer_move(grid):
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if grid[row][col] == UNHIT_SYMBOL:
            return (row, col)

# Define a function to update the grid after a move
def update_grid(grid, row, col):
    if grid[row][col] == UNHIT_SYMBOL:
        grid[row][col] = UNHIT_SYMBOL + HIT_SYMBOL + UNHIT_SYMBOL
        return True
    else:
        return False

# Define a function to check if a player has won
def check_win(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j][1] == 'x':
                return False
    return True

# Define a function to save the game state to a file
def save_game_state(player_grid, computer_grid):
    with open('game_state.txt','w') as file:
        # Write the player grid to the file
        file.write('Player grid:\n')
        for row in player_grid:
            file.write(' '.join(row) + '\n')
        # Write the computer grid to the file
        file.write('Computer grid:\n')
        for row in computer_grid:
            file.write(' '.join(row) + '\n')

# Define a function to load the game state from a file
def load_game_state():
    if not os.path.isfile('game_state.txt'):
        return None, None
    with open('game_state.txt', 'r') as file:
        lines = file.readlines()
        player_grid = [[cell for cell in row.strip().split()] for row in lines[1:GRID_SIZE+1]]
        computer_grid = [[cell for cell in row.strip().split()] for row in lines[GRID_SIZE+3:2*GRID_SIZE+3]]
        return player_grid, computer_grid

# Define the main game loop
def play_game():
    # Load the game state from a file or initialize a new game
    player_grid, computer_grid = load_game_state()
    if player_grid is None or computer_grid is None:
        player_grid = [[UNHIT_SYMBOL]*GRID_SIZE for _ in range(GRID_SIZE)]
        computer_grid = [[UNHIT_SYMBOL]*GRID_SIZE for _ in range(GRID_SIZE)]
        place_ship(player_grid)
        place_ship(computer_grid)
    
    # Play the game until one side wins
    while True:
        # Display the grids
        print('Player grid:')
        display_grid(player_grid)
        print('Computer grid:')
        display_grid(computer_grid)
        
        # Get the player's move
        print('Your turn:')
        row, col = get_player_move()
        hit = update_grid(computer_grid, row, col)
        if hit:
            print('You hit the computer\'s ship!')
            if check_win(computer_grid):
                print('Congratulations, you won!')
                save_game_state(player_grid, computer_grid)
                break
        else:
            print('You missed.')
        
        # Get the computer's move
        print('Computer\'s turn:')
        row, col = get_computer_move(player_grid)
        hit = update_grid(player_grid, row, col)
        if hit:
            print('The computer hit your ship!')
            if check_win(player_grid):
                print('Sorry, you lost.')
                save_game_state(player_grid, computer_grid)
                break
        else:
            print('The computer missed.')

# Start the game
play_game()

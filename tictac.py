# -----------------------------------------------------------------------------
# Name:       tictac
# Purpose:    Implement a game of Tic Tac Toe
#
# Author:     Caroline Liu
# -----------------------------------------------------------------------------
'''
Module to implement and play a game of tic tac toe against the computer.
'''
import tkinter
import random

class Game(object):
    '''
    Implement a game of tic tac between the user and the computer.

    Argument:
    parent (tkinter.TK): root window

    Attributes:
    parent (tkinter.TK): root window
    canvas (tkinter.Canvas): canvas representing game board
    bottom_message (tkinter.Label): win/lose/tie message in the bottom
    grid_id (dictionary): keeps track of squares occupied by each player
    game_in_progress (boolean): game status to see if game is in progress
    '''

    tile_size = 100     # Size of square tiles on board
    user_color = '#5f9ea0'  # Color of user's squares
    computer_color = '#f9ab8a' # Color of computer's squares

    def __init__(self, parent):
        parent.title('Tic Tac Toe')

        self.parent = parent

        # Restart button widget at the top
        restart_button = tkinter.Button(self.parent,
                                        text='RESTART',
                                        width=8,
                                        command=self.restart)
        restart_button.grid()

        # Initialize tic tac toe board
        self.draw_board()

        # Initialize dictionary to identify squares on board
        self.grid_id = {square:0 for square in self.canvas.find_all()}

        # Assign id's to squares on grid: 1 - 9
        self.assign_square_id()

        # Click event handler for board
        self.canvas.bind("<Button-1>", self.play)

        # Label widget located at the bottom for the win/lose message
        self.bottom_message = tkinter.Label(parent,
                                       text='',
                                       width=20)
        self.bottom_message.grid()

        # Game status instance variable
        self.game_in_progress = True

    def draw_board(self):
        """
        Initializes a 3 x 3 tic tac toe board with white squares.

        Parameters:
        none
        Return:
        none
        """
        # Canvas widget
        self.canvas = tkinter.Canvas(self.parent,
                                     width=self.tile_size * 3,
                                     height=self.tile_size * 3)
        self.canvas.grid()

        # Draw white squares in 3x3 formation
        for row in range(3):
            for column in range(3):
                self.canvas.create_rectangle(self.tile_size * column,
                                             self.tile_size * row,
                                             self.tile_size * (column + 1),
                                             self.tile_size * (row + 1),
                                             fill='white')

    def assign_square_id(self):
        """
        Assigns each square on the tic tac toe board a number value (1 - 9)
        in the grid_id dictionary.

        Parameters:
        none
        Return:
        none
        """
        count = 1
        for square in self.canvas.find_all():
            self.grid_id[square] = count
            count += 1

    def restart(self):
        """
        Reinitialize the game by resetting square colors, botom label,
        grid id's, and game status.

        Parameters:
        none
        Return:
        none
        """
        # Reset square colors
        for square in self.canvas.find_all():
            self.canvas.itemconfigure(square, fill='white')

        # Reset bottom label
        self.bottom_message.configure(text='')

        # Reset grid id's
        self.assign_square_id()

        # Reset game status
        self.game_in_progress = True

    def check_win(self, player):
        """
        Check for wins horizontally, vertically, and diagonally
        and updates bottom message and game status if there is a win.

        Parameters:
        player (string): type of player ('user' or 'computer')
        Return:
        none
        """
        # All 8 possible wins in tic tac toe
        row_win1 = [1,2,3]
        row_win2 = [4,5,6]
        row_win3 = [7,8,9]
        col_win1 = [1,4,7]
        col_win2 = [2,5,8]
        col_win3 = [3,6,9]
        diag_win1 = [1,5,9]
        diag_win2 = [3,5,7]
        all_wins = [row_win1, row_win2, row_win3,
                    col_win1, col_win2, col_win3,
                    diag_win1, diag_win2]

        # Determine if checking for player or computer
        if player == 'user':
            player_type = 0     # Square id for user move
            outcome_message = 'You win!'
        elif player == 'computer':
            player_type = -1    # Square id for computer move
            outcome_message = 'You lose!'

        # Check for win according to player type
        # Update bottom message accordingly
        for win_type in all_wins:
            play_track = 0
            for square_num in win_type:
                if self.grid_id[square_num] == player_type:
                    play_track += 1
            if play_track == 3:  # Player gets 3 in a row
                self.bottom_message.configure(text = outcome_message)
                self.game_in_progress = False   # Game over

    def play(self, event):
        """
        Method invoked when user clicks on a square to attempt a move.
        Authorizes and represents user moves in user's color and after,
        determines whether the computer is allowed to move.

        Parameters:
        none
        Return:
        none
        """
        # Check if user can move
        if self.game_in_progress:
            user_square = self.canvas.find_closest(event.x, event.y)[0]
            user_square_id = self.grid_id[user_square]
            if user_square_id != 0 and user_square_id != -1:

                # User moves, square id marked '0', and square filled
                self.canvas.itemconfigure(user_square, fill=self.user_color)
                self.grid_id[user_square] = 0

                # If user didn't win, computer plays after if space allows
                self.check_win('user')
                if self.game_in_progress:
                    spaces_left = \
                        [square for square in self.grid_id
                         if self.grid_id[square] > 0]
                    if len(spaces_left) > 0:
                        self.computer_move()
                        self.check_win('computer')

                    # If board is full and user didn't win, it's a tie
                    else:
                        self.bottom_message.configure(text='It\'s a tie!')
                        self.game_in_progress = False   # Game over

    def computer_move(self):
        """
        The computer generates random spaces until it finds an open space to
        make a move, then represents the move in the computer's color.

        Parameters:
        none
        Return:
        none
        """
        # Generate random number to pick random square
        my_random_int = random.randint(1, 9)
        comp_square_id = self.grid_id[my_random_int]

        # Keep generating until computer gets open space to play
        while comp_square_id == 0 or comp_square_id == -1:
            my_random_int = random.randint(1, 9)
            comp_square_id = self.grid_id[my_random_int]

        # Computer moves, square id is marked '-1', and square filled
        self.canvas.itemconfigure(comp_square_id, fill=self.computer_color)
        self.grid_id[comp_square_id] = -1
    
def main():
    root = tkinter.Tk()
    my_game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()
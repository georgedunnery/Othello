"""
George Dunnery
CS 5001 Homework #7 - Othello (8x8 version) - Module
11/28/2018

Self-Citation:
Reviewed code from module spaceship.py (HW5) to help write the flat file
processing functions. 
"""

# MODULES & CONSTANTS ----------------------------------------------------------
import turtle
import math
import os
import time
import random

SQUARE = 50
RADIUS = 40
FILE = 'scores.txt'

# CLASS: GAME ------------------------------------------------------------------
class Game:
    """
    Class to represent the game. The game has two players, a board
    Attributes: size, board, players, turn
    Required in constructor: size
    Optional in constructor: none
    default values: turn = 2
    """
    def __init__(self, size):
        self.players = [Player('human', 'b'), Player('computer', 'w')]
        self.turn = 2
        self.scoreboard = []
        self.ai_moves = []
        try:
            self.size = int(size)
            if self.size < 2:
                self.size = int(4)
        except ValueError:
            self.size = int(4)
        self.board = Board(size)

    def __str__(self):
        printme = ""
        for i in range(len(self.scoreboard)):
            printme += (str(self.scoreboard[i][0]) + ' ' + \
                       str(self.scoreboard[i][1]) + '\n')
        return printme

    def prepare_game(self):
        """
        Parameters: none
        Does: runs a routine at the beginning of the game: draws the board,
        generates the nested list, finds the center of the board, places the
        starting stones, updates the nested list
        Returns: nothing, but updates several board attributes 
        """
        draw_board(self.size)
        self.board.generate_index()
        self.board.find_center()
        self.board.start_stones()
        self.board.update_layout(self.board.center_boxes)
        for p in range(len(self.players)):
            self.scoreboard.append([self.players[p].name, self.players[p].score])

    def launch(self):
        """
        Parameters: None
        Does: Assists in structuring flow of control by initiating the first 
        turn of the game
        Returns: Nothing
        """
        turtle.onscreenclick(self.play_human)
        print("CURRENT TURN: Human")


    def play_human(self,x,y):
        """
        Parameters: x and y, integer coordinates passed automatically by turtle
        when the user clicks on the board.
        Does: Contains the script for the human player's turn
        Returns: Nothing, but calls the play_computer method at the end
        """
        # Clear old move, check if this player can have a turn or not
        self.board.new_moves = [[]]
        turtle.ht()
        turtle.penup()
        turtle.goto(x,y)
        x = math.floor(((x + (self.board.size * self.board.square / 2))
                        / self.board.square))
        y = math.floor(((-y + (self.board.size * self.board.square / 2))
                        / self.board.square))
        if x in range(self.board.size) and y in range(self.board.size):
            self.board.new_moves = [[y, x, self.players[0].color]]
            if self.board.is_legal(self.board.new_moves) == True:
                self.board.update_layout(self.board.new_moves)
                to_flip = self.board.flip(self.board.new_moves,
                                            self.board.hitbox)
                self.board.update_layout(to_flip)
                self.update_scoreboard()
                self.play_computer()

    def play_computer(self):
        """
        Parameters: None
        Does: Contains the script for the computer player's turn. The computer's
        turn also handles ending the game and rerouting turns when one player
        has none but the other does
        Returns: Nothing, but calls the player's turn when finished by
        turning onscreenclick back on!
        """
        print("CURRENT TURN: Computer")
        turtle.onscreenclick(None)
        turn_decision = self.is_over()
        if turn_decision[1] == False:
            self.board.new_moves = [self.ai_moves[random.randint\
                                                  (0,(len(self.ai_moves) - 1))]]
            self.board.is_legal(self.board.new_moves)
            self.board.update_layout(self.board.new_moves)
            to_flip = self.board.flip(self.board.new_moves,
                                      self.board.hitbox)
            self.board.update_layout(to_flip)
            self.update_scoreboard()
            turn_decision = self.is_over()
            if turn_decision[0] == False:
                print("CURRENT TURN: Human")
                turtle.onscreenclick(self.play_human)
            elif turn_decision[1] == False:
                self.play_computer()
            else:
                self.end_game()
        elif turn_decision[0] == False:
            print("CURRENT TURN: Human")
            turtle.onscreenclick(self.play_human)
        else:
            self.end_game()

    def clicked(self,x,y):
        # this is the old clicked function, which works perfectly for playing
        # both colors. Leaving it here for reference while writing play_human
        # and play_computer
        """
        Paramters: x, y, integer coordinates where the user clicked on the board
        Does: Updates new_moves with the place clicked, if it is within the
        board. New_moves meant to be passed to update_layout. Due to the
        asynchronous nature of the onscreenclick function in turtle, this
        method acts as the hub of the whole game...
        Returns: Nothing
        """
        turtle.ht()
        turtle.penup()
        turtle.goto(x,y)
        x = math.floor(((x + (self.board.size * self.board.square / 2))
                        / self.board.square))
        y = math.floor(((-y + (self.board.size * self.board.square / 2))
                        / self.board.square))
        if x not in range(self.board.size) or y not in range(self.board.size):
            self.board.new_moves = [[]]
        else:
            self.board.new_moves = [[y, x, self.which_color()]]
            #print(self.board.new_moves)
            #print(self.board.is_legal(self.board.new_moves))
            if self.board.is_legal(self.board.new_moves) == True:
                # Still place the actual move as usual
                self.board.update_layout(self.board.new_moves)
                # Now, find the sandwhiched stones, and flip em!
                self.board.update_layout(self.board.flip(self.board.new_moves,
                                                         self.board.hitbox))
                self.turn += 1
                self.update_scoreboard()
            else:
                self.board.new_moves = [[]]
        if self.is_over() == True:
            self.is_winner()
            print("Closing in 10 seconds, thanks for playing!")
            time.sleep(10)
            os._exit(0)
            # Add flat file functionality for HW 7!

    def which_color(self):
        """
        Parameters: none
        Does: picks the color of the stone placed based on attribute turn
        Returns: string, color of the stone to be placed
        """
        try:
            if self.turn % 2 == 0:
                return self.players[0].color
            elif self.turn % 2 == 1:
                return self.players[1].color
        except TypeError:
            return None

    def is_over(self):
        """
        Parameters: none
        Does: checks for legal moves with current board layout
        Returns: nested list of booleans, True when a player cannot make any
        moves.
        """
        turn_decision = []
        self.ai_moves = []
        human_legal = 0
        comp_legal = 0
        for row in range(len(self.board.board_stones)):
            for col in range(len(self.board.board_stones[row])):
                if self.board.board_stones[row][col] == 'x':
                    if self.board.is_legal([[row, col, self.players[0].color]])\
                       == True:
                        human_legal += 1
                    if self.board.is_legal([[row, col, self.players[1].color]])\
                       == True:
                        comp_legal += 1
                        self.ai_moves.append([row, col, self.players[1].color])
        # clear memory of bounceable stones
        self.board.hitbox = []
        if human_legal == 0:
            turn_decision.append(True)
        else:
            turn_decision.append(False)
        if comp_legal == 0:
            turn_decision.append(True)
        else:
            turn_decision.append(False)
        return turn_decision
            

    def update_scoreboard(self):
        """
        Parameters: none
        Does: counts the stones for each player. resets the score and does a 
        recount every time, so that the method can account for losing/gaining
        many stones at a time in the full version of othello
        Returns: nothing, updates player.score attributes to reflect the number
        of stones each player has on the board, updates game.scoreboard
        """
        for p in range(len(self.players)):
            self.players[p].score = 0
            for row in range(len(self.board.board_stones)):
                for column in range(len(self.board.board_stones[row])):
                    if self.board.board_stones[row][column] ==\
                    self.players[p].color:
                        self.players[p].score += 1
            self.scoreboard[p][1] = self.players[p].score
            
    def is_winner(self):
        """
        Parameters: none
        Does: compares the number of stones each player has, announces the
        winner and the number of stones they had (the winner's score)
        Returns: winner
        """
        print("-----------")
        winner = []
        if self.players[0].score > self.players[1].score:
            print(self.players[0].name, 'has won with', self.players[0].score,
                  'stones!')
            winner = [self.players[0].name]
        elif self.players[0].score < self.players[1].score:
            print(self.players[1].name, 'has won with', self.players[1].score,
                  'stones!')
            winner = [self.players[1].name]
        else:
            print(self.players[0].name, 'had', self.players[0].score, 'stones!')
            print(self.players[1].name, 'had', self.players[1].score, 'stones!')
            print('It was a tie!')
            winner = [self.players[0].name, self.players[1].name]
        print("-----------")
        return winner

    def end_game(self):
        """
        Parameters: None
        Does: Coordinates the file processing for saving scores by calling
        file processing functions.
        Returns: Nothing
        """
        winner = self.is_winner()
        username = str(input("Enter a name for posterity:\n"))
        score = self.players[0].score
        if verify_existence(FILE) == False:
            append_score(FILE, username, score)
        elif verify_existence(FILE) == True:
            old_scores = read_score(FILE)
            if score > compare(old_scores):
                insert_score(FILE, username, score, old_scores)
            else:
                append_score(FILE, username, score)
        print("---------------------------------")
        print("Score saved, thanks for playing!")
        print("The game will close in 3 seconds.")
        print("---------------------------------")
        time.sleep(3)
        os._exit(0)

# CLASS: PLAYER ----------------------------------------------------------------
class Player:
    """
    Class to represent a player
    Attributes: score, name, color
    Required in constructor: name, color
    Optional in constructor: score
    default values: score = 0
    """
    def __init__(self, name, color, score = 0):
        self.name = str(name)
        self.color = str(color)
        self.score = int(score)

# CLASS: BOARD -----------------------------------------------------------------
class Board:
    """
    Class to represent the game board for Othello
    Attributes: size, square, board_stones, center_boxes, new_moves
    Required in constructor: size
    Optional in constructor: square
    default values: square = 50, board_stones = [], center_boxes = [],
    new_moves = [[]]
    """
    def __init__(self, size, square = 50):
        self.size = size
        self.square = square
        self.board_stones = []
        self.center_boxes = []
        self.new_moves = [[]]
        self.hitbox = []
        
    def __str__(self):
        printme = str(self.board_stones)
        return printme

    def generate_index(self):
        """
        Parameters: none
        Does: generates a list of lists to represent all the boxes
        in the rows/columns of the othello board
        Returns: nothing
        """
        try:
            for i in range(self.size):
                self.board_stones.append([])
                for j in range(self.size):
                    self.board_stones[i].append("x")
        except TypeError:
            self.board_stones = ['bad_size']

    def find_center(self):
        """
        Parameters: none
        Does: finds the 4 center boxes with a formula
        Returns: nothing, but it does update the attribute center_boxes with a
        list containing the 4 center boxes
        """
        try:
            self.center_boxes.append([(self.size // 2 - 1),(self.size // 2 - 1)])
            self.center_boxes.append([(self.size // 2 - 1),(self.size // 2)])
            self.center_boxes.append([(self.size // 2),(self.size // 2 - 1)])
            self.center_boxes.append([(self.size // 2),(self.size // 2)])
        except TypeError:
            self.center_boxes = []

    def start_stones(self):
        """
        Parameters: none
        Does: takes list of center_boxes, appends the color of the stone to each
        ordered pair in the list generated by find_center
        Returns: nothing, but it updates the attribute center_boxes with the
        color of each stone that is to be placed at the start of the game
        """
        try:
            self.center_boxes[0].append('w')
            self.center_boxes[1].append('b')
            self.center_boxes[2].append('b')
            self.center_boxes[3].append('w')
        except IndexError:
            self.center_boxes.append('Unable to assign color')

    def update_layout(self, places):
        """
        Parameters: nested list containing ordered pairs with colors, can take
        one or more. Even if there is just one set of data, it MUST be a nested
        list to work
        Does: calls the draw_stone function to draw the stones, then updates
        the nested list board_stones to represent the new layout of the board
        Returns: nothing, but it updates the attribute board_stones
        """
        try:
            for i in range(len(places)):
                row = places[i][0]
                column = places[i][1]
                color = places[i][2]
                y = int(((self.size / 2) * self.square -
                                (places[i][0] * self.square) - 25))
                x = int(((self.size / 2) * (-self.square) +
                                (places[i][1] * self.square) + 25))
                mark = [x, y, color]
                draw_stone(mark)
                self.board_stones[row][column] = str(color)
        except IndexError:
            return False
        except TypeError:
            return False

    def is_open(self, box):
        """
        Parameter: box, nested list with box coordinates
        Does: checks if there is already a tile there
        Returns: boolean
        """
        row = box[0][0]
        column = box[0][1]
        if self.board_stones[row][column] == 'x':
            return True
        else:
            return False

    def is_legal(self, box):
        """
        Parameter: box, nested list with box coordinates
        Does: checks if the move was legal or not by calling check_dir with
        row and column increments to point in all the cardinal directions
        Returns: boolean
        """
        enemy = ""
        friend = box[0][2]
        if friend == "w":
            enemy = "b"
        else:
            enemy = "w"
        if self.is_open(box) == True:
            # Seeking: down, up, right, left, SE, NE, SW, NW
            legality = 0
            for row in range(-1,2):
                for col in range(-1,2):
                    if self.check_dir(box, row, col, friend, enemy) == True:
                        legality += 1
            if legality >= 1:
                return True
        return False

    def check_dir(self, box, row_inc, col_inc, friend, enemy):
        """
        Name: check_dir, as in "check direction"
        Parameters: box, a nested list of coordinates. row_inc and col_inc,
        integers to add to the row and/or the column in order to increment
        through the list - i.e. look in a direction on the board. friend, string
        with color of active player's stones. enemy, string with color of the
        opponent's stones.
        Does: checks if the adjacent stone in the specified direction is an
        enemy stone, and that at some point we encounter a consecutive friendly
        stone. It checks for the "sandwiching" of an enemy stone. Intended to be
        called repeatedly in is_legal to check all 8 cardinal directions. When
        a sandwiched stone is found, it is appended to a nested list attribute
        called hitbox so that the process doesn't have to be repeated in the
        flipping function. 
        Returns: booelan, updates board attribute hitbox
        """
        # Special Case: immediate neighbor MUST be an enemy
        try:
            row = box[0][0] + row_inc
            col = box[0][1] + col_inc
            if self.board_stones[row][col] == enemy:
                # General Case: next box must not be empty, eventually friendly
                while ((row >= 0 and row <= self.size - 1) and \
                      (col >= 0 and col <= self.size - 1)):
                    if self.board_stones[row][col] == "x":
                        return False
                    elif self.board_stones[row][col] == friend:
                        self.hitbox.append([row_inc, col_inc, row, col])
                        return True
                    else:
                        row += row_inc
                        col += col_inc
            return False
        except IndexError:
            return False

    def flip(self, move, hitbox):
        """
        Parameters: move, a nested list with coordinates and color of the new
        move, expects to receive new_moves. hitbox, nested list containing the
        row_inc and col_inc (integers to increment row and/or column) and the
        row / column coordinates of the friendly stone.
        Does: seeks the locations between the new move and the sandwhiching
        friendly stones. This is intended to be passed directly into the
        update_layout method - the stones are not flipped by this method, but
        rather the places to change are identified.
        Returns: nested list, coordinates of stones to be flipped and which
        color to flip to
        """
        start = []
        end = []
        to_be_flipped = []
        for stone in range(len(hitbox)):
            start = [move[0][0], move[0][1]]
            end = [hitbox[stone][2], hitbox[stone][3]]
            while not (start[0] == end[0] and start[1] == end[1]):
                to_be_flipped.append([start[0], start[1], move[0][2]])
                start[0] += hitbox[stone][0]
                start[1] += hitbox[stone][1]
        return to_be_flipped
   

# FUNCTIONS --------------------------------------------------------------------
def draw_stone(info):
    """
    Parameter: List containing coordinates, integers, and color, string
    Does: Draws a dot of the specified color at the coordinates
    Returns: nothing
    """
    turtle.penup()
    turtle.goto(info[0],info[1])
    if info[2] == 'b':
        turtle.dot(RADIUS, "black")
    elif info[2] == 'w':
        turtle.dot(RADIUS, "white")

def verify_existence(filename):
    """
    Parameter: filename, string containing the name of the file
    Does: checks if the file exists by attempting to open it
    Returns: boolean, file exists or doesn't exist
    """
    try:
        infile = open(filename, 'r')
        infile.close()
        return True
    except FileNotFoundError:
        return False
    
def read_score(filename):
    """
    Parameters: filename, string, name of the file to read
    Does: extracts the data from the file into a list the program can use
    Returns: list containing old scores that were saved
    """
    try:
        infile = open(filename, 'r')
        old_scores = infile.readlines()
        infile.close()
        for score in range(len(old_scores)):
            old_scores[score] = old_scores[score].strip('\n')
        return old_scores
    except OSError:
        return []

def append_score(filename, username, score):
    """
    Parameters: filename, string, name of file. username, string, player's
    chosen name to record. score, int, the number of stones the player had
    Does: appends the user's name and score to the end of the scores.txt file
    Returns: Nothing
    """
    outfile = open(filename, 'a')
    outfile.write(str(username) + ' ' + str(score) + '\n')
    outfile.close()

def insert_score(filename, username, score, old_scores):
    """
    Parameters: filename, string, the name of the file. username, string,
    the user's chosen name to record. score, int, the number of stones the
    user had at the end of the game. old_scores, list of strings, the contents
    of the file prior to being overwritten.
    Does: Overwrites the file. Puts the new high score first, then writes
    the old scores below the new high score
    Returns: Nothing
    """
    outfile = open(filename, 'w')
    outfile.write(str(username) + ' ' + str(score) + '\n')
    for score in range(len(old_scores)):
        outfile.write(old_scores[score] + '\n')
    outfile.close()

def compare(leaderboard):
    """
    Parameter: list, strings of data read from a file
    Does: removes the names from the leaderboard, and then passes the integer
    scores to the higest function
    Returns: greatest integer score found in the file
    """
    try:
        just_scores = []
        for score in leaderboard:
            score = score.split(' ')
            just_scores.append(int(score[-1]))
        return highest(just_scores)
    except IndexError:
        return 0
        
def highest(just_scores):
    """
    Parameter: list of integers
    Does: seeks the largest integer
    Returns: largest integer from the list
    """
    try:
        if len(just_scores) == 1:
            return just_scores[0]
        else:
            if just_scores[0] > highest(just_scores[1:]):
                return just_scores[0]
            else:
                return highest(just_scores[1:])
    except IndexError:
        return 0


# CS 5001 STARTER CODE ---------------------------------------------------------
def draw_board(n):
    """
    Function: draw_board
    Parameters: n, an int for # of squares
    Returns: nothing
    Does: Draws an nxn board with a green background
    """

    turtle.setup(n * SQUARE + SQUARE, n * SQUARE + SQUARE)
    turtle.screensize(n * SQUARE, n * SQUARE)
    turtle.bgcolor('white')

    # Create the turtle to draw the board
    othello = turtle.Turtle()
    othello.penup()
    othello.speed(20)
    othello.hideturtle()

    # Line color is black, fill color is green
    othello.color("black", "forest green")
    
    # Move the turtle to the upper left corner
    corner = -n * SQUARE / 2
    othello.setposition(corner, corner)
  
    # Draw the green background
    othello.begin_fill()
    for i in range(4):
        othello.pendown()
        othello.forward(SQUARE * n)
        othello.left(90)
    othello.end_fill()

    # Draw the horizontal lines
    for i in range(n + 1):
        othello.setposition(corner, SQUARE * i + corner)
        draw_lines(othello, n)

    # Draw the vertical lines
    othello.left(90)
    for i in range(n + 1):
        othello.setposition(SQUARE * i + corner, corner)
        draw_lines(othello, n)

def draw_lines(turt, n):
    turt.pendown()
    turt.forward(SQUARE * n)
    turt.penup()
    

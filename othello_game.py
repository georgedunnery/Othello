"""
George Dunnery
CS 5001 - Homework #7 - Othello 8x8 Driver
11/28/2018
"""

import turtle
from othello import *

SIZE = 8

def main():

    # Initialize the game logic and start the game
    # Flow of control is handed off to a call and response pattern between:
    # game.play_human, game.play_computer
    game = Game(SIZE)
    game.prepare_game()
    game.launch()
    
main()

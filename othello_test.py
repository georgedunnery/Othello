"""
George Dunnery
CS 5001 Homework #7 - Othello (8x8 version) - Test Suite
11/28/2018
"""

import unittest
import turtle
from othello import *
turtle.ht()
turtle.speed(1000)
ORIGINAL = ['velma 64', 'scooby 32', 'shaggy 0']

"""
ORDER OF TESTING ---------------------------------------------------------------

The test suite will focus on one class at a time, and then deal with any
leftover functions before running main().

OMITTED METHODS / FUNCTIONS ----------------------------------------------------

Certain methods are not accounted for in the test suite. The following is an
explanation of their ommission. I am confident that the game will still be
stable despite these omissions. 

1. game.launch(): This method is omitted because it is merely a tool to help
    iron out the flow of control. It only calls the play_human method to
    get the ball rolling at the beginning of the game. After that, the two
    player turns have a call and response while there are legal moves to be
    made. 
2. game.play_human(): Omitted because it is merely a collection of other methods.
    Since it will call the computer's turn at the end of the script, it proved
    difficult to test. The ai is unpredictable, making it impossible to verify
    by checking attributes. Playing the game shows that the method works
    sufficiently. This function is a revision of the clicked function. Clicked
    was vigorously tested in Othello 4x4, and is vigorously tested again in
    Othello 8x8, with changes made to the test to account for increasing
    game logic complexity.
3. game.play_computer(): Similarly to game.play_human, this method is omitted
    because it is a collection of other methods. Furthermore, the random aspect
    of the ai makes it impossible to predict what will happen. I know that the
    computer will always make a legal move because legal_moves is used as a
    failsafe (and to catch sandwiching stones) in the method. In addition,
    the tests run for the is_over method grants confidence that the turns
    will work as we expect them to - if a player can't make a move, the other
    player goes again, and the game ends when no moves are left. Playing the
    game demonstrates the orchestration of these methods is running smoothly.
"""

print("\n------- Welcome to the Othello (8x8 Version) Test Suite -------\n"
      "You will see several turtle windows open as tests are performed.\n"
      "----------------------------------------------------------------\n")
        
# TEST CLASS: Player -----------------------------------------------------------
class PlayerTest(unittest.TestCase):
    """
    class to test all the methods from the Player class
    * __init__
    """
    def test_init(self):
        person = Player('test', 'b')
        self.assertEqual(person.name, 'test')
        self.assertEqual(person.color, 'b')
        self.assertEqual(person.score, 0)

        person = Player(55, 10, 500)
        self.assertEqual(person.name, '55')
        self.assertEqual(person.color, '10')
        self.assertEqual(person.score, 500)

# TEST CLASS: Board ------------------------------------------------------------
class BoardTest(unittest.TestCase):
    """
    class to test all the methods from the Board class
    * __init__
    * __str__
    * generate_index
    * find_center
    * start_stones
    * update_layout
    * is_open
    * check_dir
    * is_legal
    * flip
    """

    def test_init(self):
        board = Board(4)
        self.assertEqual(board.size, 4)
        self.assertEqual(board.square, 50)
        self.assertEqual(board.board_stones, [])
        self.assertEqual(board.center_boxes, [])
        self.assertEqual(board.new_moves, [[]])

        board = Board(8, 100)
        self.assertEqual(board.size, 8)
        self.assertEqual(board.square, 100)
        self.assertEqual(board.board_stones, [])
        self.assertEqual(board.center_boxes, [])
        self.assertEqual(board.new_moves, [[]])

        board = Board(0, 0)
        self.assertEqual(board.size, 0)
        self.assertEqual(board.square, 0)
        self.assertEqual(board.board_stones, [])
        self.assertEqual(board.center_boxes, [])
        self.assertEqual(board.new_moves, [[]])

        board = Board('a', 'b')
        self.assertEqual(board.size, 'a')
        self.assertEqual(board.square, 'b')
        self.assertEqual(board.board_stones, [])
        self.assertEqual(board.center_boxes, [])
        self.assertEqual(board.new_moves, [[]])

    def test_str(self):
        board = Board(4)
        expected = "[]"
        self.assertEqual(board.__str__(), expected)

        board = Board(4)
        board.board_stones = ['x', 'x', 'x', 'x']
        expected = "['x', 'x', 'x', 'x']"
        self.assertEqual(board.__str__(), expected)

        board = Board(4)
        board.board_stones = [['x', 'w', 'b', 'Q']]
        expected = "[['x', 'w', 'b', 'Q']]"
        self.assertEqual(board.__str__(), expected)

        board = Board(4)
        board.board_stones = 100
        expected = "100"
        self.assertEqual(board.__str__(), expected)
        
    def test_generate_index(self):
        board = Board(4)
        board.generate_index()
        expected = [['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x']]
        self.assertEqual(board.board_stones, expected)

        board = Board(8)
        board.generate_index()
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(board.board_stones, expected)

        board = Board(1)
        board.generate_index()
        expected = [['x']]
        self.assertEqual(board.board_stones, expected)

        board = Board(0)
        board.generate_index()
        expected = []
        self.assertEqual(board.board_stones, expected)

        board = Board(-1)
        board.generate_index()
        expected = []
        self.assertEqual(board.board_stones, expected)

        board = Board('a')
        board.generate_index()
        expected = ['bad_size']
        self.assertEqual(board.board_stones, expected)

    def test_find_center(self):
        board = Board(4)
        board.find_center()
        expected = [[1,1,],[1,2,],[2,1,],[2,2]]
        self.assertEqual(board.center_boxes, expected)

        board = Board(8)
        board.find_center()
        expected = [[3,3],[3,4],[4,3],[4,4]]
        self.assertEqual(board.center_boxes, expected)

        board = Board(0)
        board.find_center()
        expected = [[-1, -1], [-1, 0], [0, -1], [0, 0]]
        self.assertEqual(board.center_boxes, expected)

        board = Board(-8)
        board.find_center()
        expected = [[-5, -5], [-5, -4], [-4, -5], [-4, -4]]
        self.assertEqual(board.center_boxes, expected)

        board = Board('bad')
        board.find_center()
        expected = []
        self.assertEqual(board.center_boxes, expected)

    def test_start_stones(self):
        board = Board(4)
        board.find_center()
        board.start_stones()
        expected = [[1, 1, 'w'], [1, 2, 'b'], [2, 1, 'b'], [2, 2, 'w']]
        self.assertEqual(board.center_boxes, expected)

        board = Board(8)
        board.find_center()
        board.start_stones()
        expected = [[3, 3, 'w'], [3, 4, 'b'], [4, 3, 'b'], [4, 4, 'w']]
        self.assertEqual(board.center_boxes, expected)

        board = Board('bad')
        board.find_center()
        board.start_stones()
        expected = ['Unable to assign color']
        self.assertEqual(board.center_boxes, expected)

        board = Board(0)
        board.find_center()
        board.start_stones()
        expected = [[-1, -1, 'w'], [-1, 0, 'b'], [0, -1, 'b'], [0, 0, 'w']]
        self.assertEqual(board.center_boxes, expected)

        board = Board(-8)
        board.find_center()
        board.start_stones()
        expected = [[-5, -5, 'w'], [-5, -4, 'b'], [-4, -5, 'b'], [-4, -4, 'w']]
        self.assertEqual(board.center_boxes, expected)

    def test_update_layout(self):
        board = Board(4)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)
        expected = [['x', 'x', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(board.board_stones, expected)
        turtle.clear()

        board = Board(8)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)
        expected =[['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'w', 'b', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(board.board_stones, expected)
        turtle.clear()
        
        board = Board(0)
        board.generate_index()
        board.find_center()
        board.start_stones()
        self.assertFalse(board.update_layout(board.center_boxes))

        board = Board('bad')
        board.generate_index()
        board.find_center()
        board.start_stones()
        self.assertFalse(board.update_layout(board.center_boxes))

        board = Board(4)
        board.generate_index()
        bad_list = [[0, 0, 0]]
        board.update_layout(bad_list)
        expected = [['0', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(board.board_stones, expected)
        turtle.clear()

    def test_is_open(self):
        board = Board(4)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)

        boxes = [[[1,1]],[[1,2]],[[2,1]],[[2,2]]]
        for nested_list in range(len(boxes)):
            self.assertFalse(board.is_open(boxes[nested_list]))

        boxes = [[[0,0]],[[0,1]],[[0,2]],[[0,3]],
                 [[1,0]],[[1,3]],[[2,0]],[[2,3]],
                 [[3,0]],[[3,1]],[[3,2]],[[3,3]]]
        for nested_list in range(len(boxes)):
            self.assertTrue(board.is_open(boxes[nested_list]))

        board.new_moves = [[0,0,'b'],[0,3,'w'],[3,0,'b'],[3,3,'w']]
        board.update_layout(board.new_moves)

        boxes = [[[0,0]],[[0,3]],[[1,1]],[[1,2]],[[2,1]],[[2,2]],[[3,0]],
                 [[3,3]]]
        for nested_list in range(len(boxes)):
            self.assertFalse(board.is_open(boxes[nested_list]))

        boxes = [[[0,1]],[[0,2]],[[1,0]],[[1,3]],[[2,0]],[[2,3]],[[3,1]],
                 [[3,2]]]
        for nested_list in range(len(boxes)):
            self.assertTrue(board.is_open(boxes[nested_list]))

    def test_check_dir(self):
        # Critical function, tested thoroughly for all 8 cardinal directions!
        board = Board(8)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)

        # RIGHT INVALID
        board.new_moves = [[3,7,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[3,7,'w']], 0, 1, 'w', 'b'))

        board.new_moves = [[3,2,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[3,2,'w']], 0, 1, 'w', 'b'))

        board.new_moves = [[0,0,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[0,0,'b']], 0, 1, 'b', 'w'))
        
        # RIGHT VALID
        board.new_moves = [[3,1,'b']]
        board.update_layout(board.new_moves)
        self.assertTrue(board.check_dir([[3,1,'b']], 0, 1, 'b', 'w'))

        # LEFT INVALID
        board.new_moves = [[4,5,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[4,5,'w']], 0, -1, 'w', 'b'))

        board.new_moves = [[4,7,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[4,7,'w']], 0, -1, 'w', 'b'))

        board.new_moves = [[0,1,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[0,1,'w']], 0, -1, 'w', 'b'))
        
        # LEFT VALID
        board.new_moves = [[3,5,'w']]
        board.update_layout(board.new_moves)
        self.assertTrue(board.check_dir([[3,5,'w']], 0, -1, 'w', 'b'))

        # UP INVALID
        board.new_moves = [[4,1,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[4,1,'b']], -1, 0, 'b', 'w'))

        board.new_moves = [[2,1,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[2,1,'b']], -1, 0, 'b', 'w'))

        board.new_moves = [[5,5,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[5,5,'b']], -1, 0, 'b', 'w'))
        
        # UP VALID
        board.new_moves = [[5,4,'b']]
        board.update_layout(board.new_moves)
        self.assertTrue(board.check_dir([[5,4,'b']], -1, 0, 'b', 'w'))
               
        # DOWN INVALID
        board.new_moves = [[1,0,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[1,0,'w']], 1, 0, 'w', 'b'))

        board.new_moves = [[2,2,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[2,2,'w']], 1, 0, 'w', 'b'))

        board.new_moves = [[1,1,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[1,1,'w']], 1, 0, 'w', 'b'))
        
        # DOWN VALID
        board.new_moves = [[2,4,'w']]
        board.update_layout(board.new_moves)
        self.assertTrue(board.check_dir([[2,4,'w']], 1, 0, 'w', 'b'))

        # SE INVALID
        board.new_moves = [[4,6,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[4,6,'b']], 1, 1, 'b', 'w'))

        board.new_moves = [[3,2,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[3,2,'b']], 1, 1, 'b', 'w'))

        board.new_moves = [[2,0,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[2,0,'w']], 1, 1, 'w', 'b'))
        
        # SE VALID
        board.new_moves = [[1,3,'b']]
        board.update_layout(board.new_moves)
        self.assertTrue(board.check_dir([[1,3,'b']], 1, 1, 'b', 'w'))     

        # NE INVALID
        board.new_moves = [[2,5,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[2,5,'w']], -1, 1, 'w', 'b'))

        board.new_moves = [[3,0,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[3,0,'w']], -1, 1, 'w', 'b'))

        board.new_moves = [[2,0,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[2,0,'w']], -1, 1, 'w', 'b'))
        
        # NE VALID
        board.new_moves = [[5,2,'w']]
        board.update_layout(board.new_moves)
        self.assertTrue(board.check_dir([[5,2,'w']], -1, 1, 'w', 'b'))

        # SW INVALID
        board.new_moves = [[4,2,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[4,2,'b']], 1, -1, 'b', 'w'))

        board.new_moves = [[0,2,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[0,2,'b']], 1, -1, 'b', 'w'))

        board.new_moves = [[2,3,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[2,3,'b']], 1, -1, 'b', 'w'))
        
        # SW VALID
        board.new_moves = [[1,5,'b']]
        board.update_layout(board.new_moves)
        self.assertTrue(board.check_dir([[1,5,'b']], 1, -1, 'b', 'w'))
        """
        Chart to keep track of check direction testing on a single board
                      0    1    2    3    4    5    6    7
                0  [['b', 'w', 'b', 'x', 'x', 'x', 'x', 'x'],
                1   ['w', 'w', 'x', 'b', 'x', 'b', 'x', 'x'],
                2   ['w', 'b', 'w', 'b', 'w', 'w', 'x', 'x'],
                3   ['b', 'b', 'b', 'w', 'b', 'w', 'x', 'w'],
                4   ['x', 'b', 'b', 'b', 'w', 'w', 'b', 'w'],
                5   ['x', 'x', 'w', 'x', 'b', 'b', 'x', 'x'],
                6   ['x', 'x', 'x', 'x', 'x', 'b', 'x', 'x'],
                7   ['x', 'x', 'x', 'x', 'x', 'x', 'w', 'x']]
        """
        # NW INVALID
        board.new_moves = [[3,0,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[3,0,'b']], -1, -1, 'b', 'w'))

        board.new_moves = [[6,5,'b']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[6,5,'b']], 1, -1, 'b', 'w'))

        board.new_moves = [[5,2,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[5,2,'w']], 1, -1, 'w', 'b'))

        # NW VALID
        board.new_moves = [[7,6,'w']]
        board.update_layout(board.new_moves)
        self.assertFalse(board.check_dir([[7,6,'w']], 1, -1, 'w', 'b'))
        
    def test_is_legal(self):
        turtle.clear()
        board = Board(4)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)

        # Uses hard coded flipping
        board.new_moves = [[0,1,'b']]
        self.assertTrue(board.is_legal(board.new_moves))
        board.update_layout([[0,1,'b'],[1,1,'b']])

        board.new_moves = [[0,0,'w']]
        self.assertTrue(board.is_legal(board.new_moves))
        board.update_layout([[0,0,'w'],[1,1,'w']])

        board.new_moves = [[0,2,'w']]
        self.assertTrue(board.is_legal(board.new_moves))
        board.update_layout([[0,2,'w'],[0,1,'w']])

        turtle.clear()
        board = Board(8)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)

        board.new_moves = [[5,4,'b']]
        self.assertTrue(board.is_legal(board.new_moves))
        board.update_layout([[5,4,'b'],[4,4,'b']])

        board.new_moves = [[5,5,'w']]
        self.assertTrue(board.is_legal(board.new_moves))
        board.update_layout([[5,5,'w'],[4,4,'w']])

        turtle.clear()
        board = Board(8)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)

        board.update_layout([[3,4,'w']])
        board.new_moves = [[2,5,'b']]
        self.assertTrue(board.is_legal(board.new_moves))
        board.update_layout([[2,5,'b'],[3,4,'b']])

        board.update_layout([[4,5,'w']])
        board.new_moves = [[2,3,'w']]
        self.assertTrue(board.is_legal(board.new_moves))
        board.update_layout([[3,4,'w'],[0,1,'w']])

    def test_flip(self):
        turtle.clear()
        board = Board(8)
        board.generate_index()
        board.find_center()
        board.start_stones()
        board.update_layout(board.center_boxes)

        # A single flip, for example the first move of the game
        board.new_moves = [[2, 3, 'b']]
        board.is_legal(board.new_moves)
        to_flip = board.flip(board.new_moves, board.hitbox)
        expected = [[2, 3, 'b'],[3, 3, 'b']]
        self.assertEqual(to_flip, expected)
        board.hitbox = []

        # Manually setting up the board to create some situations of interest
        # Multiple flips
        board.update_layout([[2,2,'w'],[5,5,'w'],[6,6,'b']])
        board.new_moves = [[1, 1, 'b']]
        board.is_legal(board.new_moves)
        to_flip = board.flip(board.new_moves, board.hitbox)
        expected = [[1, 1, 'b'],[2,2,'b'],[3,3,'b'],[4,4,'b'],[5,5,'b']]
        self.assertEqual(to_flip, expected)
        board.hitbox = []

        # Stops at first friendly stone, no extra flips beyond
        board.update_layout([[2,3,'w'],[5,3,'w'],[6,3,'b']])
        board.new_moves = [[1, 3, 'b']]
        board.is_legal(board.new_moves)
        to_flip = board.flip(board.new_moves, board.hitbox)
        expected = [[1,3,'b'],[2,3,'b'],[3,3,'b']]
        self.assertEqual(to_flip, expected)
        board.hitbox = []

        # Two directions have flips
        board.update_layout([[2,3,'w'],[3,3,'w'],[4,3,'w'],[3,4,'b'],[4,4,'b']])
        board.new_moves = [[4, 5, 'w']]
        board.is_legal(board.new_moves)
        to_flip = board.flip(board.new_moves, board.hitbox)
        expected = [[4,5,'w'],[3,4,'w'],[4,5,'w'],[4,4,'w']]
        self.assertEqual(to_flip, expected)
        board.hitbox = []

        # Three directions have flips
        board.update_layout([[2,3,'w'],[3,3,'w'],[4,3,'w'],[5,3,'w'],[6,3,'w'],
                             [3,4,'b'],[4,4,'b'],[5,4,'b']])
        board.new_moves = [[4, 5, 'w']]
        board.is_legal(board.new_moves)
        to_flip = board.flip(board.new_moves, board.hitbox)
        expected = [[4,5,'w'],[3,4,'w'],[4,5,'w'],[4,4,'w'],[4,5,'w'],[5,4,'w']]
        self.assertEqual(to_flip, expected)
        board.hitbox = []
        
# TEST CLASS: Game -------------------------------------------------------------
class GameTest(unittest.TestCase):
    """
    Class to test all the methods from the Game class
    * __init__
    * __str__
    * clicked: the foundation of play_human
    * which_color
    * is_over
    * is_winner
    * update_scoreboard
    """
    def test_init(self):
        turtle.clear()
        game = Game(4)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 4)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

        game = Game(4.12345)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 4)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

        game = Game(4.54321)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 4)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

        game = Game(0)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 4)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

        game = Game(-8)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 4)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

        game = Game(8)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 8)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

        game = Game('four')
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 4)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

        game = Game('eight')
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.size, 4)
        self.assertEqual(game.turn, 2)
        self.assertEqual(game.scoreboard, [])

    def test_str(self):
        game = Game(4)
        expected = ''
        self.assertEqual(game.__str__(), expected)

        game.scoreboard = [['human', 2], ['computer', 2]]
        expected = 'human 2\ncomputer 2\n'
        self.assertEqual(game.__str__(), expected)

        game.scoreboard = [[2, 'human'], [2, 'computer']]
        expected = '2 human\n2 computer\n'
        self.assertEqual(game.__str__(), expected)

        game.scoreboard = [[10, 2], [20, 2]]
        expected = '10 2\n20 2\n'
        self.assertEqual(game.__str__(), expected)

    def test_which_color(self):
        game = Game(4)
        color = 'b'
        for i in range(2, 100, 2):
            game.turn = i
            self.assertEqual(game.which_color(), color)

        color = 'w'
        for i in range(3, 101, 2):
            game.turn = i
            self.assertEqual(game.which_color(), color)

        game.turn = 0
        self.assertEqual(game.which_color(), 'b')

        game.turn = -1
        self.assertEqual(game.which_color(), 'w')

        game.turn = 5.5
        self.assertEqual(game.which_color(), None)

        game.turn = 'bad'
        self.assertEqual(game.which_color(), None)

        game.turn = []
        self.assertEqual(game.which_color(), None)

    
    
    def test_clicked(self):
        # This method provides the foundation for the play_human method
        # Extensively tested to reinforce user-friendliness
        game = Game(4)
        game.prepare_game()
        turtle.onscreenclick(game.clicked(-49, 100))
        expected = [['x', 'b', 'x', 'x'],
                    ['x', 'b', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(-99.99, 51))
        expected = [['w', 'b', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(100.1, 100.1))
        expected = [['w', 'b', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(100.1, -100.1))
        expected = [['w', 'b', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(-100.1, 100.1))
        expected = [['w', 'b', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(-100.1, -100.1))
        expected = [['w', 'b', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(99.99, -99.99))
        expected = [['w', 'b', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)
        
        game = Game(4)
        game.prepare_game()
        turtle.onscreenclick(game.clicked(-100.01, 100.01))
        expected = [['x', 'x', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(100, 100))
        expected = [['x', 'x', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(-100, -100))
        expected = [['x', 'x', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(100, -100))
        expected = [['x', 'x', 'x', 'x'],
                    ['x', 'w', 'b', 'x'],
                    ['x', 'b', 'w', 'x'],
                    ['x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)


        game = Game(8)
        game.prepare_game()
        turtle.onscreenclick(game.clicked(-200, 200))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'w', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(199.99, 199.99))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'w', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(-199.99, -199.99))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'w', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        turtle.onscreenclick(game.clicked(199.99, -199.99))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'w', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(-49, 51))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Computer
        turtle.onscreenclick(game.clicked(-51, -49))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'w', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(75, -75))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'w', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'b', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Computer
        turtle.onscreenclick(game.clicked(75, 75))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'w', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'b', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(-1, -51))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'b', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'b', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Computer
        turtle.onscreenclick(game.clicked(51, -1))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'w', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'w', 'w', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'b', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(75, 25))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'w', 'w', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'b', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)  

        # Computer
        turtle.onscreenclick(game.clicked(75, -125))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'b', 'w', 'x', 'x'],
                    ['x', 'x', 'w', 'w', 'b', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(-125, -25))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'b', 'w', 'x', 'x'],
                    ['x', 'b', 'b', 'b', 'b', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Computer
        turtle.onscreenclick(game.clicked(-75, 75))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'w', 'b', 'w', 'x', 'x'],
                    ['x', 'b', 'b', 'b', 'w', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(125, 75))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'w', 'b', 'b', 'x', 'x'],
                    ['x', 'b', 'b', 'b', 'b', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Computer
        turtle.onscreenclick(game.clicked(125, 25))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'w', 'w', 'w', 'w', 'x'],
                    ['x', 'b', 'b', 'b', 'b', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(125, -75))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'w', 'b', 'w', 'w', 'x'],
                    ['x', 'b', 'b', 'b', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'x', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Computer
        turtle.onscreenclick(game.clicked(-75, -75))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'w', 'w', 'w', 'w', 'x'],
                    ['x', 'b', 'b', 'w', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(75, 125))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'b', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'b', 'b', 'x'],
                    ['x', 'x', 'x', 'w', 'w', 'b', 'w', 'x'],
                    ['x', 'b', 'b', 'w', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Computer
        turtle.onscreenclick(game.clicked(125, 125))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'b', 'w', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'w', 'x'],
                    ['x', 'x', 'x', 'w', 'w', 'b', 'w', 'x'],
                    ['x', 'b', 'b', 'w', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(175, 125))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'b', 'b', 'b'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'w', 'w', 'b', 'w', 'x'],
                    ['x', 'b', 'b', 'w', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)

        # Human
        turtle.onscreenclick(game.clicked(125, 175))
        expected = [['x', 'x', 'x', 'x', 'x', 'x', 'w', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'b', 'w', 'b'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'w', 'x'],
                    ['x', 'x', 'x', 'w', 'w', 'b', 'w', 'x'],
                    ['x', 'b', 'b', 'w', 'b', 'b', 'x', 'x'],
                    ['x', 'x', 'w', 'b', 'x', 'w', 'b', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'w', 'x', 'x'],
                    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
        self.assertEqual(game.board.board_stones, expected)
        
        turtle.clear()
        
    def test_is_over(self):
        # start of game
        game = Game(4)
        game.prepare_game()
        turn_decision = game.is_over()
        for player in turn_decision:
            self.assertFalse(turn_decision[player])

        # board full of black stones
        for i in range(len(game.board.board_stones)):
            for j in range(len(game.board.board_stones[i])):
                game.board.board_stones[i][j] = 'b'
        turn_decision = game.is_over()
        for player in turn_decision:
            self.assertTrue(turn_decision[player])

        # board full of white stones
        for i in range(len(game.board.board_stones)):
            for j in range(len(game.board.board_stones[i])):
                game.board.board_stones[i][j] = 'w'
        turn_decision = game.is_over()
        for player in turn_decision:
            self.assertTrue(turn_decision[player])

        # board near full, white has no legal but black does
        game.board.new_moves = [[1, 0, 'b'],[1, 3, 'b'],[3, 3, 'x']]
        game.board.update_layout(game.board.new_moves)
        turn_decision = game.is_over()
        self.assertFalse(turn_decision[0])
        self.assertTrue(turn_decision[1])

        # board near full, black has no legal but white does
        game.board.new_moves = [[2, 3, 'b']]
        game.board.update_layout(game.board.new_moves)
        turn_decision = game.is_over()
        self.assertTrue(turn_decision[0])
        self.assertFalse(turn_decision[1])
        
    def test_is_winner(self):
        print("\n")
        game = Game(4)
        game.prepare_game()
        game.update_scoreboard()
        winner = ['human', 'computer']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 4
        game.players[1].score = 3
        winner = ['human']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 3
        game.players[1].score = 4
        winner = ['computer']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = -4
        game.players[1].score = 3
        winner = ['computer']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 4.5
        game.players[1].score = 4.5
        winner = ['human', 'computer']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 8
        game.players[1].score = 8
        winner = ['human', 'computer']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 'five'
        game.players[1].score = 'four'
        winner = ['computer']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 32
        game.players[1].score = 32
        winner = ['human', 'computer']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 64
        game.players[1].score = 0
        winner = ['human']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 27
        game.players[1].score = 26
        winner = ['human']
        self.assertEqual(game.is_winner(), winner)

        game.players[0].score = 8.1
        game.players[1].score = 8.0
        winner = ['human']
        self.assertEqual(game.is_winner(), winner)
        
    def test_update_scoreboard(self):
        # hard coded moves for each player, check if the score is accurate
        turtle.clear()
        game = Game(8)
        game.prepare_game()
        scores = [['human', 2], ['computer', 2]]
        game.update_scoreboard()
        self.assertEqual(game.scoreboard, scores)

        game.board.new_moves =[[2, 3, 'b']]
        game.board.is_legal(game.board.new_moves)
        game.board.update_layout(game.board.new_moves)
        game.board.update_layout(game.board.flip(game.board.new_moves,
                                                 game.board.hitbox))
        game.update_scoreboard()
        scores = [['human', 4], ['computer', 1]]
        self.assertEqual(game.scoreboard, scores)
        game.is_over()

        game.board.new_moves =[[2, 2, 'w']]
        game.board.is_legal(game.board.new_moves)
        game.board.update_layout(game.board.new_moves)
        game.board.update_layout(game.board.flip(game.board.new_moves,
                                                 game.board.hitbox))
        game.update_scoreboard()
        scores = [['human', 3], ['computer', 3]]
        self.assertEqual(game.scoreboard, scores)
        game.is_over()

        game.board.new_moves =[[4, 5, 'b']]
        game.board.is_legal(game.board.new_moves)
        game.board.update_layout(game.board.new_moves)
        game.board.update_layout(game.board.flip(game.board.new_moves,
                                                 game.board.hitbox))
        game.update_scoreboard()
        scores = [['human', 5], ['computer', 2]]
        self.assertEqual(game.scoreboard, scores)
        game.is_over()

        game.board.new_moves =[[3, 5, 'w']]
        game.board.is_legal(game.board.new_moves)
        game.board.update_layout(game.board.new_moves)
        game.board.update_layout(game.board.flip(game.board.new_moves,
                                                 game.board.hitbox))
        game.update_scoreboard()
        scores = [['human', 4], ['computer', 4]]
        self.assertEqual(game.scoreboard, scores)
        game.is_over()
        # Close turtle after test suite is done
        turtle.bye()

# TEST FILE PROCESSING FUNCTIONS -----------------------------------------------
class FunctionTest(unittest.TestCase):
    def test_verify_existence(self):
        self.assertFalse(verify_existence('fakefile.txt'))
        self.assertTrue(verify_existence('scores_test1.txt'))

    def test_read_score(self):
        expected = []
        self.assertEqual(read_score('fakefile'), expected)
        
        expected = ['velma 64', 'scooby 32', 'shaggy 0']
        self.assertEqual(read_score('scores_test1.txt'), expected)

    def test_append_score(self):
        append_score('scores_test2.txt', 'anotherguy', 5)
        expected = ['anotherguy 5']
        self.assertEqual(read_score('scores_test2.txt'), expected)

        append_score('scores_test2.txt', 'sam', 4)
        expected = ['anotherguy 5', 'sam 4']
        self.assertEqual(read_score('scores_test2.txt'), expected)

        append_score('scores_test2.txt', 'bob', 5)
        expected = ['anotherguy 5', 'sam 4', 'bob 5']
        self.assertEqual(read_score('scores_test2.txt'), expected)

        # Clear out the file successive test can be run without errors
        outfile = open('scores_test2.txt', 'w')
        outfile.write('')
        outfile.close()

    def test_insert_score(self):
        insert_score('scores_test3.txt', 'start', 4, [])
        expected = ['start 4']
        self.assertEqual(read_score('scores_test3.txt'), expected)

        insert_score('scores_test3.txt', 'new', 5, ['start 4'])
        expected = ['new 5','start 4']
        self.assertEqual(read_score('scores_test3.txt'), expected)

        insert_score('scores_test3.txt', 'best', 64, ['new 5','start 4'])
        expected = ['best 64', 'new 5','start 4']
        self.assertEqual(read_score('scores_test3.txt'), expected)

    def test_compare(self):
        expected = 64
        comparison = compare(read_score('scores_test3.txt'))
        self.assertEqual(comparison, expected)

        append_score('scores_test3.txt', 'big', 128)
        expected = 128
        comparison = compare(read_score('scores_test3.txt'))
        self.assertEqual(comparison, expected)



def main():
    unittest.main(verbosity = 3)

main()

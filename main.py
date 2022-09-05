import cmd
import os
from termcolor import colored
import math
import time
import random
import json

# checking the width of console
width = os.get_terminal_size().columns

class Player:
    def __init__(self, sign, move):
        self.sign = sign
        self.move = move

def save_game(game, winner):
    # checking if storage.json already exists
    if (os.path.isfile("storage.json")):
        file_object = open("storage.json", "r")
        data = json.load(file_object)
        output_file = open("storage.json", "w")
        game_data = {
            'game': game,
            'winner': winner
        }
        data.append(game_data)
        json.dump(data, output_file, indent=2)
    else:
        output_file = open("storage.json", "w")
        game_data = {
            'game': game,
            'winner': winner
        }
        json.dump([game_data], output_file, indent=2)

# printing the game
def print_game(game):
    vb = colored("|", 'yellow')
    print(colored("=============", 'yellow'))
    i = 1
    for row in game:
        print(vb, row[0], vb, row[1], vb, row[2], vb, "    ", vb, i, vb, i + 1, vb, i + 2, vb)
        i += 3
        print(colored("=============", 'yellow'))

class TicTacToe(cmd.Cmd):
    # intro prompt
    str = "Tic-Tac-Toe"
    prompt = ">> "
    intro = colored(str.center(width), 'blue')
    
    game_snapshot = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    
    # loading the previous saved games
    def do_load(self, arg):
        if (os.path.isfile("storage.json")):
            data = json.load(open("storage.json", "r"))
            for elements in data:
                print(elements)
                print_game(elements['game'])
                print("Match result:", elements['winner'])
        else:
            print(colored("No data exists till now...", 'red'))

    def do_new(self, arg):
        self.game_snapshot = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        print("")
        # randomly assigning first move and sign
        player1 = Player('X' if random.randint(0, 1) == 0 else 'O', random.randint(0, 1))
        player2 = Player('X' if player1.sign == 'O' else 'O', 1 if player1.sign == 0 else 0)
        print("Your Sign:", player1.sign)
        print(colored("You got first turn!!!", 'green') if player1.move == 0 else colored("Computer has first turn!!!", 'blue'))
        move = 0
        run = True
        while run:
            # checking who has the move
            if (move == player1.move):
                x = input("Enter your input: ")
                if x == 'q':
                    run = False
                elif (x.isdigit()):
                    if int(x) < 10 and (self.game_snapshot[math.floor(int(x) / 3.1)][(int(x) % 3) - 1] == ' '):
                        self.game_snapshot[math.floor(int(x) / 3.1)][(int(x) % 3) - 1] = player1.sign
                    else:
                        if (move == 1):
                            move = 0
                        else:
                            move = 1
                        print(colored("Wrong Input", 'red'))
                else:
                    if (move == 1):
                        move = 0
                    else:
                        move = 1
                    print(colored("Wrong Input", 'red'))
            else:
                print("Computer taking decision...")
                time.sleep(2)
                bot_move = bot_play(self.game_snapshot, player2.sign, player1.sign)
                self.game_snapshot[bot_move[0]][bot_move[1]] = player2.sign
            print_game(self.game_snapshot)
            result = win_move(self.game_snapshot)
            # checking and saving game results
            if (result == 'd'):
                print(colored('Draw Match!!!', 'yellow'))
                save_game(self.game_snapshot, 'draw')
                run = False
            if (result != ''):
                if (result == player1.sign):
                    print(colored('You Won!!!', 'green'))
                    save_game(self.game_snapshot, 'player won')
                    run = False
                elif (result == player2.sign):
                    print(colored('Computer Won!!!', 'red'))
                    save_game(self.game_snapshot, 'bot won')
                    run = False
            # toggling moves
            if (move == 1):
                move = 0
            else:
                move = 1
    
    # to quit
    def do_quit(self, arg):
        print(colored('Good Bye!!!', 'yellow'))
        raise SystemExit

# creating the bot
def bot_play(game, bot, human):
    bestScore = -1000
    bestMove = []
    for rows in range(0, 3):
        for blocks in range(0, 3):
            if (game[rows][blocks] == ' '):
                game[rows][blocks] = bot
                score = minimax(game, 0, False, bot, human)
                if (score > bestScore):
                    bestScore = score
                    bestMove = [rows, blocks]
                game[rows][blocks] = ' '
    return bestMove

# checking if someone wins or loses or draws
def win_move(game):
    win = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    result = ' '
    for cases in win:
        char = game[int(cases[0] / 3)][cases[0] % 3] + game[int(cases[1] / 3)][cases[1] % 3] + game[int(cases[2] / 3)][cases[2] % 3]
        if ('XXX' == char):
            result = 'X'
        elif ('OOO' == char):
            result = 'O'
        char = ''
    if (char != ''):
        draw = True
        for row in range(0, 3):
            for block in range(0, 3):
                if (game[row][block] == ' '):
                    draw = draw and False
        if (draw):
            return 'd'
    return result

# minimax recursive function
def minimax(game, depth, isMaximizing, bot, human):
    # checking if someone wins
    won = win_move(game)
    if (won != ''):
        if (won == bot):
            return 10
        elif (won == 'd'):
            return 0
        elif (won == human):
            return -10
    # this bot opposes human
    if (isMaximizing):
        bestScore = -math.inf
        for rows in range(0, 3):
            for blocks in range(0, 3):
                if (game[rows][blocks] == ' '):
                    game[rows][blocks] = bot
                    score = minimax(game, depth + 1, False, bot, human)
                    if (score > bestScore):
                        bestScore = score
                        bestMove = [rows, blocks]
                    game[rows][blocks] = ' '
        return bestScore
    # this bot tries to oppose the previous bot and assumes the human will take the best move
    else:
        bestScore = math.inf
        for rows in range(0, 3):
            for blocks in range(0, 3):
                if (game[rows][blocks] == ' '):
                    game[rows][blocks] = human
                    score = minimax(game, depth + 1, True, bot, human)
                    if (score < bestScore):
                        bestScore = score
                        bestMove = [rows, blocks]
                    game[rows][blocks] = ' '
        return bestScore

# main function
if __name__ == '__main__':
    TicTacToe().cmdloop()
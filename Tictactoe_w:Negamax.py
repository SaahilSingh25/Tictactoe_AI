#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 10:05:20 2020

@author: Saahil
"""
import sys

ai_char = ""
user_char = ""
     
def nega_is_game_over(board, char): #Checks if the game is over respective to the current player
    for x in range(3):
        if board[(x*3)] == board[(x*3)+1] == board[(x*3)+2] and board[x*3] != ".":
            if board[(x*3)+1] == char:
                return (True, 1)
            else:
                return (True, -1)
    for x in range(3):
        if board[x] == board[x+3] == board[x+6] and board[x] != ".":
            if board[x] == char:
                return (True, 1)
            else:
                return (True, -1)
    if board[0] == board[4] == board[8] and board[0] != ".":
        if board[0] == char:
            return (True, 1)
        else:
            return (True, -1)
    elif board[2] == board[4] == board[6] and board[2] != ".":
        if board[2] == char:
            return (True, 1)
        else:
            return (True, -1)
    elif board.count(".") == 0:
        return (True, 0)
    return (False, -1)
            
def negamax(board, cur_play): #Negamax function
    score = nega_is_game_over(board, cur_play)
    if score[0] == True:
        return score[1]
    results = []
    if cur_play == "X": #This if-else is used to determine the opponent symbol
        other_play = "O"
    else:
        other_play = "X"
    for next_board in possible_next_boards(board, cur_play)[0]:
        results.append(-1 * negamax(next_board, other_play)) #Determine the inverse of the result of the other symbol
    return max(results)   

def nega_move(board, cur_play):
    results = []
    boards = []
    changes = []
    temp = possible_next_boards(board, cur_play)
    if cur_play == "X":
        other_play = "O"
    else:
        other_play = "X"
    print()
    for x in range(len(temp[1])):
        changed = temp[1][x]
        board = temp[0][x]
        res = -1*negamax(board, other_play)
        results.append(res)
        boards.append(board)
        changes.append(changed)
        if results[x] == 1:
            s = "win"
        elif results[x] == -1:
            s = "loss"
        else:
            s = "tie"
        print("Moving at " + str(changed) + " results in a " + s)
    temp = results.index(max(results))
    print()
    print("I choose space " + str(changes[temp]) + "\n")
    return boards[temp]

def possible_next_boards(board, current_player):
    start = board
    possible_boards = []
    changed = []
    for x in range(9):
        if board[x] == ".":
            board = list(board)
            board[x] = current_player
            possible_boards.append("".join(board))
            changed.append(x)
            board = start
    return (possible_boards,changed)

def who_plays(board):
    board = list(board)
    comp = ""
    if (board.count("X") + board.count("O")) % 2 == 0:
        comp = "X"
    else:
        comp = "O"
    return comp

def display_board(board):
    count = 0
    char = 0
    ind = 0
    s = ""
    for x in range(21):
        if count == 7:
            count = 0
            s+= "\n"
        if count < 3:
            s+= board[char]
            char += 1
        elif count == 3:
            s+= "     "
        elif count > 3:
            s+= str(ind)
            ind+= 1
        count+=1
    print(s)

def empty_spaces(board):
    s = ""
    for x in range(9):
        if board[x] == ".":
            s += str(x) + ", "
    s = s[:-2]
    return s
    
board = sys.argv[1]
score = nega_is_game_over(board, "X")
if score[0] == True:
    if score[1] == "X":
        print("X has already won!")
    elif score[1] == "O":
        print("O has already won!")
    else:
        print("The game is a tie!")
elif list(board).count(".") == 9:
    ai_char = input("Should I be X or O? ")
    if ai_char == "X":
        user_char = "O"
    else:
        user_char = "X"
    print()
    print("Current board:")
    display_board(board)
    while nega_is_game_over(board, "X")[0] == False:
        if ai_char == "X":
            board = nega_move(board, "X")
            print("Current board:")
            display_board(board)
            print()
            temp = nega_is_game_over(board, "X")
            if temp[0] == False:
                print("You can move to any of these spaces " + empty_spaces(board))
                choice = input("Your choice? ")
                print()
                board = list(board)
                board[int(choice)] = "O"
                board = "".join(board)   
                print("Current board:")
                display_board(board)
        elif ai_char == "O":
            print()
            print("You can move to any of these spaces " + empty_spaces(board))
            choice = input("Your choice? ")
            print()
            board = list(board)
            board[int(choice)] = "X"
            board = "".join(board)   
            print("Current board:")
            display_board(board)                    
            temp = nega_is_game_over(board, "X")
            if temp[0] == False:
                board = nega_move(board, "O")
                print("Current board:")
                display_board(board)
                print()
    temp = nega_is_game_over(board, "X")
    char = ""
    if temp[1] == 1:
        char = "X"
    elif temp[1] == -1:
        char = "O"
    else:
        print("We tied!")
    if char == ai_char:
        print("I win!")
    elif char == user_char:
        print("You win!")
else:
    ai_char = who_plays(board)
    if ai_char == "X":
        user_char = "O"
    else:
        user_char = "X"
    print("Current board:")
    display_board(board)
    while nega_is_game_over(board, "X")[0] == False:
        if ai_char == "X":
            board = nega_move(board, "X")
        else:
            board = nega_move(board, "O")
        print("Current board:")
        display_board(board)
        print()
        temp = nega_is_game_over(board, "X")
        if temp[0] == False:
            print("You can move to any of these spaces " + empty_spaces(board))
            choice = input("Your choice? ")
            print()
            board = list(board)
            board[int(choice)] = user_char
            board = "".join(board)  
            print("Current board:")
            display_board(board)    
    print()
    temp = nega_is_game_over(board, "X")
    char = ""
    if temp[1] == 1:
        char = "X"
    elif temp[1] == -1:
        char = "O"
    else:
        print("We tied!")
    if char == ai_char:
        print("I win!")
    elif char == user_char:
        print("You win!")

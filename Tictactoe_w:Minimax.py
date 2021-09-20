#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 10:05:20 2020

@author: Saahil
"""
import sys

ai_char = ""
user_char = ""

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
            
def is_game_over(board):
    for x in range(3):
        if board[(x*3)] == board[(x*3)+1] == board[(x*3)+2] and board[x*3] != ".":
            if board[(x*3)+1] == "X":
                return (True, 1)
            else:
                return (True, -1)
    for x in range(3):
        if board[x] == board[x+3] == board[x+6] and board[x] != ".":
            if board[x] == "X":
                return (True, 1)
            else:
                return (True, -1)
    if board[0] == board[4] == board[8] and board[0] != ".":
        if board[0] == "X":
            return (True, 1)
        else:
            return (True, -1)
    elif board[2] == board[4] == board[6] and board[2] != ".":
        if board[2] == "X":
            return (True, 1)
        else:
            return (True, -1)
    elif board.count(".") == 0:
        return (True, 0)
    return (False, -1)
            
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

def max_step(board):
    if ai_char == "X":
        current_player = ai_char
    else:
        current_player = user_char
    score = is_game_over(board)
    if score[0] == True:
        return score[1]
    results = []
    for next_board in possible_next_boards(board, current_player)[0]:
        results.append(min_step(next_board))
    return max(results)

def min_step(board):
    if ai_char == "O":
        current_player = ai_char
    else:
        current_player = user_char
    score = is_game_over(board)
    if score[0] == True:
        return score[1]
    results = []
    for next_board in possible_next_boards(board, current_player)[0]:
        results.append(max_step(next_board))
    return min(results)

def max_move(board):
    results = []
    boards = []
    changes = []
    temp = possible_next_boards(board, "X")
    print()
    for x in range(len(temp[1])):
        changed = temp[1][x]
        board = temp[0][x]
        res = min_step(board)
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

def min_move(board):
    results = []
    boards = []
    changes = []
    temp = possible_next_boards(board, "O")
    print()
    for x in range(len(temp[1])):
        changed = temp[1][x]
        board = temp[0][x]
        res = max_step(board)
        results.append(res)
        boards.append(board)
        changes.append(changed)
        if results[x] == 1:
            s = "loss"
        elif results[x] == -1:
            s = "win"
        else:
            s = "tie"
        print("Moving at " + str(changed) + " results in a " + s)
    temp = results.index(min(results))
    print()
    print("I choose space " + str(changes[temp]) + "\n")
    return boards[temp]

def empty_spaces(board):
    s = ""
    for x in range(9):
        if board[x] == ".":
            s += str(x) + ", "
    s = s[:-2]
    return s
    
board = sys.argv[1]
score = is_game_over(board)
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
    while is_game_over(board)[0] == False:
        if ai_char == "X":
            board = max_move(board)
            print("Current board:")
            display_board(board)
            print()
            temp = is_game_over(board)
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
            temp = is_game_over(board)
            if temp[0] == False:
                board = min_move(board)
                print("Current board:")
                display_board(board)
                print()
                temp = is_game_over(board)
    temp = is_game_over(board)
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
    while is_game_over(board)[0] == False:
        if ai_char == "X":
            board = max_move(board)
        else:
            board = min_move(board)
        print("Current board:")
        display_board(board)
        print()
        temp = is_game_over(board)
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
    temp = is_game_over(board)
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

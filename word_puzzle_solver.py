# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 23:51:08 2023

@author: Feyza
"""
my_name = "Ayse Feyza Birer"
my_id = "220102002033"
my_email = "a.birer2022@gtu.edu.tr"



words = [] 
board = []
def read_file(filename = "test_puzzle.txt"):
    a = []
    string = ''
    with open(filename, 'r',) as dosya:
        letters = dosya.read()

    for letter in letters:
        a.append(letter.strip())
   
    for element in a:
        if element != '':
            string += element
        else:
            if string != '':
                try:
                    int_value = int(string)
                    board.append(string)
                except ValueError:
                    words.append(string)
                string = ''                          
        
    if string != '':
        try:
            int_value = int(string)
            board.append(string)
        except ValueError:
            words.append(string)
        
    return words, board

def check_consistency(board):
    for i in range(1, len(board)):
        if len(board[i]) != len(board[0]):
            return False
    return True
    
def create_board(board):
    for i in range(len(board)):
       board[i] = list(board[i])
    return None
   
def identifier(words):
    my_list = []
    for i in range(len(words)):
       my_list.append(False) 
    return my_list

def print_board(board):
   for row in board:
       row_str = ""
       for i in row: 
           if i == '0':
               row_str += " + "
           elif i == '1':
               row_str += " "        
       
       print(row_str)
   return None

def print_board_w_c(board):
    row_number = 1
    print("  ", end="")
    for i in range(1,(len(board[0])+1)):
        print("C" + str(i), end="  ")
    print()
        
    for row in board:
        row_str = ""
        for i, value in enumerate(row):
            if i == 0: 
                if value == '0':
                    row_str += " +"
                elif value == '1':
                    row_str += "  "
            else:
                if value == '0':
                    row_str += "   +"
                elif value == '1':
                    row_str += "    "
        print("R" + str(row_number), end="")
        print(row_str)
        row_number += 1  
    return None
        
def print_wordlist(words, wstatus):
    longest_word = max(words, key=len)
    longest_word_length = len(longest_word)
    if longest_word_length > 12:
        spaces = longest_word_length
        print(f"Word List{longest_word_length * ' '}Status")
    else:
        spaces = 12
        print("Word List" + str(spaces * " ") + "Status")

    for i in range(len(words)):
        word = words[i]
        if wstatus[i]:
            status = "USED"
        else:
            status = "NOT USED"
        spaces_2 = " " * (spaces + 9 - len(word) - 3)
        print(f"W{i+1} {word}{spaces_2}{status}")
    
def check_entries(coordinates, wordno, board, words):

    if 0 < wordno <= len(words):
        a = True 
    else: 
        a = False 
    
    if 0 < coordinates[0] <= len(board) and 0 < coordinates[1] <= len(board[0]):
        b = True 
    else: 
        b = False
        
    return  b, a

def check_location(board, words, coordinates, wordno, direction='H'):
    conditions = []

    if board[coordinates[0] - 1][coordinates[1] - 1] == "0":
        conditions.append(False)  # Check if starting cell is a forbidden cell

    if direction == "V" and coordinates[0] - 2 >= 0 and board[coordinates[0] - 2][coordinates[1] - 1] == "1":
        conditions.append(False)  # Check if direction is vertical and upper cell is a forbidden cell

    if direction == "H" and coordinates[1] - 2 >= 0 and board[coordinates[0] - 1][coordinates[1] - 2] == "1":
        conditions.append(False)  # Check if direction is horizontal and left cell is a forbidden cell

    if direction == "H" and len(words[wordno - 1]) > len(board[0]) - coordinates[1] + 1:
        conditions.append(False)  # Check if direction is horizontal and the word exceeds the board

    if direction == "V" and len(words[wordno - 1]) > len(board) - coordinates[0] + 1:
        conditions.append(False)  # Check if direction is vertical and the word exceeds the board

    if direction == "H" and coordinates[1] + len(words[wordno - 1]) - 1 < len(board[0]) and \
            board[coordinates[0] - 1][coordinates[1] + len(words[wordno - 1]) - 1] == "1":
        conditions.append(False)  # Check if direction is horizontal and the next cell (if any) of the words last cell in given direction is a not a forbidden cell

    if direction == "V" and coordinates[0] + len(words[wordno - 1]) - 1 < len(board) and \
            board[coordinates[0] + len(words[wordno - 1]) - 1][coordinates[1] - 1] == "1":
        conditions.append(False)  # Check if direction is vertical and the next cell (if any) of the words last cell in given direction is a not a forbidden cell

    if False in conditions:
        return False, conditions.count(False)
    else: 
        return True, 0
    
    
def check_word_fits(board,words,coordinates,wordno,direction='H'):
    conditions = []
    if direction == "H":
        chosen_row = board[coordinates[0]-1][(coordinates[1]-1):(coordinates[1]+len(words[wordno-1])-1)]
        for i, (value1, value2) in enumerate(zip(words[wordno-1],chosen_row)):
            if (chosen_row[i] != "1" and chosen_row[i] != "0" and words[wordno-1][i] != chosen_row[i]) or chosen_row[i] == "0":
                conditions.append(False)
                conditions.append("1")
    if direction == "V":
        chosen_column = []
        for row in board[coordinates[0]-1:coordinates[0]-1+len(words[wordno-1])]:
            chosen_column.append(row[coordinates[1]-1])
           
        for i, (value1, value2) in enumerate(zip(words[wordno-1],chosen_column)):
            if (chosen_column[i] == "1"  and chosen_column[i] == "0" and words[wordno-1][i] != chosen_column[i]) or chosen_column[i] == "0":
                conditions.append(False)
                conditions.append("2")
               
    if False in conditions:
        if "1" in conditions:
             return False, 1 
        else: 
             return False, 2 
    else:
         return True, 0

def clear_board(board,wstatus) :
    for row_index, row in enumerate(board):
        for column_index, element in enumerate(row):
            if element != "0":
                board[row_index][column_index] = "1"
            
    for i in range(len(wstatus)):
        if wstatus[i] != False:
            wstatus[i] = False

def decompose_command(str1):
    if ("w" in str1 or "W" in str1) and ("r" in str1 or "R" in str1) and ("c" in str1 or "C" in str1) \
        and ("d" in str1 or "D" in str1):
            output1 = 0
    else: 
       return (-1, None, None, None)
        
    if output1 == 0:
        
        output2 = []

        for i, value in enumerate(str1):
            if (value == "w" or value == "W") and (i+2 < len(str1)) and str1[i+1].isdigit() and str1[i+2].isdigit() :
                output2.append(int(str1[i+1] + str1[i+2]))
            elif (value == "w" or value == "W") and str1[i+1].isdigit():
                output2.append(int(str1[i+1]))

        output2 = output2[0]

        row_no = []
        for i, value in enumerate(str1):
            if (value == "R" or value == "r") and (i+2 < len(str1)) and str1[i+1].isdigit() and str1[i+2].isdigit():
                row_no.append(int(str1[i+1] + str1[i+2]))
            elif (value == "R" or value == "r") and str1[i+1].isdigit():
                row_no.append(int(str1[i+1]))

        row_no = row_no[0]

        column_no = []
        for i, value in enumerate(str1):
            if (value == "C" or value == "c") and (i+2 < len(str1)) and str1[i+1].isdigit() and str1[i+2].isdigit():
                column_no.append(int(str1[i+1] + str1[i+2]))
            elif (value == "C" or value == "c") and str1[i+1].isdigit():
                column_no.append(int(str1[i+1]))

        column_no = column_no[0]

        output3 = [row_no, column_no]

        direction = []
        for i, value in enumerate(str1):
            if (value == "d" or value == "D") and (str1[i+1] != "V" and str1[i+1] != "H" and str1[i+1] != "h" and str1[i+1] != "v" ):
                direction.append("H")
            if (value == "d" or value == "D") and (str1[i+1] == "V" or str1[i+1] == "v"):
                direction.append("V")
            if (value == "d" or value == "D") and (str1[i+1] == "H" or str1[i+1] == "h"):        
                direction.append("H") 

        output4 = direction[0]
        return (output1, output2, output3, output4)
    
    

     
def word_it(board,words,wstatus,coordinates,wordno,direction): 
    a = check_entries(coordinates,wordno,board,words)
    b = check_location(board,words,coordinates,wordno,direction='H')
    c = check_word_fits(board,words,coordinates,wordno,direction='H')
    
    if a == (True, True) and b == (True, 0) and c == (True, 0):
        return True

    if direction == "V":
        for i, letter in enumerate(words[wordno-1]):
            board[coordinates[0]-1 + i][coordinates[1]-1] = letter
    
    if direction == "H":
        for i, letter in enumerate(words[wordno-1]):
            board[coordinates[0]-1][coordinates[1]-1 + i] = letter
            
    wstatus[wordno-1] = True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
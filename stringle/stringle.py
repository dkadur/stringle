from random import randint
from tkinter import *
from tkinter import ttk
import os, sys

def onAlphabetPress(event):
    global char_indicator, row_indicator, char_count, row_count, guess, freeze_status
    if char_indicator < char_count and not freeze_status:
        labels[row_indicator][char_indicator]['text'] = event.char
        guess += event.char
        char_indicator += 1

def onEnterPress(event):
    global char_indicator, row_indicator, char_count, row_count, new_word, root, freeze_status
    if char_indicator == char_count and row_indicator == row_count-1 and not freeze_status:
        if colorRow() == char_count:
            printWin()
        else:
            printLose()
        freeze_status = YES
        Button(mainframe, text ="Play Again", command = buttonPressed).grid(row=row_count+2, column=0, columnspan=char_count)
    elif char_indicator == char_count and row_indicator < row_count and not freeze_status:
        if colorRow() == char_count:
            printWin()
            freeze_status = YES
            Button(mainframe, text ="Play Again", command = buttonPressed).grid(row=row_count+2, column=0, columnspan=char_count)
        row_indicator += 1
        char_indicator = 0

def onDeletePress(event):
    global char_indicator, guess, freeze_status
    if char_indicator > 0 and not freeze_status:
        char_indicator -= 1
        labels[row_indicator][char_indicator]['text'] = "  "
        guess = guess[:-1]


def colorRow():
    global char_count, guess, labels, new_word, row_indicator
    temp_new_word = new_word
    green_count = 0

    for count, guess_char in enumerate(guess):
        if guess_char == temp_new_word[count]:
            labels[row_indicator][count]['bg'] = 'green'
            temp_new_word = temp_new_word[:count] + '_' + temp_new_word[count+1:]
            guess = guess[:count] + '/' + guess[count+1:]
            green_count += 1
    
    for count, guess_char in enumerate(guess):
        if guess_char != temp_new_word[count] and guess_char in temp_new_word:
            labels[row_indicator][count]['bg'] = '#EDDF24'
            index = temp_new_word.index(guess_char)
            temp_new_word = temp_new_word[:index] + '_' + temp_new_word[index+1:]

    guess = ''
    return green_count

def printWin():
    global new_word, char_count, row_count
    Label(mainframe, text=f"You guessed the word: '{new_word}'", fg='#e0dfd5', font=('Times 20'), width=2).grid(row=row_count+1, columnspan=char_count, sticky=EW)

def printLose():
    global new_word, char_count, row_count
    Label(mainframe, text=f"You did not guess the word: '{new_word}'", fg='#e0dfd5', font=('Times 20'), width=2).grid(row=row_count+1, columnspan=char_count, sticky=EW)

def buttonPressed():
    os.execv(sys.executable, ['python'] + sys.argv)

char_indicator = 0
row_indicator = 0
char_count = 5
row_count = 6
freeze_status = NO

with open(os.path.join(sys.path[0], "words.txt"), "r") as f:
    words = f.readlines()
num_lines = sum(1 for word in words)
rand_index = randint(0, num_lines-1)
new_word = words[rand_index][0:char_count]

letters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l',
'z','x','c','v','b','n','m']
labels = []
guess = ''

root = Tk()
root.title("Stringle")

mainframe = ttk.Frame(root, padding="120 120 120 120")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

for x in range(row_count):
    for y in range(char_count):
        labels.append([])
        label = Label(mainframe, bg='gray', text="", fg='black', font=('Times 50'), width=2)
        labels[x].append(label)
        label.grid(column=y, row=x)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=2, pady=2)

for letter in letters:
    root.bind(letter, onAlphabetPress)

root.bind('<Return>', onEnterPress)
root.bind('<BackSpace>', onDeletePress)

'''Uncomment the line below to reveal word before guessing. Recomment to conceal word during guessing'''
#print(new_word)

root.mainloop()
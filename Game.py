#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

# imports all the libraries of tkinter.

from collections import OrderedDict

# imports OrderedDict from Collections.

import random

# imports random.

fps = 20

# defines the frame rate per second.

points = -1

# sets points to -1 so that score is set to 0 when the game starts.

w = None
unwanted_widgets = []

# makes a list in which widgets are added which can be removed later.

hpoints = {}

# creates a dictionary of leaderboard.

pt = None
cheats = {'feed me score': False, 'pipes are useless': False}

# dictionary of cheatcodes

data = open('key.txt', 'r').readlines()
UP_KEY = str(data[0]).replace('\n', '')


# opens the txt file that defines the commands to move the bird.

def boss_key():
    global bimg, NOW_PAUSE
    NOW_PAUSE = True
    tp = Toplevel()
    bimg = PhotoImage('bossimg.png')
    lb = Label(tp, image=bimg)
    lb.pack()

    # tp.attributes('-fullscreen',True)

    tp.mainloop()


# defines the bosskey and uses the png image of the excel sheet.

def check_key(event):

    def apply_or_remove():
        global cheats
        code = e.get()

        if str(code) in list(cheats.keys()):
            if cheats[code] == True:
                cheats[code] = False
            else:
                cheats[code] = True

            tp.destroy()

    if event.char == 'c':
        tp = Toplevel()
        lb = Label(tp, text='Enter here : ')
        lb.pack()

        e = Entry(tp)
        e.pack()

        b = Button(tp, text='Apply / Remove', command=apply_or_remove)
        b.pack()

        tp.mainloop()

    if event.char == 'b':
        boss_key()


# Defines a function which takes input of a char key as an input and depending on the input activates either the bosskey or the cheatcode key.

def pause_game(event=None):
    global NOW_PAUSE, w, pt
    if NOW_PAUSE == False:
        NOW_PAUSE = True
        pt = w.create_text(
            15,
            45,
            text='PAUSED',
            font='Impact 60',
            fill='#ffffff',
            anchor=W,
            )
        return 0
    elif NOW_PAUSE == True:
        NOW_PAUSE = False
        w.delete(pt)
        birdDown()
        pipesMotion()
        detectCollision()
        return 0


# defines the pause functionality in which if pause is pressed game either pauses or resumes depending on the previous state.

def load_score():
    global hpoints
    hpoints.clear()
    names = []
    scores = []
    f = open('Hscore.txt', 'r')
    data = f.readlines()

    # data = data[:5]

    f.close()
    for i in data:
        cp = i.find(',')
        name = i[:cp]
        score = i[cp + 1:].replace('\n', '')
        names.append(name)
        scores.append(int(score))

    # updates the scores and names by iterating and differentiating the two.

    for j in range(len(scores) - 1):

        # sorting of scores is performed

        for i in range(len(scores) - 1):
            if scores[i] < scores[i + 1]:
                (scores[i], scores[i + 1]) = (scores[i + 1], scores[i])
                (names[i], names[i + 1]) = (names[i + 1], names[i])

    for i in range(len(scores)):
        hpoints.update({names[i]: scores[i]})

    for i in hpoints.keys():
        print (i, hpoints[i])


load_score()


def create_canvas():
    global w
    w = Canvas(
        main,
        width=550,
        height=700,
        background='#4EC0CA',
        bd=0,
        highlightthickness=0,
        )
    w.pack()


# creates the canvas where the actual game is played

def center(toplevel):

    # places the game in the centre in accordance to the screen

    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+'
                 )[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2 - 35
    toplevel.geometry('%dx%d+%d+%d' % (size + (x, y)))


main = Tk()
main.resizable(width=False, height=False)
main.title('Flappy Bird')

# main.geometry('550x700')

main.geometry('1366x768')
main.configure(bg='black')

# main window of the game.

center(main)

BIRD_Y = 200
PIPE_X = 550
PIPE_HOLE = 0
NOW_PAUSE = False

# position of the pipes

Score_label = Label(main, text='Score : ', font=('Arial', 20))
Score_label.pack(anchor='w')

# score is displayed as a label

create_canvas()

birdImg = PhotoImage('player.png')
bird = w.create_image(100, BIRD_Y, image=birdImg)

# to set up the bird.

up_count = 0
endRectangle = endBest = endScore = None

pipeUp = w.create_rectangle(
    PIPE_X,
    0,
    PIPE_X + 100,
    PIPE_HOLE,
    fill='#ff0000',
    outline='black',
    )
pipeDown = w.create_rectangle(
    PIPE_X,
    PIPE_HOLE + 200,
    PIPE_X + 100,
    700,
    fill='#ff0000',
    outline='black',
    )


# score_w = w.create_text(15, 45, text="0", font='Impact 60', fill='#ffffff', anchor=W)

def generatePipeHole():
    global PIPE_HOLE
    global points
    global fps
    global cheats

    if cheats['feed me score'] == True:
        points += 50
    else:
        points += 1

    # w.itemconfig(score_w, text=str(points))

    Score_label.configure(text='Score : ' + str(points))
    PIPE_HOLE = random.randint(50, 500)
    if points + 1 % 7 == 0 and points != 0:
        fps -= 1


    # print("Score: " + str(points))

# sets up the holes for bird to pass

generatePipeHole()


def birdUp(event=None):
    global BIRD_Y
    global up_count
    global NOW_PAUSE

    if NOW_PAUSE == False:
        BIRD_Y -= 20
        if BIRD_Y <= 0:
            BIRD_Y = 0
        w.coords(bird, 100, BIRD_Y)
        if up_count < 5:
            up_count += 1
            main.after(fps, birdUp)
        else:

            up_count = 0


    # else:
    # ....restartGame()

def birdDown():
    global BIRD_Y
    global NOW_PAUSE

    BIRD_Y += 8
    if BIRD_Y >= 700:
        BIRD_Y = 700
    w.coords(bird, 100, BIRD_Y)
    if NOW_PAUSE == False:
        main.after(fps, birdDown)


# defines the motion of the bird in y axis

def pipesMotion():
    global PIPE_X
    global PIPE_HOLE
    global NOW_PAUSE

    PIPE_X -= 5
    w.coords(pipeUp, PIPE_X, 0, PIPE_X + 50, PIPE_HOLE)
    w.coords(pipeDown, PIPE_X, PIPE_HOLE + 200, PIPE_X + 50, 700)

    if PIPE_X < -100:
        PIPE_X = 550
        generatePipeHole()

    if NOW_PAUSE == False:
        main.after(fps, pipesMotion)


# defines the motion of pipe in x axis

def settings_page():
    var = IntVar()

    def sel():
        global UP_KEY
        k = var.get()
        file = open('key.txt', 'w')
        if k == 1:
            main.unbind(UP_KEY)
            UP_KEY = '<space>'
            file.write('<space>')
            main.bind(UP_KEY, birdUp)
        elif k == 2:
            main.unbind(UP_KEY)
            UP_KEY = '<Return>'
            file.write('<Return>')
            main.bind(UP_KEY, birdUp)
        elif k == 3:
            main.unbind(UP_KEY)
            UP_KEY = '<Shift_R>'
            file.write('<Shift_R>')
            main.bind(UP_KEY, birdUp)
        file.close()

# settings to change the command to move the bird

    tp = Toplevel()
    lb = Label(tp, text='Key to Move Bird Up : ')
    lb.pack()

    r = Radiobutton(tp, text='space', variable=var, value=1,
                    command=sel)
    r.pack(anchor='w', side='left')
    r2 = Radiobutton(tp, text='enter', variable=var, value=2,
                     command=sel)
    r2.pack(anchor='w', side='left')
    r3 = Radiobutton(tp, text='shift', variable=var, value=3,
                     command=sel)
    r3.pack(anchor='w', side='left')

    tp.mainloop()


def detectCollision():
    global NOW_PAUSE
    global BEST_SCORE
    global unwanted_widgets
    global hpoints, Score_label, cheats

    if PIPE_X < 150 and PIPE_X + 100 >= 55 and (BIRD_Y < PIPE_HOLE + 45
            or BIRD_Y > PIPE_HOLE + 175):

        if cheats['pipes are useless'] == True:
            pass
        else:
            NOW_PAUSE = True

            Score_label.pack_forget()
            w.pack_forget()  # hide everything

            sb = Button(main, text='Settings', command=settings_page)
            sb.pack(side='right', anchor='ne')

            ys = Label(main, text='Your score : ' + str(points),
                       font=('Arial', 40), fg='red')
            ys.pack()

            hfr = LabelFrame(main, text='HIGH points', font=('Arial',
                             20))
            hfr.pack(expand=True, fill=X, pady=(50, 0))

            unwanted_widgets.append(sb)
            unwanted_widgets.append(ys)
            unwanted_widgets.append(hfr)

            keys = list(hpoints.keys())
            values = list(hpoints.values())
            for i in range(5):
                try:
                    LHS = Label(hfr, text=str(i + 1) + '\t|\t'
                                + str(keys[i]) + '\t|\t'
                                + str(values[i]), font=('Arial', 15))
                    LHS.pack(anchor='w', padx=(50, 0))
                    unwanted_widgets.append(LHS)
                except:
                    pass

            rb = Button(main, text='Click to Play Again !',
                        font=('Arial', 30), command=restartGame)
            rb.pack(fill=X, expand=True, side='bottom', anchor='s')

            unwanted_widgets.append(rb)

            # if points > int(min(values[:5])):
            # ....messagebox.showinfo('Congratulations ! ','You have made it to HIGHSCORE list !')

            def add_HSCORE():
                na = e.get()
                sc = points
                file = open('HScore.txt', 'a')
                file.write('\n')
                file.write(na)
                file.write(',')
                file.write(str(sc))
                file.close()
                load_score()
                tp.destroy()

            tp = Toplevel()
            tp.geometry('300x300')
            l = Label(tp, text='Enter name : ')
            l.pack()
            e = Entry(tp)
            e.pack()
            b = Button(tp, text='Add Player ! ', command=add_HSCORE)
            b.pack()
            l = Label(tp,
                      text='You have made it to the\nLeder Board !!!!',
                      font=('Arial', 10))
            l.pack()
            tp.mainloop()

    if NOW_PAUSE == False:
        main.after(fps, detectCollision)


# the code will display the leaderboard, the score and settings if collision occurs and will give a button to restart.
# if the restart button is pressed the leaderboard, the score and settings is destroyed and game restarts.

def restartGame():
    global PIPE_X
    global BIRD_Y
    global points
    global NOW_PAUSE
    global fps
    global unwanted_widgets

    for i in unwanted_widgets:
        i.destroy()

    Score_label.pack()
    w.pack()

    BIRD_Y = 200
    PIPE_X = 550
    points = -1
    fps = 20
    NOW_PAUSE = False
    w.delete(endScore)
    w.delete(endRectangle)
    w.delete(endBest)
    generatePipeHole()
    main.after(fps, birdDown)
    main.after(fps, pipesMotion)
    main.after(fps, detectCollision)


# to restart the game after it ends and restart is pressed.

main.after(fps, birdDown)
main.after(fps, pipesMotion)
main.after(fps, detectCollision)
main.bind(UP_KEY, birdUp)
main.bind('<Escape>', pause_game)
main.bind('<KeyRelease>', check_key)

main.mainloop()

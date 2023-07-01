from tkinter import *
import random

WIDTH_GAME=600
HEIGHT_GAME=600
SIZE_SPACE=40
BODY_PART=3
SPEED=100
BACKGROUND="white"
FOOD_COLOR="red"
SNAKE_COLOR="green"
WALL_COLOR="black"



class Map:
    def __init__(self):
        self.wall=[(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(2,11),(2,12),
                   (12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),
                   (3,2), (3,12),(11,2), (11,12),
                   (5,5),(5,6), (5,7),(5,8),
                   (9,5),(9,6), (9,7),(9,8)]
        self.coordinate=[]

        for x, y in self.wall:
            self.coordinate.insert(0,(x*SIZE_SPACE, y*SIZE_SPACE))
        for x,y in self.coordinate:
            canvas.create_image(x, y, image=wall_image, anchor=NW)

class Snake:
    def __init__(self):
        self.body_part=BODY_PART
        self.coordinate=[]
        self.square=[]
        for i in range(0,BODY_PART):
            self.coordinate.append((0,0))
        for x,y in self.coordinate:
            square=canvas.create_rectangle(x, y, x+SIZE_SPACE, y+SIZE_SPACE, fill=SNAKE_COLOR)
            self.square.append(square)

class Food:
    def __init__(self, snake):
        global map
        self.snake=snake
        check_snake = True
        check_wall = True
        while check_snake or check_wall:
            x = random.randint(0, int(WIDTH_GAME / SIZE_SPACE - 1)) * SIZE_SPACE
            y = random.randint(0, int(HEIGHT_GAME / SIZE_SPACE - 1)) * SIZE_SPACE
            for a,b in self.snake.coordinate:
                check_snake = True
                if a==x and y==b:
                    break
                else:
                    check_snake=False
            for m,n in map.coordinate:
                check_wall = True
                if m==x and n==y:
                    break
                else:
                    check_wall=False
        self.coordinate=[x,y]
        self.food=canvas.create_oval(x, y, x+SIZE_SPACE, y+SIZE_SPACE, fill=FOOD_COLOR)

def turn_on(snake, food):
    global direction
    global map
    x,y = snake.coordinate[0]
    # check turn
    if direction=='down':
        y+=SIZE_SPACE
    elif direction=='up':
        y-=SIZE_SPACE
    elif direction=='right':
        x+=SIZE_SPACE
    else: x-=SIZE_SPACE

    #check chuyển tiếp
    if x==-SIZE_SPACE:
        x=WIDTH_GAME+x
        print(x)
    elif x==WIDTH_GAME:
        x=x-WIDTH_GAME
        print(x)
    elif y==-SIZE_SPACE:
        y= y+HEIGHT_GAME
        print(y)
    elif y==HEIGHT_GAME:
        y=y-HEIGHT_GAME
        print(y)
    snake.coordinate.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SIZE_SPACE, y + SIZE_SPACE, fill=SNAKE_COLOR)
    snake.square.insert(0, square)
    # check ăn food
    if x==food.coordinate[0] and y==food.coordinate[1]:
        global score
        score+=1
        canvas.delete(food.food)
        del food
        food=Food(snake)
        score_label.config(text=f"Score: {score}")
    else:
        del snake.coordinate[-1]
        canvas.delete(snake.square[-1])
        del snake.square[-1]

    if collision(snake):
        gameover()
    else:

        window.after(SPEED, turn_on, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction=='left':
        if direction!='right':
            direction=new_direction
    if new_direction=='right':
        if direction!='left':
            direction=new_direction
    if new_direction=='down':
        if direction!='up':
            direction=new_direction
    if new_direction=='up':
        if direction!='down':
            direction=new_direction

def collision(snake):
    global map
    x,y=snake.coordinate[0]
    for a,b in snake.coordinate[1:]:
        if a==x and b==y:
            return True
    for a,b in map.coordinate:
        if a==x and b==y:
            return True
def gameover():
    global gameover_label
    gameover_label.place(x=window.winfo_width() / 2, y=window.winfo_height() / 2, anchor=CENTER)

def new_game():
    global gameover_label
    global direction
    global score
    global map
    score=0
    score_label.config(text=f"Score: {score}")
    gameover_label.place_forget()
    canvas.delete(ALL)
    map = Map()
    snake = Snake()
    food = Food(snake)
    direction = 'down'
    turn_on(snake, food)

def convert_image(file):
    my_image = PhotoImage(file=file)
    width = int(my_image.width() / SIZE_SPACE)
    height = int(my_image.height() / SIZE_SPACE)
    subsample = my_image.subsample(width, height)
    return subsample


window=Tk()
window.title("Snake game")

score=0
frame=Frame(window)
frame.pack()
button=Button(frame, width=7, height=2, text="New Game", font=("consolas"), command=new_game)
score_label=Label(frame, text=f"Score: {score}", font=("consolas",40))
button.pack(side=RIGHT)
score_label.pack()

wall_image=convert_image('img.png')

canvas=Canvas(window, width=WIDTH_GAME, height=HEIGHT_GAME, bg=BACKGROUND)
canvas.pack()
gameover_label = Label(text="Game Over", font=("consolas", 40), fg="red")

direction='down'

new_game()

window.bind("<w>",lambda event: change_direction('up'))
window.bind("<s>",lambda event : change_direction('down'))
window.bind("<a>",lambda event : change_direction('left'))
window.bind("<d>",lambda event : change_direction('right'))
window.bind("<Up>",lambda event: change_direction('up'))
window.bind("<Down>",lambda event : change_direction('down'))
window.bind("<Left>",lambda event : change_direction('left'))
window.bind("<Right>",lambda event : change_direction('right'))

window.update()
width_window=window.winfo_width()
height_window=window.winfo_height()
x=int((window.winfo_screenwidth()/2)-(width_window/2))
y=int((window.winfo_screenheight()/2)-(height_window/2))

window.geometry(f"{width_window}x{height_window}+{x}+{y}")

window.mainloop()
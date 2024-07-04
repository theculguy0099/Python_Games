import turtle
import time
import random

delay = 0.05

score = 0
high_score = 0 

# setting up the screen
wn = turtle.Screen()
wn.title("Snake Game by Kevin")
wn.bgcolor("black")
wn.setup(width=900, height=900)
wn.tracer(0)  # turns off the animation

# snake head part
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("red")
head.penup()
head.goto(0, 0)  # starts from the center of the screen
head.direction = "stop"

# Food for Snake
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
# Set stretching factors to 2 (both horizontal and vertical)
food.shapesize(stretch_wid=1, stretch_len=1)
food.color("yellow")
food.penup()
food.goto(100, 100)

segments = []


# Scoring
pen=turtle.Turtle()
pen.speed(0)
# pen.shape("sqaure")
pen.color("skyblue")
pen.penup()
pen.hideturtle()
pen.goto(0,400)
pen.write("Your Score: 0 High Score: 0", align="center",font=("Courier",24,"normal"))
new_pen=turtle.Turtle()
new_pen.goto(-930,400)
new_pen.color("yellow")
new_pen.pendown()
new_pen.forward(2000)
    


def go_up():
    if head.direction!="down":
        head.direction = "up"

def go_down():
    if head.direction!="up":
        head.direction = "down"

def go_left():
    if head.direction!="right":
        head.direction = "left"

def go_right():
    if head.direction!="left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()  # current y coordinate
        head.sety(y+20)  # update the y coordinate
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()  # current x coordinate
        head.setx(x-20)  # update the x coordinate
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)


# KEYBOARD PRESSES
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# loop of main game
while True:
    wn.update()
    # BOUNDARY CONDITIONS
    if head.xcor() > 434 or head.xcor() < -440 or head.ycor() > 380 or head.ycor() < -440:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # now reset the segments
        for seg in segments:
            seg.goto(1200, 1200)  # only way to disappear them

        # clear the segments list
        segments.clear()
        high_score=max(high_score,score)
        score=0
        delay=0.05
        pen.clear()
        pen.write("Score: {} High_score: {}".format(score,high_score),align="center",font=("Courier",24,"normal"))

    if head.distance(food) < 20:
        x = random.randint(-440, 434)
        y = random.randint(-440, 380)
        food.goto(x, y)
        # incrementing length of the snake
        new_part = turtle.Turtle()
        new_part.speed(0)
        new_part.shape("square")
        new_part.color("white")
        new_part.penup()
        segments.append(new_part)
        # delay-=0.0001
        
        score+=10
        # high_score=max(high_score,score)
        pen.clear()
        pen.write("Score: {}".format(score),align="center",font=("Courier",24,"normal"))
        

    # moving the end parts in reverse order
    length = len(segments)
    for index in range(length-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # case of first part
    if (length > 0):  # checking whether there exist parts except head
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # check for self collision
    for seg in segments:
        if seg.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for seg in segments:
                seg.goto(1200, 1200)
            segments.clear()
            high_score=max(high_score,score)
            score=0
            delay=0.05
            pen.clear()
            pen.write("Score: {} High_score: {}".format(score,high_score),align="center",font=("Courier",24,"normal"))        

    time.sleep(delay)

wn.mainloop()

import random
import turtle

turtleScreen = turtle.Screen()
turtleScreen.bgcolor("lightblue")
turtleScreen.title("Catch The Turtle 🐢")

score = 0
game_over = False

score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()

timer_writer = turtle.Turtle()
timer_writer.hideturtle()
timer_writer.penup()

turtleList = []

def draw_board():
    score_writer.goto(0, 260)
    score_writer.clear()
    score_writer.write(arg=f"Score: {score}", move=False, align="center", font=("Arial", 22, "bold"))

def handleClick(x, y):
    global score
    if not game_over:
        score += 1
        score_writer.clear()
        score_writer.write(arg=f"Score: {score}", move=False, align="center", font=("Arial", 22, "bold"))

def makeTurtle(x, y):
    t = turtle.Turtle()
    t.penup()
    t.shape("turtle") 
    t.shapesize(2.5)
    t.color("dark green")
    t.setpos(x, y)
    t.onclick(handleClick)
    turtleList.append(t)

def setUpTurtle():
    xcordinates = [-200, -100, 0, 100, 200]
    yCordinates = [180, 80, -20, -120]

    for x in xcordinates:
        for y in yCordinates:
            makeTurtle(x, y)

def hideTurtles():
    for t in turtleList:
        t.hideturtle()

def RastgeleTurtleSec():
    if not game_over:
        hideTurtles()
        randomTurtle = random.choice(turtleList)
        randomTurtle.showturtle()
        turtleScreen.ontimer(RastgeleTurtleSec, 500)

def countdown(time):
    global game_over
    timer_writer.goto(0, 220)
    timer_writer.clear()

    if time > 0:
        timer_writer.write(arg=f"Time: {time}", move=False, align="center", font=("Arial", 16, "normal"))
        turtleScreen.ontimer(lambda: countdown(time - 1), 1000)
    else:
        game_over = True
        hideTurtles()
        timer_writer.clear()
        timer_writer.goto(0, 0)
        timer_writer.write(arg="Süre Bitti! Oyunu Bिटirdin 🏆", move=False, align="center", font=("Arial", 24, "bold"))

turtle.tracer(0)
setUpTurtle()
hideTurtles()
draw_board()
countdown(20)
RastgeleTurtleSec()
turtle.tracer(1)

turtle.done()
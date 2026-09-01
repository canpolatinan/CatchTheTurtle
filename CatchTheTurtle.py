import random
import turtle

turtleScreen = turtle.Screen()
turtleScreen.bgcolor("lightblue")

t1 = turtle.Turtle()
turtleList = []
score = 0


def YerDegistir(x, y):
  t1.penup()
  t1.setpos(x, y)
  t1.pendown()


def scoreTurtle():
  t1.color("black")
  FONT = ("Arial", 20, "normal")
  YerDegistir(0, 270)
  t1.hideturtle()
  t1.write(arg=f"Score : {score}", move=False, align="center", font=FONT)


scoreTurtle()


def handleClick(x, y):
  global score
  score += 1
  t1.clear()
  scoreTurtle()


def makeTurtle(x, y):
  t = turtle.Turtle()
  t.penup()
  t.shape("turtle")
  t.shapesize(3)
  t.color("dark green")
  t.setpos(x, y)
  t.onclick(handleClick)
  turtleList.append(t)


def setUpTurtle():
  xcordinates = [-200, -100, 0, 100, 200]
  yCordinates = [200, 100, 0, -100]

  for x in xcordinates:
    for y in yCordinates:
      makeTurtle(x, y)


def hideTurtles():
  for t in turtleList:
    t.hideturtle()


def RastgeleTurtleSec():
  hideTurtles()
  randomTurtle = random.choice(turtleList)
  randomTurtle.showturtle()
  turtleScreen.ontimer(RastgeleTurtleSec,500)



turtle.tracer(0)
setUpTurtle()
hideTurtles()
RastgeleTurtleSec()
turtle.tracer(1)

turtle.done()
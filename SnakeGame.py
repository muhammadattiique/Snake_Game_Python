import turtle
import time
import random

delay = 0.1
sc = 0
hc = 0
food_count = 0
special_food_active = False

bodies = []

# Screen setup
Screen = turtle.Screen()
Screen.setup(600, 600)
Screen.bgcolor('light blue')
Screen.title("Snake Game")
Screen.tracer(0)

# Head
Head = turtle.Turtle()
Head.speed(0)
Head.shape('classic')
Head.shapesize(3)
Head.color('blue')
Head.fillcolor('black')
Head.penup()
Head.goto(0, 0)
Head.direction = 'stop'

# Food
Food = turtle.Turtle()
Food.shape('circle')
Food.color('red')
Food.penup()
Food.goto(190, 190)

# Special Food
special_food = turtle.Turtle()
special_food.shape("circle")
special_food.color("Red")
special_food.shapesize(2)
special_food.penup()
special_food.hideturtle()

# Scoreboard
sb = turtle.Turtle()
sb.hideturtle()
sb.penup()
sb.goto(-290, 260)
sb.write("Score : 0 | Highest Score : 0",
         font=("Times New Roman", 20, "bold"))

# Game over pen
game_over_pen = turtle.Turtle()
game_over_pen.hideturtle()
game_over_pen.penup()

# Movement functions
def moveUp():
    if Head.direction != 'down':
        Head.direction = 'up'

def moveDown():
    if Head.direction != 'up':
        Head.direction = 'down'

def moveLeft():
    if Head.direction != 'right':
        Head.direction = 'left'

def moveRight():
    if Head.direction != 'left':
        Head.direction = 'right'

def movestop():
    Head.direction = 'stop'

def move():
    if Head.direction == 'up':
        Head.sety(Head.ycor() + 20)
        Head.setheading(90)

    if Head.direction == 'down':
        Head.sety(Head.ycor() - 20)
        Head.setheading(270)

    if Head.direction == 'left':
        Head.setx(Head.xcor() - 20)
        Head.setheading(180)

    if Head.direction == 'right':
        Head.setx(Head.xcor() + 20)
        Head.setheading(0)

# Blink special food
def blink():
    if special_food_active:
        if special_food.isvisible():
            special_food.hideturtle()
        else:
            special_food.showturtle()
        Screen.ontimer(blink, 300)

# Show special food
def show_special_food():
    global special_food_active
    special_food_active = True

    # hide normal food
    Food.hideturtle()

    x = random.randint(-250, 250)
    y = random.randint(-250, 250)
    special_food.goto(x, y)
    special_food.showturtle()

    blink()
    Screen.ontimer(hide_special_food, 6000)

# Hide special food
def hide_special_food():
    global special_food_active
    special_food_active = False

    special_food.hideturtle()

    # show normal food again
    Food.showturtle()

# Key bindings
Screen.listen()
Screen.onkey(moveUp, 'Up')
Screen.onkey(moveDown, 'Down')
Screen.onkey(moveLeft, 'Left')
Screen.onkey(moveRight, 'Right')
Screen.onkey(movestop, 'space')

# Main loop
try:
    while True:
        Screen.update()

        # Border collision
        if Head.xcor() > 290:
            Head.setx(-290)
        if Head.xcor() < -290:
            Head.setx(290)
        if Head.ycor() > 290:
            Head.sety(-290)
        if Head.ycor() < -290:
            Head.sety(290)

        # Normal food collision (ONLY if special food is not active)
        if (not special_food_active) and Head.distance(Food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            Food.goto(x, y)

            body = turtle.Turtle()
            body.speed(0)
            body.shape('square')
            body.color('blue')
            body.penup()

            if len(bodies) == 0:
                body.goto(Head.xcor(), Head.ycor())
            else:
                body.goto(bodies[-1].xcor(), bodies[-1].ycor())

            bodies.append(body)

            sc += 10
            food_count += 1
            delay -= 0.001

            if sc > hc:
                hc = sc

            sb.clear()
            sb.write("Score : {} | Highest Score : {}".format(sc, hc),
                     font=("Times New Roman", 20, "bold"))

            # Trigger special food every 5 foods
            if food_count % 5 == 0:
                show_special_food()

        # Special food collision
        if special_food_active and Head.distance(special_food) < 20:
            sc += 50

            special_food.hideturtle()
            special_food_active = False

            Food.showturtle()

            sb.clear()
            sb.write("Score : {} | Highest Score : {}".format(sc, hc),
                     font=("Times New Roman", 20, "bold"))

        # Save head position
        prev_x = Head.xcor()
        prev_y = Head.ycor()


        # Move body
        if len(bodies) > 0:
            for i in range(len(bodies) - 1, 0, -1):
                x = bodies[i - 1].xcor()
                y = bodies[i - 1].ycor()
                bodies[i].goto(x, y)

            bodies[0].goto(prev_x, prev_y)
            if len(bodies) > 0: 
                bodies[0].goto(Head.xcor(), Head.ycor())
        move()

        # Self collision
        for body in bodies:
            if body.distance(Head) < 20:
                time.sleep(1)

                Head.goto(0, 0)
                Head.direction = 'stop'

                game_over_pen.goto(0, 0)
                game_over_pen.write("Game Over!", align="center",
                                    font=("Times New Roman", 20, "bold"))

                Screen.update()
                time.sleep(5)
                game_over_pen.clear()

                for b in bodies:
                    b.hideturtle()

                bodies.clear()
                sc = 0
                delay = 0.1
                food_count = 0

                sb.clear()
                sb.write("Score : {} | Highest Score : {}".format(sc, hc),
                         font=("Times New Roman", 20, "bold"))

        time.sleep(delay)

except turtle.Terminator:
    print("Game closed safely")
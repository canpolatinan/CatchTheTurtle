import random
import turtle
import os


HIGHSCORE_FILE = "highscore.txt"


def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_highscore(value):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(value))
    except OSError:
        pass


DIFFICULTIES = {
    "Kolay": dict(duration=25, base_interval=800, min_interval=450,
                  bomb_chance=0.10, gold_chance=0.22, hit_radius=62, miss_penalty=0,
                  color="#4CAF50"),
    "Orta":  dict(duration=22, base_interval=620, min_interval=320,
                  bomb_chance=0.16, gold_chance=0.16, hit_radius=52, miss_penalty=0,
                  color="#FF9800"),
    "Zor":   dict(duration=20, base_interval=480, min_interval=200,
                  bomb_chance=0.24, gold_chance=0.12, hit_radius=42, miss_penalty=1,
                  color="#E53935"),
}

X_POSITIONS = [-200, -100, 0, 100, 200]
Y_POSITIONS = [160, 60, -40, -140]

turtleScreen = turtle.Screen()
turtleScreen.bgcolor("#eaf6ff")
turtleScreen.title("Catch The Turtle 🐢")
turtleScreen.setup(width=680, height=680)
turtleScreen.tracer(0)



state = "menu"
score = 0
high_score = load_highscore()
active_turtle = None
current_interval = 600
settings = DIFFICULTIES["Orta"]
turtleList = []
popups = []
menu_buttons = []


def make_writer():
    w = turtle.Turtle()
    w.hideturtle()
    w.penup()
    return w


title_shadow = make_writer()
title_writer = make_writer()
score_writer = make_writer()
timer_writer = make_writer()
legend_writer = make_writer()
message_writer = make_writer()

border_pen = turtle.Turtle()
border_pen.hideturtle()
border_pen.penup()
border_pen.speed(0)


def draw_border():
    border_pen.color("#4a90d9")
    border_pen.pensize(6)
    border_pen.goto(-320, -320)
    border_pen.pendown()
    for _ in range(2):
        border_pen.forward(640)
        border_pen.left(90)
        border_pen.forward(640)
        border_pen.left(90)
    border_pen.penup()


def draw_title():
    title_shadow.clear()
    title_shadow.color("#9ecbf0")
    title_shadow.goto(3, 297)
    title_shadow.write("🐢 Catch The Turtle 🐢", move=False, align="center",
                        font=("Arial", 26, "bold"))
    title_writer.clear()
    title_writer.color("#22577a")
    title_writer.goto(0, 300)
    title_writer.write("🐢 Catch The Turtle 🐢", move=False, align="center",
                        font=("Arial", 26, "bold"))





def draw_scoreboard():
    score_writer.clear()
    score_writer.goto(0, 250)
    score_writer.color("#1b1b1b")
    score_writer.write(f"Skor: {score}    En Yüksek: {high_score}",
                        move=False, align="center", font=("Arial", 18, "bold"))


def draw_timer(time_left):
    timer_writer.clear()
    timer_writer.goto(0, 215)
    timer_writer.color("#1b1b1b")
    timer_writer.write(f"Süre: {time_left}", move=False, align="center",
                        font=("Arial", 15, "normal"))


def draw_legend():
    legend_writer.clear()
    legend_writer.goto(0, -300)
    legend_writer.color("#1b1b1b")
    legend_writer.write("🟢 Yeşil = +1     🟡 Altın = +3 (nadir)     🔴 Kırmızı = -2 (bombadan kaç!)",
                         move=False, align="center", font=("Arial", 12, "normal"))



def make_turtle(x, y):
    t = turtle.Turtle()
    t.penup()
    t.shape("turtle")
    t.setpos(x, y)
    t.hideturtle()
    turtleList.append(t)


def setup_turtles():
    for x in X_POSITIONS:
        for y in Y_POSITIONS:
            make_turtle(x, y)


def hide_all_turtles():
    global active_turtle
    for t in turtleList:
        t.hideturtle()
    active_turtle = None


def animate_appear(t, step=0):
    sizes = [1.0, 1.7, 2.2, 2.5]
    if state != "playing" or not t.isvisible():
        return
    if step < len(sizes):
        t.shapesize(sizes[step])
        turtleScreen.update()
        turtleScreen.ontimer(lambda: animate_appear(t, step + 1), 45)


def show_popup(x, y, text, color, step=0):
    if step == 0:
        p = make_writer()
        p.color(color)
        popups.append(p)
    else:
        p = popups[-1]
        p.clear()

    if step < 6:
        p.goto(x, y + 15 + step * 6)
        p.write(text, move=False, align="center", font=("Arial", 16, "bold"))
        turtleScreen.update()
        turtleScreen.ontimer(lambda: show_popup(x, y, text, color, step + 1), 60)
    else:
        p.clear()
        popups.remove(p)


def show_random_turtle():
    global active_turtle

    if state != "playing":
        return

    hide_all_turtles()
    chosen = random.choice(turtleList)

    roll = random.random()
    if roll < settings["bomb_chance"]:
        chosen.color("#e53935")
    elif roll < settings["bomb_chance"] + settings["gold_chance"]:
        chosen.color("#ffc107")
    else:
        chosen.color("#2e7d32")

    chosen.shapesize(1.0)
    chosen.showturtle()
    active_turtle = chosen
    animate_appear(chosen)
    turtleScreen.update()

    turtleScreen.ontimer(show_random_turtle, current_interval)


def speed_up(elapsed):
    global current_interval
    progress = min(elapsed / settings["duration"], 1)
    current_interval = int(
        settings["base_interval"]
        - (settings["base_interval"] - settings["min_interval"]) * progress
    )


def countdown(time_left, elapsed=0):
    if state != "playing":
        return

    draw_timer(time_left)
    speed_up(elapsed)

    if time_left > 0:
        turtleScreen.ontimer(lambda: countdown(time_left - 1, elapsed + 1), 1000)
    else:
        end_game()


def on_screen_click(x, y):
    global score, active_turtle

    if state != "playing":
        return

    if active_turtle is not None and active_turtle.isvisible():
        tx, ty = active_turtle.pos()
        if (x - tx) ** 2 + (y - ty) ** 2 <= settings["hit_radius"] ** 2:
            color = active_turtle.fillcolor()
            if color == "#e53935":
                score = max(0, score - 2)
                show_popup(tx, ty, "-2", "#e53935")
            elif color == "#ffc107":
                score += 3
                show_popup(tx, ty, "+3", "#c98a00")
            else:
                score += 1
                show_popup(tx, ty, "+1", "#2e7d32")

            active_turtle.hideturtle()
            active_turtle = None
            draw_scoreboard()
            turtleScreen.update()
            return

    if settings["miss_penalty"] > 0:
        score = max(0, score - settings["miss_penalty"])
        draw_scoreboard()
        turtleScreen.update()


def start_game(difficulty_name):
    global score, state, current_interval, settings

    settings = DIFFICULTIES[difficulty_name]
    score = 0
    state = "playing"
    current_interval = settings["base_interval"]

    message_writer.clear()


    for b in menu_buttons:
        b.clear()
        b.hideturtle()

    draw_scoreboard()
    draw_legend()
    hide_all_turtles()
    countdown(settings["duration"])
    show_random_turtle()
    turtleScreen.update()


def end_game():
    global state, high_score

    state = "over"
    hide_all_turtles()
    timer_writer.clear()
    legend_writer.clear()

    if score > high_score:
        high_score = score
        save_highscore(high_score)
        result_text = f"Süre Bitti! Yeni Rekor 🏆  Skor: {score}"
    else:
        result_text = f"Süre Bitti!  Skorun: {score}   En Yüksek: {high_score}"

    message_writer.clear()
    message_writer.goto(0, 40)
    message_writer.color("#1b1b1b")
    message_writer.write(result_text, move=False, align="center",
                          font=("Arial", 18, "bold"))

    draw_scoreboard()
    show_menu(restart=True)
    turtleScreen.update()

def make_menu_button(label, x, color, handler):
    b = turtle.Turtle()
    b.penup()
    b.shape("square")
    b.shapesize(stretch_wid=1.6, stretch_len=4.2)
    b.color("white", color)
    b.goto(x, -60)
    b.onclick(handler)
    menu_buttons.append(b)

    lbl = make_writer()
    lbl.color("white")
    lbl.goto(x, -68)
    lbl.write(label, move=False, align="center", font=("Arial", 13, "bold"))
    menu_buttons.append(lbl)


def show_menu(restart=False):
    for b in menu_buttons:
        b.clear() if hasattr(b, "clear") else None
        b.hideturtle() if hasattr(b, "hideturtle") else None
    menu_buttons.clear()

    if not restart:
        message_writer.clear()
        message_writer.goto(0, 40)
        message_writer.color("#1b1b1b")
        message_writer.write("Bir zorluk seviyesi seç ve başla!", move=False,
                              align="center", font=("Arial", 17, "bold"))

    positions = [-180, 0, 180]
    for (name, cfg), x in zip(DIFFICULTIES.items(), positions):
        make_menu_button(name, x, cfg["color"], lambda x1, y1, n=name: start_game(n))

    turtleScreen.update()

draw_border()
draw_title()
draw_scoreboard()
setup_turtles()
show_menu(restart=False)

turtleScreen.onclick(on_screen_click)
turtleScreen.update()

turtle.done()
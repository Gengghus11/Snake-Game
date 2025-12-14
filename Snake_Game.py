# Snake Game 
# By: Voo Geng Loong

# Snake Game Imports
import turtle
import time
import random
import pygame

# Snake Game Sound Import by Pygame
pygame.mixer.init()
pygame.mixer.music.load("Music/bgmusic.mp3")
nom_sound = pygame.mixer.Sound("Music/nom.wav")
thud_sound = pygame.mixer.Sound("Music/thud.mp3")
pygame.mixer.music.play(-1)

# Snake Movement will be slowed down
delay = 0.1

# Area of food and obstacles placement
min_x = -370
max_x = 370
min_y = -370
max_y = 290

###########################################################################################################
# 1.) Game Interface Feature
###########################################################################################################

# Music Volume
music_volume = 0.2
music_muted = False

###########################################################################################################
# Snake Game Score
###########################################################################################################

score = 0
high_score = 0

# Scoring Display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 340)
pen.write("Score: 0  High Score: 0",
          align="center", font=("Ariel", 24, "normal"))

###########################################################################################################
# Screen / State Setup
###########################################################################################################

# Current Gaming State
game_state = "menu"

# Screen Setup
wn = turtle.Screen()
wn.title("Snake Game by: Voo Geng Loong")
wn.bgpic("Images/Snake.gif")
wn.setup(width=800, height=800)
wn.tracer(0)  # Turns off screen updates

###########################################################################################################
# Assets: Food / Obstacle / Snake Images
###########################################################################################################

# Food Images
wn.register_shape("Images/Cherry.gif")
wn.register_shape("Images/Apple.gif")
wn.register_shape("Images/Strawberry.gif")
wn.register_shape("Images/Star.gif")

# Obstacle Image
wn.register_shape("Images/Rock.gif")

# Snake Head Images
wn.register_shape("Images/SnakeHeadRight.gif")
wn.register_shape("Images/SnakeHeadLeft.gif")
wn.register_shape("Images/SnakeHeadUp.gif")
wn.register_shape("Images/SnakeHeadDown.gif")

###########################################################################################################
# Snake Head
###########################################################################################################

head = turtle.Turtle()
head.speed(0)
head.shape("Images/SnakeHeadRight.gif")
head.penup()
head.goto(0, 0)
head.direction = "stop"

###########################################################################################################
# Border Drawing
###########################################################################################################

border = turtle.Turtle()
border.speed(0)
border.color("black")
border.penup()
border.goto(-390, -390)
border.pendown()
border.pensize(4)

# Rectangle border
border.goto(390, -390)    # bottom-right
border.goto(390, 310)     # top-right
border.goto(-390, 310)    # top-left
border.goto(-390, -390)   # back to bottom-left

border.hideturtle()

###########################################################################################################
# UI Pens (Menus / Buttons)
###########################################################################################################

# Menu Display
message_pen = turtle.Turtle()
message_pen.speed(0)
message_pen.shape("square")
message_pen.color("black")
message_pen.penup()
message_pen.hideturtle()
message_pen.goto(0, 0)

# Turtle to draw buttons
button_pen = turtle.Turtle()
button_pen.speed(0)
button_pen.shape("square")
button_pen.color("black")
button_pen.penup()
button_pen.hideturtle()

# Stores menu button hitboxes
pause_buttons = []
menu_buttons = []
gameover_buttons = []


def clear_pause_buttons():
    button_pen.clear()
    pause_buttons.clear()
    menu_buttons.clear()
    gameover_buttons.clear()


def show_main_menu():
    clear_pause_buttons()
    message_pen.clear()

    # Title
    message_pen.goto(0, 120)
    message_pen.write("Snake Game", align="center", font=("Ariel", 36, "bold"))
    message_pen.goto(0, 80)
    message_pen.write("By: Voo Geng Loong", align="center", font=("Ariel", 18, "normal"))

    labels = [
        ("Play", "play", 10),
        ("Quit", "quit", -50),
    ]

    button_width = 260
    button_height = 40

    button_pen.penup()
    for text, name, cy in labels:
        left = -button_width // 2
        right = button_width // 2
        top = cy + button_height // 2
        bottom = cy - button_height // 2

        # Draw rectangle
        button_pen.goto(left, top)
        button_pen.pendown()
        button_pen.goto(right, top)
        button_pen.goto(right, bottom)
        button_pen.goto(left, bottom)
        button_pen.goto(left, top)
        button_pen.penup()

        # Write label
        message_pen.goto(0, cy - 10)
        message_pen.write(text, align="center", font=("Ariel", 20, "normal"))

        # Store hitbox for main menu
        menu_buttons.append({
            "name": name,
            "x1": left,
            "x2": right,
            "y1": bottom,
            "y2": top,
        })


# Draw main menu once at start
show_main_menu()

###########################################################################################################
# Snake Body
###########################################################################################################

segments = []


def hide_snake():
    head.hideturtle()
    for segment in segments:
        segment.hideturtle()


def show_snake():
    head.showturtle()
    for segment in segments:
        segment.showturtle()


hide_snake()

# Fancy snake body style
BODY_COLORS = ["#145A32", "#27AE60"]


def create_segment():
    """Create one nicely styled body segment."""
    seg = turtle.Turtle()
    seg.speed(0)
    seg.shape("square")
    seg.shapesize(stretch_wid=0.8, stretch_len=0.8)
    # Alternate colors based on current length
    seg.color(BODY_COLORS[len(segments) % len(BODY_COLORS)])
    seg.penup()
    seg.goto(1000, 1000)
    return seg

###########################################################################################################
# 2.) Functions for Snake Game
###########################################################################################################

# When Snake goes up it cannot go down (and similar for other directions)
def go_up():
    if head.direction != "down":
        head.direction = "up"
        head.shape("Images/SnakeHeadUp.gif")


def go_down():
    if head.direction != "up":
        head.direction = "down"
        head.shape("Images/SnakeHeadDown.gif")


def go_left():
    if head.direction != "right":
        head.direction = "left"
        head.shape("Images/SnakeHeadLeft.gif")


def go_right():
    if head.direction != "left":
        head.direction = "right"
        head.shape("Images/SnakeHeadRight.gif")


# Moving direction of the Snake
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

###########################################################################################################
# Food & Obstacles Setup
###########################################################################################################

foods = []
FOOD_COUNT = 12
FOOD_SHAPES = [
    "Images/Cherry.gif",
    "Images/Apple.gif",
    "Images/Strawberry.gif",
    "Images/Star.gif",
]

obstacles = []
OBSTACLE_COUNT = 15
OBSTACLE_SHAPE = ["Images/Rock.gif"]

###########################################################################################################
# Game Over Menu
###########################################################################################################


def show_game_over_menu():
    clear_pause_buttons()
    message_pen.clear()

    # Title
    message_pen.goto(0, 140)
    message_pen.write("Game Over", align="center", font=("Ariel", 36, "bold"))

    labels = [
        ("Restart", "restart", 40),
        ("Quit", "quit", -20),
    ]

    button_width = 260
    button_height = 40

    # Draw buttons
    for text, name, cy in labels:
        left = -button_width // 2
        right = button_width // 2
        top = cy + button_height // 2
        bottom = cy - button_height // 2

        button_pen.goto(left, top)
        button_pen.pendown()
        button_pen.goto(right, top)
        button_pen.goto(right, bottom)
        button_pen.goto(left, bottom)
        button_pen.goto(left, top)
        button_pen.penup()

        # Write button label
        message_pen.goto(0, cy - 10)
        message_pen.write(text, align="center", font=("Ariel", 20, "normal"))

        # Store hitbox
        gameover_buttons.append({
            "name": name,
            "x1": left,
            "x2": right,
            "y1": bottom,
            "y2": top,
        })


def wall_collision_effect():
    """Flash the border red a few times when you hit the wall."""
    for _ in range(3):
        # Draw border in red
        border.clear()
        border.color("red")
        border.penup()
        border.goto(-390, -390)
        border.pendown()
        border.pensize(4)
        border.goto(390, -390)    # bottom-right
        border.goto(390, 310)     # top-right
        border.goto(-390, 310)    # top-left
        border.goto(-390, -390)   # back to bottom-left
        border.hideturtle()
        wn.update()
        time.sleep(0.05)

        # Draw border back in black
        border.clear()
        border.color("black")
        border.penup()
        border.goto(-390, -390)
        border.pendown()
        border.pensize(4)
        border.goto(390, -390)
        border.goto(390, 310)
        border.goto(-390, 310)
        border.goto(-390, -390)
        border.hideturtle()
        wn.update()
        time.sleep(0.05)


def obstacle_collision_effect(obs):
    """Flash the obstacle red and back to normal."""
    original_shape = obs.shape()
    for _ in range(3):
        obs.color("red")
        wn.update()
        time.sleep(0.05)

        obs.color("white")
        wn.update()
        time.sleep(0.05)

    # Restore original shape (important!)
    obs.shape(original_shape)
    obs.color("white")

###########################################################################################################
# Pause / Music / State Helpers
###########################################################################################################


def show_pausemenu():
    message_pen.clear()
    message_pen.write("Game Paused\n\nPress R to Restart\nPress Q to Quit",
                      align="center", font=("Ariel", 28, "normal"))


def hide_game_over_menu():
    message_pen.clear()
    clear_pause_buttons()


def start_game_from_menu():
    global game_state
    if game_state == "menu":
        reset_game()


# Restart function when losing the game
def reset_game():
    """Reset everything and start a new game."""
    global score, delay, segments, game_state

    # Move head back to center
    head.goto(0, 0)
    head.direction = "stop"

    # Hide segments
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    # Reset score and speed
    score = 0
    delay = 0.1

    # Update score display
    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score),
              align="center", font=("Ariel", 24, "normal"))

    # Hide menu and set state to playing
    hide_game_over_menu()
    game_state = "playing"
    show_snake()

    # New random positions each time you restart
    randomize_food_and_obstacles()

    show_all_food()
    show_all_obstacles()
    if not music_muted:
        pygame.mixer.music.unpause()


# Quitting the game after losing or pausing
def quit_game():
    wn.bye()


# Pausing the Game
def pausegame():
    global game_state
    if game_state == "playing":
        game_state = "paused"
        show_pausemenu()
        head.direction = "stop"
        pygame.mixer.music.pause()
        show_snake()
        hide_all_food()
        hide_all_obstacles()
    elif game_state == "paused":
        hide_game_over_menu()
        game_state = "playing"
        show_snake()
        show_all_food()
        show_all_obstacles()
        if not music_muted:
            pygame.mixer.music.unpause()


# Eating Sound
def play_nom_sound():
    nom_sound.play()


# Background Music
def show_music_menu():
    """Show music settings menu."""
    clear_pause_buttons()
    message_pen.clear()
    vol_percent = int(music_volume * 100)
    mute_text = "Yes" if music_muted else "No"
    message_pen.write(
        f"Music Settings\n\n"
        f"Volume: {vol_percent}%\n"
        f"Muted: {mute_text}\n\n"
        f"Up Arrow: Volume Up\n"
        f"Down Arrow: Volume Down\n"
        f"M: Mute / Unmute\n"
        f"ESC: Back",
        align="center",
        font=("Ariel", 22, "normal")
    )


def update_music_volume():
    if music_muted:
        pygame.mixer.music.set_volume(0.0)
    else:
        pygame.mixer.music.set_volume(music_volume)


# Background Music Volume Up, Down & Muting
def volume_up():
    global music_volume
    if game_state != "music_settings":  # only works inside menu
        return
    if music_volume < 1.0:
        music_volume += 0.1
    update_music_volume()
    show_music_menu()


def volume_down():
    global music_volume
    if game_state != "music_settings":
        return
    if music_volume > 0.0:
        music_volume -= 0.1
    update_music_volume()
    show_music_menu()


def toggle_mute():
    global music_muted
    if game_state != "music_settings":
        return
    music_muted = not music_muted
    update_music_volume()
    show_music_menu()


def open_music_menu():
    global game_state
    head.direction = "stop"
    game_state = "music_settings"
    hide_snake()
    hide_all_food()
    hide_all_obstacles()
    show_music_menu()


def close_music_menu():
    global game_state
    hide_game_over_menu()
    game_state = "paused"   # return to pause screen
    show_pausemenu()


def show_pausemenu():
    clear_pause_buttons()
    message_pen.clear()

    # Title
    message_pen.goto(0, 140)
    message_pen.write("Game Paused", align="center", font=("Ariel", 32, "bold"))

    labels = [
        ("Resume", "resume", 60),
        ("Restart", "restart", 10),
        ("Music Settings", "music", -40),
        ("Quit", "quit", -90),
    ]

    button_width = 260
    button_height = 40

    button_pen.penup()
    for text, name, cy in labels:
        left = -button_width // 2
        right = button_width // 2
        top = cy + button_height // 2
        bottom = cy - button_height // 2

        # Draw rectangle
        button_pen.goto(left, top)
        button_pen.pendown()
        button_pen.goto(right, top)
        button_pen.goto(right, bottom)
        button_pen.goto(left, bottom)
        button_pen.goto(left, top)
        button_pen.penup()

        # Write label
        message_pen.goto(0, cy - 10)
        message_pen.write(text, align="center", font=("Ariel", 20, "normal"))

        # Store hitbox
        pause_buttons.append({
            "name": name,
            "x1": left,
            "x2": right,
            "y1": bottom,
            "y2": top,
        })

    # Reset pen pos
    message_pen.goto(0, 0)


def m_pressed():
    if game_state == "music_settings":
        toggle_mute()
    elif game_state in ("paused", "playing"):
        open_music_menu()


def esc_pressed():
    if game_state == "music_settings":
        close_music_menu()
    else:
        pausegame()


def handle_click(x, y):
    global game_state

    # Clicks in PAUSE MENU
    if game_state == "paused":
        for btn in pause_buttons:
            if btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]:
                if btn["name"] == "resume":
                    pausegame()          # toggles back to playing
                elif btn["name"] == "restart":
                    reset_game()
                elif btn["name"] == "music":
                    open_music_menu()
                elif btn["name"] == "quit":
                    quit_game()
                return   # stop after one click

    # Clicks in MAIN MENU
    if game_state == "menu":
        for btn in menu_buttons:
            if btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]:
                if btn["name"] == "play":
                    start_game_from_menu()
                elif btn["name"] == "quit":
                    quit_game()
                return

    # Clicks in GAME OVER MENU
    if game_state == "game_over":
        for btn in gameover_buttons:
            if btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]:
                if btn["name"] == "restart":
                    reset_game()
                elif btn["name"] == "quit":
                    quit_game()
                return

###########################################################################################################
# Spawning / Position Helpers
###########################################################################################################


def get_free_position():
    """Return a random (x, y) inside the play area that does not overlap food/obstacles."""
    while True:
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)

        collision = False

        # Check against existing food
        for f in foods:
            if f.distance(x, y) < 24:
                collision = True
                break

        # Check against existing obstacles
        if not collision:
            for obs in obstacles:
                if obs.distance(x, y) < 24:
                    collision = True
                    break

        if not collision:
            return x, y


# Creating the shape and colour of the food
def spawn_food():
    """Create food turtle and return it."""
    f = turtle.Turtle()
    f.speed(0)
    food_shape = random.choice(FOOD_SHAPES)
    f.shape(food_shape)
    f.penup()

    x, y = get_free_position()
    f.goto(x, y)

    return f


def hide_all_food():
    for food in foods:
        food.hideturtle()


def show_all_food():
    for food in foods:
        food.showturtle()


def spawn_obstacle():
    """Create one obstacle block and return it."""
    obs = turtle.Turtle()
    obs.speed(0)
    obstacle_shape = random.choice(OBSTACLE_SHAPE)
    obs.shape(obstacle_shape)
    obs.penup()

    x, y = get_free_position()
    obs.goto(x, y)
    return obs


def hide_all_obstacles():
    for obs in obstacles:
        obs.hideturtle()


def show_all_obstacles():
    for obs in obstacles:
        obs.showturtle()


def randomize_food_and_obstacles():
    """Move every food and obstacle to a new random free position."""
    # Move foods first
    for food in foods:
        x, y = get_free_position()
        food.goto(x, y)

    # Then move obstacles
    for obs in obstacles:
        x, y = get_free_position()
        obs.goto(x, y)


# Create initial food items
for i in range(FOOD_COUNT):
    foods.append(spawn_food())

# Create initial obstacles
for i in range(OBSTACLE_COUNT):
    obstacles.append(spawn_obstacle())

if game_state == "menu":
    hide_all_food()
    hide_all_obstacles()


def play_thud_sound():
    thud_sound.play()

###########################################################################################################
# Keybindings
###########################################################################################################

wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(m_pressed, "m")
wn.onkeypress(volume_up, "Up")
wn.onkeypress(volume_down, "Down")
wn.onkeypress(esc_pressed, "Escape")
wn.onclick(handle_click)

###########################################################################################################
# Main Game Loop
###########################################################################################################

while True:
    wn.update()

    # If game over, just wait, don't update snake
    if game_state in ("game_over", "paused", "music_settings", "menu"):
        time.sleep(0.1)
        continue

    # Collision with borders
    if head.xcor() > 390 or head.xcor() < -390 or head.ycor() > 310 or head.ycor() < -390:
        wall_collision_effect()
        play_thud_sound()
        game_state = "game_over"
        show_game_over_menu()
        pygame.mixer.music.pause()
        hide_snake()
        hide_all_food()
        hide_all_obstacles()

    # Collision with multiple food
    for food in foods:
        if head.distance(food) < 20:
            play_nom_sound()

            # Move this food somewhere else
            x, y = get_free_position()
            food.goto(x, y)

            # Give it a new random sprite
            new_shape = random.choice(FOOD_SHAPES)
            food.shape(new_shape)

            # Add segment
            new_segment = create_segment()
            segments.append(new_segment)

            # Modify speed and score
            delay -= 0.001

            # Bonus: star gives extra points
            if new_shape == "Images/Star.gif":
                score += 30
            else:
                score += 10   # normal fruit

            if score > high_score:
                high_score = score

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score),
                      align="center", font=("Ariel", 24, "normal"))

    # Move end of segment to first reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    # Move the head
    move()

    # Check for collision with obstacles
    for obs in obstacles:
        if head.distance(obs) < 20:
            play_thud_sound()
            obstacle_collision_effect(obs)
            game_state = "game_over"
            show_game_over_menu()
            pygame.mixer.music.pause()
            hide_snake()
            hide_all_food()
            hide_all_obstacles()
            break

    # Check for head collision with body segment
    for segment in segments:
        if segment.distance(head) < 20:
            play_thud_sound()
            game_state = "game_over"
            show_game_over_menu()
            pygame.mixer.music.pause()
            hide_snake()
            hide_all_food()
            hide_all_obstacles()
            break

    time.sleep(delay)

wn.mainloop()
import random
import time
import pgzrun

WIDTH = 600
HEIGHT = 600
START_SPEED = 10
FINAL_LEVEL = 6

# Extra items list (Capitalized so it won't be overwritten!)
ITEMS = ["plastic", "glass", "metal", "wrapper"]

game_over = False
game_complete = False
current_level = 1
items = []
animation = []

def draw():
    screen.clear()
    screen.blit("background", (0, 0))
    if game_over:
        msg("GAME OVER", "Try again!")
    elif game_complete:
        msg("YOU WIN!", "Congratulations!")
    else:
        for item in items:
            item.draw()

def update():
    if not items and not game_complete and not game_over:
        make_items()

def make_items():
    global items, animation
    names = ["paper"] + [random.choice(ITEMS) for _ in range(current_level)]
    random.shuffle(names)
    gap = WIDTH / (len(names) + 1)
    
    items = []
    animation = []
    for i, name in enumerate(names):
        item = Actor(name, anchor=("center", "bottom"))
        item.x = (i + 1) * gap
        anim = animate(item, duration=START_SPEED - current_level, y=HEIGHT, on_finished=game_over_func)
        animation.append(anim)
        items.append(item)

def on_mouse_down(pos):
    global items, animation, current_level, game_complete
    for item in items:
        if item.collidepoint(pos):
            if "paper" in item.image:
                for a in animation:
                    if a.running:
                        a.stop()
                if current_level == FINAL_LEVEL:
                    game_complete = True
                else:
                    current_level += 1
                    items = []
                    animation = []
            else:
                game_over_func()

def game_over_func():
    global game_over
    game_over = True

def msg(title, sub):
    screen.draw.text(title, fontsize=60, color="white", center=(WIDTH / 2, HEIGHT / 2 - 20))
    screen.draw.text(sub, fontsize=30, color="white", center=(WIDTH / 2, HEIGHT / 2 + 35))

pgzrun.go()

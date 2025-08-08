add_library('minim')
add_library('sound')
import random

player = Minim(this)
jump_sound = player.loadFile("jump.mp3")
bg_music = player.loadFile("background.mp3")
# bg_music.loop()

# Constants
WIDTH = 800
HEIGHT = 800
GRAVITY = 0.4

# Game states: 'cover', 'playing', 'gameover'
gameState = 'cover'

# Global vars
yshift = 0

# Colors
colors = [
    color(204, 0, 0),    # Red
    color(106, 168, 79), # Green
    color(241, 194, 50), # Yellow
    color(61, 133, 198)  # Blue
]

# Start Button
class StartButton:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hovered = False

    def isHovered(self):
        return self.x <= mouseX <= self.x + self.w and self.y <= mouseY <= self.y + self.h

    def display(self):
        self.hovered = self.isHovered()
        if self.hovered:
            noStroke()
            for i in range(4):
                fill(colors[i])
                rect(self.x + i * self.w / 4, self.y, self.w / 4, self.h)
        else:
            fill(255)
            rect(self.x, self.y, self.w, self.h)

        fill(0)
        textSize(24)
        textAlign(CENTER, CENTER)
        text("START", self.x + self.w / 2, self.y + self.h / 2)

startBtn = StartButton(WIDTH//2 - 75, HEIGHT//2 + 40, 150, 50)

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.radius = 20
        self.vy = 0
        self.color_idx = random.randint(0, 3)
        self.dead = False
        self.started = False

    def update(self):
        if not self.dead and self.started:
            self.vy += GRAVITY
            self.y += self.vy
    
            global yshift
            if self.y < HEIGHT // 2:
                yshift = HEIGHT // 2 - self.y
            else:
                yshift = 0
    
            if self.y - yshift > HEIGHT + self.radius:
                self.dead = True


    def jump(self):
        if not self.dead:
            self.vy = -8
            # jump_sound.rewind()
            # jump_sound.play()

    def show(self):
        fill(colors[self.color_idx])
        noStroke()
        ellipse(self.x, self.y + yshift, self.radius * 2, self.radius * 2)

# Obstacle class
class Obstacle:
    def __init__(self, y, size=150, speed=1):
        self.x = WIDTH // 2
        self.y = y 
        self.size = size
        self.angle = 0
        self.speed = speed
        self.scored = False

    def update(self):
        self.angle += self.speed

    def show(self):
        noFill()
        strokeWeight(10)
        for i in range(4):
            stroke(colors[i])
            arc(self.x, self.y + yshift, self.size, self.size,
                radians(i * 90 + self.angle),
                radians((i + 1) * 90 + self.angle))

    def check_collision(self, player):
        d = dist(player.x, player.y, self.x, self.y)
        if abs(d) > self.size / 2 or abs(d) < self.size / 2 - 20:
            return
        relative_angle = (degrees(atan2(player.y - self.y, player.x - self.x)) - self.angle) % 360
        section = int(relative_angle // 90)
        if section != player.color_idx:
            player.dead = True

# Color Switcher class
class ColorSwitcher:
    def __init__(self, y):
        self.x = WIDTH // 2
        self.y = y
        self.passed = False

    def show(self):
        noStroke()
        for i in range(4):
            fill(colors[i])
            arc(self.x, self.y + yshift, 40, 40, radians(i * 90), radians((i + 1) * 90))

    def check_switch(self, player):
        if not self.passed and dist(player.x, player.y, self.x, self.y) < 30:
            player.color_idx = random.randint(0, 3)
            self.passed = True

# Setup
def setup():
    size(WIDTH, HEIGHT)
    global player, obstacles, switchers, score, gameState
    player = Player()
    obstacles = []
    switchers = []
    score = 0
    gameState = 'cover'

    spawn_y = HEIGHT - 300
    spacing = 400

    for i in range(6):
        obstacles.append(Obstacle(spawn_y))
        switchers.append(ColorSwitcher(spawn_y - spacing / 2))
        spawn_y -= spacing

# Main loop
def draw():
    background(30)

    if gameState == 'cover':
        drawCoverScreen()
    elif gameState == 'playing':
        runGame()
    elif gameState == 'gameover':
        drawGameOver()

# Cover screen with Start button
def drawCoverScreen():
    fill(255)
    textSize(50)
    textAlign(CENTER)
    text("Color Switch", WIDTH // 2, HEIGHT // 2 - 50)
    startBtn.display()

# Main gameplay loop
def runGame():
    global score, switchers, gameState

    player.update()
    player.show()

    for obs in obstacles:
        obs.update()
        obs.show()
        obs.check_collision(player)

    for switch in switchers:
        switch.show()
        switch.check_switch(player)

    # Remove used color switchers
    switchers = [s for s in switchers if not s.passed]

    fill(255, 0, 0)  # Red color
    textSize(32)
    textAlign(RIGHT, TOP)
    text("Score: " + str(score), WIDTH - 20, 20)

    if not player.started and not player.dead:
        textSize(40)
        textAlign(CENTER, CENTER)
        
        msg = "Press UP to Start"
        x = WIDTH // 2 - textWidth(msg) / 2
        y = HEIGHT // 2 - 20
    
        for i, ch in enumerate(msg):
            fill(colors[i % len(colors)])
            text(ch, x + textWidth(msg[:i]), y)

    if player.dead:
        fill(255, 0, 0)
        textSize(50)
        text("Game Over", WIDTH // 2, HEIGHT // 2)
        gameState = 'gameover'

    for obs in obstacles:
        if not obs.scored and player.y + yshift < obs.y:
            score += 1
            obs.scored = True

# Game Over screen (click to restart)
def drawGameOver():
    global gameState
    fill(255, 0, 0)
    textSize(50)
    textAlign(CENTER)
    text("Game Over", WIDTH // 2, HEIGHT // 2 - 20)

    textSize(24)
    fill(255)
    text("Click to Restart", WIDTH // 2, HEIGHT // 2 + 40)

# Controls
def keyPressed():
    global gameState
    if keyCode == UP:
        if gameState == 'playing' and not player.dead:
            player.started = True
            player.jump()

# Mouse click events for button and restart
def mousePressed():
    global gameState
    if gameState == 'cover' and startBtn.isHovered():
        gameState = 'playing'
    elif gameState == 'gameover':
        setup()
        gameState = 'playing'

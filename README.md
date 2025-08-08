# Color Switch – Python (Processing 3)

**Intro to Computer Science Final Project**  
Our own version of the famous game **Color Switch**, implemented in **Python Mode** using **Processing 3**.  
The game features smooth physics-based jumping, rotating obstacles, dynamic color switching, and a scoring system.

## 🎮 Gameplay
- Control a colored ball that must pass through matching color segments of rotating obstacles.
- Collect **Color Switchers** to randomly change your ball's color.
- Avoid mismatched segments — collision with the wrong color ends the game.
- Game states: **Cover Screen → Playing → Game Over**.

---

## 🛠 Technologies & Libraries
- **Processing 3 (Python Mode)** – for graphics and event handling.
- **Minim Audio Library** – for sound effects (`jump.mp3`) and background music.
- **Python Math Functions** – `atan2`, `radians`, `degrees`, `dist` for collision and rotation logic.

---

## ⚙️ Game Physics
The game simulates **vertical motion under constant acceleration** due to gravity.

### Position & Velocity Update:
\[
v_y = v_y + g
\]
\[
y = y + v_y
\]
Where:
- \( v_y \) → vertical velocity  
- \( g = 0.4 \) → gravitational acceleration constant  

### Jump Mechanic:
A jump applies an **instantaneous negative velocity**:
\[
v_y = -8
\]
This simulates an impulse force pushing the ball upward.

---

## 🎨 Collision Detection
We use **polar coordinates** and **relative angles** for obstacle collision:
1. Calculate distance \( d \) between player and obstacle center:
\[
d = \sqrt{(x_p - x_o)^2 + (y_p - y_o)^2}
\]
2. Calculate the **relative angle**:
\[
\theta = \left( \frac{180}{\pi} \cdot \text{atan2}(y_p - y_o, x_p - x_o) - \text{rotationAngle} \right) \mod 360
\]
3. Determine the quadrant (0–3) by:
\[
\text{section} = \lfloor \theta / 90 \rfloor
\]
4. If the quadrant’s color ≠ player's color → **Game Over**.

---

---

## 🚀 How to Run
1. Install **Processing 3**.
2. Switch to **Python Mode** in Processing.
3. Install Minim library:  
   - `Sketch → Import Library → Add Library → Search "Minim"`
4. Place `jump.mp3` and `background.mp3` in the same folder as the `.py` file.
5. Run the sketch in Processing.

---

## 📈 Features
- **Physics-based movement** with gravity and impulse jumps.
- **Rotating arc obstacles** with color-matching mechanics.
- **Multiple game states** for start, play, and restart.
- **Random color assignment** via Color Switcher objects.
- **Score tracking** with on-screen HUD.

---

## 📚 Computer Science Concepts Used
- **OOP**: Player, Obstacle, ColorSwitcher, StartButton classes.
- **Event-driven programming**: Keyboard (`keyPressed`) and mouse (`mousePressed`) handlers.
- **Trigonometry**: Angle calculations for collision detection.
- **Modular arithmetic**: Determining obstacle segment color match.
- **State machines**: Managing transitions between game states.

# 🎲 Dice Rolling Race Game

A feature-rich, two-player dice rolling game built with **Python and Tkinter**. This game offers an interactive, colorful, and animated experience complete with avatars, sound effects, celebration animations, and gameplay logic such as turn-based timers and win detection.

---

## 🚀 Project Highlights

- 🎮 **Interactive GUI** with avatars and animated dice
- ⏱️ **Turn-based 10-second timer** for fast-paced gameplay
- 🖼️ **Custom avatar upload** for each player
- 🎉 **Confetti and trophy animation** when a player wins
- 🔊 **Realistic sound effects** for dice rolls and win celebration
- 📊 **Score graph visualization** using Matplotlib
- 🔁 **Restart option** and **score tracking**
- 🧠 **Python OOP structure** for clean and maintainable code

---

## 🛠️ Technologies Used

| Category     | Tool/Library     |
|--------------|------------------|
| GUI          | Tkinter (Python) |
| Image        | PIL (Pillow)     |
| Audio        | Pygame (for `.mp3`) |
| Plotting     | Matplotlib       |
| Packaging    | PyInstaller      |

---

## 📂 Folder Structure

Dice Rolling Game/
├── Dice_Rolling_Game.py
├── trophy.jpg
├── icons/
│ ├── dice1.jpg ... dice6.jpg
├── Tunes/
│ ├── roll.mp3
│ └── win.mp3
├── README.md
└── dist/
└── Dice_Rolling_Game.exe


---

## 📸 Screenshots

| 🎲 Gameplay | 🏆 Win Animation | 📊 Score Graph |
|------------|------------------|----------------|
| ![Game UI](screenshots/game.png) | ![Trophy](screenshots/win.png) | ![Graph](screenshots/graph.png) |

---

## 🧩 Features Breakdown

### ✅ GUI & Logic
- Turn-based gameplay
- Dice roll animation and logic (rolls again if 6 is rolled)
- 50-point win condition

### ✅ Audio & Visuals
- Roll and win sounds via Pygame
- Confetti animation using Canvas
- Trophy popup with image or fallback emoji

### ✅ Real-Time Countdown
- Each player has 10 seconds per turn
- Auto switch turn if time runs out

### ✅ Avatars
- Upload custom profile pictures (with circular cropping)
- Shown above each player's roll button

---

## ▶️ How to Run

### ✅ Option 1: Python

Make sure you have the required libraries installed:

```bash
pip install pillow matplotlib pygame

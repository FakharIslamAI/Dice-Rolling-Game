#!/usr/bin/env python
# coding: utf-8

# In[137]:


import tkinter as tk
from tkinter import messagebox, filedialog
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageDraw
import pygame
import os

pygame.init()

class DiceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Dice Rolling Race Game")
        self.root.geometry("500x700")

        self.roll_sound_path = os.path.join("Tunes", "roll.mp3")
        self.win_sound_path = os.path.join("Tunes", "win.mp3")

        self.dice_images = {
            i: ImageTk.PhotoImage(Image.open(f"icons/dice{i}.jpg").resize((100, 100))) for i in range(1, 7)
        }

        self.player_names = ["Player 1", "Player 2"]
        self.scores = {self.player_names[0]: 0, self.player_names[1]: 0}
        self.score_history = {self.player_names[0]: [], self.player_names[1]: []}
        self.current_player = self.player_names[0]
        self.avatars = {self.player_names[0]: None, self.player_names[1]: None}
        self.avatar_uploaded = {self.player_names[0]: False, self.player_names[1]: False}
        self.avatar_labels = {}

        tk.Label(root, text="🎲 Dice Rolling Race", font=("Arial", 16)).pack(pady=10)

        name_frame = tk.Frame(root)
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Player 1 Name:").grid(row=0, column=0)
        self.name_entry1 = tk.Entry(name_frame)
        self.name_entry1.grid(row=0, column=1, padx=5)

        tk.Label(name_frame, text="Player 2 Name:").grid(row=1, column=0)
        self.name_entry2 = tk.Entry(name_frame)
        self.name_entry2.grid(row=1, column=1, padx=5)

        tk.Button(name_frame, text="✅ Set Names", command=self.set_names).grid(row=2, column=0, columnspan=2, pady=5)

        self.status_label = tk.Label(root, text="Enter names and upload avatars to begin", font=("Arial", 14))
        self.status_label.pack(pady=5)

        self.timer_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=2)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=2)

        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 12))
        self.score_label.pack(pady=2)

        self.dice_label = tk.Label(root)
        self.dice_label.pack(pady=5)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.roll_button_p1 = tk.Button(self.button_frame, text="🎯 Player 1 Roll", font=("Arial", 12),
                                        command=lambda: self.play_turn(self.player_names[0]))
        self.roll_button_p1.grid(row=0, column=0, padx=10)

        self.roll_button_p2 = tk.Button(self.button_frame, text="🎯 Player 2 Roll", font=("Arial", 12),
                                        command=lambda: self.play_turn(self.player_names[1]))
        self.roll_button_p2.grid(row=0, column=1, padx=10)

        self.roll_button_p1.config(state="disabled")
        self.roll_button_p2.config(state="disabled")

        self.avatar_frame = tk.Frame(root)
        self.avatar_frame.pack(pady=10)

        self.avatar_labels[self.player_names[0]] = tk.Label(self.avatar_frame)
        self.avatar_labels[self.player_names[0]].grid(row=0, column=0, padx=20)

        self.avatar_labels[self.player_names[1]] = tk.Label(self.avatar_frame)
        self.avatar_labels[self.player_names[1]].grid(row=0, column=1, padx=20)

        self.upload_btn1 = tk.Button(self.avatar_frame, text="Upload Avatar 1", command=lambda: self.upload_avatar(self.player_names[0]))
        self.upload_btn1.grid(row=1, column=0)

        self.upload_btn2 = tk.Button(self.avatar_frame, text="Upload Avatar 2", command=lambda: self.upload_avatar(self.player_names[1]))
        self.upload_btn2.grid(row=1, column=1)

        self.utility_frame = tk.Frame(root)
        self.utility_frame.pack(pady=10)

        self.graph_button = tk.Button(self.utility_frame, text="📊 Show Score Graph", font=("Arial", 12), command=self.plot_graph)
        self.graph_button.grid(row=0, column=0, padx=10)

        self.restart_button = tk.Button(self.utility_frame, text="🔁 Restart Game", font=("Arial", 12), command=self.restart_game)
        self.restart_button.grid(row=0, column=1, padx=10)

        self.timer_id = None

    def set_names(self):
        name1 = self.name_entry1.get().strip()
        name2 = self.name_entry2.get().strip()

        if not name1 or not name2:
            messagebox.showerror("Error", "Please enter names for both players.")
            return

        old_scores = self.scores
        old_history = self.score_history
        old_avatars = self.avatars
        old_current = self.current_player

        self.player_names = [name1, name2]
        self.scores = {name1: old_scores.get("Player 1", 0), name2: old_scores.get("Player 2", 0)}
        self.score_history = {name1: old_history.get("Player 1", []), name2: old_history.get("Player 2", [])}
        self.avatars = {name1: old_avatars.get("Player 1"), name2: old_avatars.get("Player 2")}
        self.avatar_uploaded = {name1: False, name2: False}
        self.current_player = name1 if old_current == "Player 1" else name2

        for widget in self.avatar_frame.winfo_children():
            widget.destroy()

        self.avatar_labels = {}
        self.avatar_labels[name1] = tk.Label(self.avatar_frame)
        self.avatar_labels[name1].grid(row=0, column=0, padx=20)
        self.avatar_labels[name2] = tk.Label(self.avatar_frame)
        self.avatar_labels[name2].grid(row=0, column=1, padx=20)

        self.upload_btn1 = tk.Button(self.avatar_frame, text="Upload Avatar 1", command=lambda: self.upload_avatar(name1))
        self.upload_btn1.grid(row=1, column=0)

        self.upload_btn2 = tk.Button(self.avatar_frame, text="Upload Avatar 2", command=lambda: self.upload_avatar(name2))
        self.upload_btn2.grid(row=1, column=1)

        for player in self.player_names:
            if self.avatars[player]:
                self.avatar_labels[player].config(image=self.avatars[player])
                self.avatar_labels[player].image = self.avatars[player]

        self.score_label.config(text=self.get_score_text())
        self.status_label.config(text=f"{self.current_player}'s Turn")
        self.roll_button_p1.config(text=f"🎯 {self.player_names[0]} Roll", command=lambda: self.play_turn(self.player_names[0]))
        self.roll_button_p2.config(text=f"🎯 {self.player_names[1]} Roll", command=lambda: self.play_turn(self.player_names[1]))
        self.update_buttons()

    def upload_avatar(self, player):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            img = Image.open(file_path).resize((80, 80))
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 80, 80), fill=255)
            img.putalpha(mask)
            circular = Image.new("RGBA", img.size)
            circular.paste(img, (0, 0), mask=img)
            photo = ImageTk.PhotoImage(circular)
            self.avatars[player] = photo
            self.avatar_labels[player].config(image=photo)
            self.avatar_labels[player].image = photo

            self.avatar_uploaded[player] = True

            # Only start game if both avatars uploaded and timer not started
            if all(self.avatar_uploaded.values()) and not self.timer_id:
                self.start_timer()

    def start_timer(self):
        self.time_left = 10
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"⏱️ Time Left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("⏱️ Time's Up!", f"{self.current_player} ran out of time!")
            self.current_player = self.player_names[1] if self.current_player == self.player_names[0] else self.player_names[0]
            self.status_label.config(text=f"{self.current_player}'s Turn")
            self.update_buttons()
            self.start_timer()

    # (Keep your other methods: play_turn, update_buttons, play_sound, show_trophy_popup, show_confetti, etc.)

    # Add your play_turn, restart_game, plot_graph, show_trophy_popup, show_confetti here (unchanged from previous code)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceGame(root)
    root.mainloop()


# In[ ]:





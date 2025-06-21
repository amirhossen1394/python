import tkinter as tk
import random

class GholakhGuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 حدس عدد با ممد اوشگول")
        self.root.geometry("500x400")
        self.root.configure(bg="black")

        self.number = random.randint(1, 20)
        self.tries = 5

        self.title = tk.Label(root, text="🕶️ ممد اوشگول میگه: یه عدد بین 1 تا 20 تو ذهنمه!",
                              font=("B Titr", 14), fg="red", bg="black")
        self.title.pack(pady=10)

        self.entry = tk.Entry(root, font=("Courier", 14), justify="center")
        self.entry.pack(pady=10)

        self.button = tk.Button(root, text="حدس بزن!", font=("B Titr", 12),
                                bg="lime", fg="black", command=self.check_guess)
        self.button.pack(pady=10)

        self.result = tk.Label(root, text="", font=("B Titr", 13),
                               fg="orange", bg="black", wraplength=400)
        self.result.pack(pady=10)

        self.tries_label = tk.Label(root, text=f"شانس‌های باقی‌مونده: {self.tries}",
                                    font=("Courier", 12), fg="white", bg="black")
        self.tries_label.pack(pady=5)

    def gholakh_speak(self, msg):
        self.result.config(text=f"🕶️ {msg}")

    def get_hint(self, guess):
        diff = abs(guess - self.number)
        if diff == 0:
            return "خودشه داش! گل کاشتی 😎"
        elif diff <= 2:
            return "خیلی داغی داش! نزدیکِ نزدیک!"
        elif diff <= 5:

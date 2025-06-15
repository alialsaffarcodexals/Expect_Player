import tkinter as tk
from urllib.request import urlopen
from io import BytesIO
from typing import List, Dict

from PIL import Image, ImageTk

from .data import players
from .game import unique_values


class GameGUI:
    """Graphical interface for the Expect Player game."""

    def __init__(self, players: List[Dict]):
        self.possible_players = players[:]
        self.attributes = ["nationality", "club", "position"]
        self.attr_index = 0
        self.value_index = 0
        self.current_values = unique_values(self.possible_players, self.attributes[self.attr_index])

        self.root = tk.Tk()
        self.root.title("Expect Player")
        self.root.configure(bg="#222222")
        self.root.geometry("800x600")
        self.font = ("Helvetica", 16)

        self.question = tk.Label(self.root, text="", fg="white", bg="#222222", font=self.font, wraplength=760)
        self.question.pack(pady=40)

        btn_frame = tk.Frame(self.root, bg="#222222")
        btn_frame.pack()
        self.yes_btn = tk.Button(btn_frame, text="Yes", font=self.font, width=10, command=lambda: self.answer(True))
        self.yes_btn.grid(row=0, column=0, padx=20)
        self.no_btn = tk.Button(btn_frame, text="No", font=self.font, width=10, command=lambda: self.answer(False))
        self.no_btn.grid(row=0, column=1, padx=20)

        self.ask_next()

    def ask_next(self) -> None:
        if len(self.possible_players) == 1 or self.attr_index >= len(self.attributes):
            self.show_result()
            return

        attr = self.attributes[self.attr_index]
        if self.value_index >= len(self.current_values):
            self.attr_index += 1
            if self.attr_index >= len(self.attributes):
                self.show_result()
                return
            self.current_values = unique_values(self.possible_players, self.attributes[self.attr_index])
            self.value_index = 0
            attr = self.attributes[self.attr_index]

        value = self.current_values[self.value_index]
        self.question.config(text=f"Is your player's {attr} {value}?")

    def answer(self, keep: bool) -> None:
        attr = self.attributes[self.attr_index]
        value = self.current_values[self.value_index]
        if keep:
            self.possible_players = [p for p in self.possible_players if p.get(attr) == value]
        else:
            self.possible_players = [p for p in self.possible_players if p.get(attr) != value]
        self.value_index += 1
        self.ask_next()

    def show_result(self) -> None:
        self.yes_btn.destroy()
        self.no_btn.destroy()
        if self.possible_players:
            player = self.possible_players[0]
            self.question.config(text=f"Your player is {player['name']}!", font=self.font)
            try:
                with urlopen(player['photo']) as resp:
                    img_data = resp.read()
                image = Image.open(BytesIO(img_data))
                image = image.resize((200, 200))
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(self.root, image=photo, bg="#222222")
                img_label.image = photo  # keep reference
                img_label.pack(pady=20)
            except Exception:
                pass
        else:
            self.question.config(text="I couldn't guess your player.")

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    GameGUI(players).run()


if __name__ == "__main__":
    main()

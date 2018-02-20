import tkinter as tk
import pickle
import os.path
from tkinter import filedialog, messagebox

sb_blue = "#07C0F5"
lighter_blue = "#A2E9Fd"

class TTTPlayer:
    score_index = {"WIN": 0, "LOSE": 1, "DRAW": 2}

    def __init__(self):
        self.name = ""
        self.mark_file = ""
        self.scores = [0, 0, 0]


class TTTPlayersManager:

    def __init__(self, players_list=None):
        self.save_file = "C:\\py\\tictac\\players.pk1"
        self.mark_dir = "C:\\py\\tictac"
        self.players = []
        if players_list is None:
            self.load_players()
        else:
            self.players = players_list

        self.root = None
        self.mark_entry = None
        self.name_entry = None

    def save_players(self):
        with open(self.save_file, "wb") as out_file:
            pklr = pickle.Pickler(out_file, -1)
            pklr.dump(self.players)

    def load_players(self):
        with open(self.save_file, "rb") as out_file:
            self.players = pickle.load(out_file)

    def add_player(self):
        #  GUI info
        self.root = tk.Tk()
        self.root.minsize(width=330, height=160)
        self.root.config(bg=sb_blue)
        name_label = tk.Label(master=self.root, text="Write your player name:", bg=sb_blue)
        self.name_entry = tk.Entry(master=self.root, bg=lighter_blue)
        self.name_entry.insert(0, "Player 1")

        mark_label = tk.Label(master=self.root, text="Choose a 40x40 .gif file as your mark  ", bg=sb_blue)
        self.mark_entry = tk.Entry(master=self.root, bg=lighter_blue)
        self.mark_entry.insert(0, "C:\\py\\tictac\\x_red.gif")
        mark_button = tk.Button(master=self.root, command=self._browse_marks, text="Browse", bg=lighter_blue)
        process_button = tk.Button(master=self.root, command=self._process_add_player, text="Add Player",
                                   bg=lighter_blue)

        name_label.grid(row=0, column=0, sticky=tk.W)
        self.name_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)
        mark_label.grid(row=2, column=0, sticky=tk.W)
        mark_button.grid(row=2, column=1, sticky=tk.E)
        self.mark_entry.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E)
        process_button.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E)
        self.root.mainloop()

    def _browse_marks(self):
        self.root.filename = filedialog.askopenfilename(initialdir=self.mark_dir,
                                                        title='Choose a 40x40 .gif file as your mar',
                                                        filetypes=(('gif files', '*.gif'), ('all files', '*.*')))
        # if we don't get a filename just bail
        if self.root.filename:
            self.mark_entry.delete(0, tk.END)
            self.mark_entry.insert(0, self.root.filename)
        else:
            pass

    def _process_add_player(self):

        mark_file = self.mark_entry.get()
        name = self.name_entry.get()
        existing_names = []
        for player in self.players:
            existing_names.append(player.name)

        if name is None or name == "":
            messagebox.showerror("Name Error", "You must enter a name")
        elif name in existing_names:
            messagebox.showerror("Name Error", "Name already exists")
        elif not os.path.exists(mark_file):
            messagebox.showerror("Mark Error", "Choose a valid mark file")
        else:
            new_player = TTTPlayer()
            new_player.name = name
            new_player.mark_file = mark_file
            self.players.append(new_player)
            self.root.destroy()
            self.save_players()

    def get_mark(self, index):
        mark = self.players[index].mark_file
        return mark

    def get_name(self, index):
        name = self.players[index].name
        return name

    def get_scores(self, index):
        scores = self.players[index].scores
        return scores

    def add_score(self, index, score_kind):
        pass # TODO


class TicTacToe:

    def __init__(self):
        #  GUI info
        #  Parameters
        self.grid_x = 50
        self.grid_y = 50
        #  TTT Board
        self.root = tk.Tk()
        self.root.config(bg=sb_blue)
        self.root.minsize(self.grid_x + 300, self.grid_y + 180)
        self.grid = tk.PhotoImage(file="C:\\py\\tictac\\grid.gif")
        self.grid_label = tk.Label(master=self.root, image=self.grid, padx=10, pady=10)
        #  self.grid_label.bind("<Button-1>", self.place_player_mark)
        #  self.grid_label.bind("<Button-3>", self.place_enemy_mark)
        self.grid_label.bind("<Button-1>", self._place_mark)
        self.grid_label.place(x=self.grid_x, y=self.grid_y)
        #  Buttons
        self.reset_button = tk.Button(master=self.root, command=self.reset, text="RESET", bg=lighter_blue)
        self.reset_button.place(x=self.grid_x + 200, y=self.grid_y + 30)
        #  Menus
        master_menu = tk.Menu(self.root, bg=sb_blue)
        self.root.config(menu=master_menu)
        player_menu = tk.Menu(master_menu, bg=lighter_blue)
        master_menu.add_cascade(menu=player_menu, label="Player Configuration")
        player_menu.add_command(label="RESET", command=self.reset)
        player_menu.add_separator()
        player_menu.add_command(label="Edit Player Config", command=lambda: print("config"))

        #  Player customizable info
        self.pm = TTTPlayersManager()
        self.player_index = 0
        self.enemy_index = 1

        #  Game info
        self.marks = []
        self.positions = ["?", "?", "?", "?", "?", "?", "?", "?", "?"]
        self.running = True
        self.is_player = True

    def place_player_mark(self, event):
        self._place_mark(event, True)

    def place_enemy_mark(self, event):
        self._place_mark(event, False)

    def _place_mark(self, event, is_player=None):
        x, y, pos = self.get_square(event.x, event.y)
        if self.running:
            if self.is_player:
                mark = tk.PhotoImage(file=self.pm.get_mark(self.player_index))
                self.positions[pos] = self.pm.get_name(self.player_index)
            else:
                mark = tk.PhotoImage(file=self.pm.get_mark(self.enemy_index))
                self.positions[pos] = self.pm.get_name(self.enemy_index)

            new_label = tk.Label(master=self.root, image=mark)
            new_label.place(x=x, y=y)
            self.marks.append(new_label)
            self.marks.append(mark) # Can't lose reference to image or it won't display
            self.root.update()
            self.is_player = not self.is_player

    def reset(self):
        for mark in self.marks:
            try:
                mark.destroy() # For tk Labels
            except AttributeError:
                del mark # For tk PhotoImages
        self.marks = []
        self.root.update()

        self.positions = ["?", "?", "?", "?", "?", "?", "?", "?", "?"]
        self.running = True

    def check_win(self):
        winner = (False, "")
        for index in [0, 1, 2]:
            if (self.positions[index] == self.positions[index + 3] == self.positions[index + 6]
                    and self.positions[index] != "?"):
                winner = (True, self.positions[index])
        for index in [0, 3, 6]:
            if (self.positions[index] == self.positions[index + 1] == self.positions[index + 2]
                    and self.positions[index] != "?"):
                winner = (True, self.positions[index])
        if (self.positions[0] == self.positions[4] == self.positions[8]
                and self.positions[0] != "?"):
            winner = (True, self.positions[0])
        if (self.positions[2] == self.positions[4] == self.positions[6]
                and self.positions[2] != "?"):
            winner = (True, self.positions[2])

        return winner

    def run(self):
        if self.running:
            game_won, winner = self.check_win()
            if game_won:
                print(winner + " wins!")
                self.running = False
            elif len(self.marks) > 16:
                print("Stalemate :(")
                self.running = False
        self.root.after(300, self.run)

    def get_square(self, x, y):
        #  0 | 1 | 2
        # -----------
        #  3 | 4 | 5
        # -----------
        #  6 | 7 | 8

        y_bar_1 = 53
        y_bar_2 = 106
        x_bar_1 = 48
        x_bar_2 = 100

        if x < x_bar_1:
            if y < y_bar_1:
                pos = 0
            elif y < y_bar_2:
                pos = 3
            else:
                pos = 6
        elif x < x_bar_2:
            if y < y_bar_1:
                pos = 1
            elif y < y_bar_2:
                pos = 4
            else:
                pos = 7
        else:
            if y < y_bar_1:
                pos = 2
            elif y < y_bar_2:
                pos = 5
            else:
                pos = 8

        if pos in [0, 3, 6]:
            pos_x = self.grid_x + 2
        elif pos in [1, 4, 7]:
            pos_x = self.grid_x + 52
        else:
            pos_x = self.grid_x + 104

        if pos in [0, 1, 2]:
            pos_y = self.grid_y + 4
        elif pos in [3, 4, 5]:
            pos_y = self.grid_y + 56
        else:
            pos_y = self.grid_y + 106

        return pos_x, pos_y, pos


def main():
    game = TicTacToe()
    game.run()
    game.root.mainloop()


def test():

    pm = TTTPlayersManager()
    pm.add_player()

if __name__ == "__main__":
    main()

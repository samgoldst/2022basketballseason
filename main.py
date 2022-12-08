"""https://server.thecoderschool.com/appgallery/super.php"""

from __future__ import annotations

import copy
import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np


class Game:
    def __init__(self, game_data: list[str]):
        self.team, self.opponent, self.date, self.outcome = game_data[:4]
        self.min, self.pts, self.fgm, self.fga, self.fgp, self.tpm, self.tpa, self.tpp, self.ftm, self.fta, self.ftp, \
            self.oreb, self.dreb, self.reb, self.ast, self.stl, self.blk, self.tov, self.pf, self.pm = [
                float(i) for i in game_data[4:]]
        self.opts = self.pts - self.pm
        self.advscore = (self.pts * (self.pts + self.reb + self.ast) / (2 * (self.fga + (.44 * self.fta))))
        if self.outcome == "W":  self.win = 1
        else: self.win = 0

    def toString(self) -> str:
        return str(vars(self).values())

    def getId(self) -> str:
        return self.team + ' ' + self.opponent+ " " + self.date


class Season:
    def __init__(self, games: list[list[str]] | list[Game] | None):
        if games is None:
            self.games: list[Game] = []
        elif type(games[0]) == list:
            self.games: list[Game] = [Game(game) for game in games]
        elif type(games[0]) == Game:
            self.games: list[Game] = games
        else:
            raise TypeError

    def filter(self, stat: str, minimum: float, comparison: str = "greater"):
        if type(minimum) is str:
            try:
                minimum = float(minimum)
            except ValueError:
                raise Exception(f"{minimum} cannot be converted to float")
        output: list[Game] = []
        if comparison == "greater":
            for game in self.games:
                if game.__getattribute__(stat) > minimum:
                    output.append(game)
        elif comparison == "lower":
            for game in self.games:
                if game.__getattribute__(stat) < minimum:
                    output.append(game)
        return Season([copy.deepcopy(game) for game in output])

    def multi_filter(self, filters: list[tuple[str, float, str]]):
        output: Season = Season([copy.deepcopy(game) for game in self.games])
        for stat, minimum, comparison in filters:
            output = output.filter(stat, minimum, comparison)
        return output

    def out(self):
        output = ""
        for game in self.games:
            output += str(game.toString())[12:-1] + "\n"
        print(output)

    def save(self, filename: str):
        output = []
        for game in self.games:
            output.append(list(vars(game).values())[:-3])
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            for g in output:
                writer.writerow(g)

    def len(self):
        return len(self.games)

    def add_game(self, game: Game):
        self.games.append(game)
        return self

    def delete_game(self, target: str):
        for num, game in enumerate(self.games):
            if game.getId() == target:
                self.games.pop(num)
        return self

    def edit_stat(self, target: str, stat: str, value: float | str):
        for num, game in enumerate(self.games):
            if game.getId() == target:
                if type(getattr(game, stat)) is float:
                    try:
                        value = float(value)
                    except ValueError:
                        raise Exception(f"{value} cannot be converted to float")
                setattr(game, stat, value)
        return self

    def load(self, file: str):
        with open(file) as data:
            for a in csv.reader(data, delimiter='\t'):
                self.games.append(Game(a))
        return self

    def reset(self):
        self.games.clear()

    def find(self, stat: str, value):
        output = Season(None)
        value = str(value)
        for game in self.games:
            if value in str(game.__getattribute__(stat)):
                output.add_game(game)
        return output

    def winPercentage(self):
        total = self.len()
        if total == 0:
            return "NO GAMES EXIST"
        wins = 0.0
        for game in self.games:
            if game.outcome == "W":
                wins += 1
        return wins/total

    def average(self, stat: str):
        num_games = self.len()
        if num_games == 0:
            return "NO GAMES EXIST"
        stat_total = 0.0
        for game in self.games:
            stat_total += game.__getattribute__(stat)
        return stat_total/num_games

    def sort(self, stat: str, descending: bool | str = True):
        if type(descending) == str:
            if descending.lower() == "true":
                descending = True
            elif descending.lower() == "false":
                descending = False
            else:
                raise Exception("string is not true or false")
        return Season(sorted(self.games, key=(lambda g: g.__getattribute__(stat)), reverse=descending))

    def plot(self, stat1: str, stat2: str | None):
        m1 = min([game.__getattribute__(stat1) for game in self.games])
        w = int(max([game.__getattribute__(stat1) for game in self.games]) + .5)
        if type(stat2) == str:
            m2 = min([game.__getattribute__(stat2) for game in self.games])
            h = int(max([game.__getattribute__(stat2) for game in self.games]) + .5)
            grid = np.zeros((h, w, 3))
            for game in self.games:
                grid[int(game.__getattribute__(stat2) - 1), int(game.__getattribute__(stat1) - 1), int(game.__getattribute__("win"))] += 1
        else:
            grid = np.zeros((1, w, 3))
            for game in self.games:
                grid[0, int(game.__getattribute__(stat1) - 1), int(game.__getattribute__("win"))] += 1
        plt.imshow(grid / np.max(grid), origin="lower")
        plt.suptitle(f"{stat2} vs. {stat1}")
        plt.show()

    def mode(self, stat: str):
        if stat == "id":
            list = [game.getId() for game in self.games]
        else:
            list = [game.__getattribute__(stat) for game in self.games]
        most = max(set(list), key=list.count)
        return str(most) + ": " + str(list.count(most))

    def show(self):
        gui(self)

def gui(season: Season):
    root = tk.Tk()
    root.geometry("400x400")
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    sbx = ttk.Scrollbar(frame, orient="horizontal")
    sby = ttk.Scrollbar(frame)
    sbx.pack(side=tk.BOTTOM, fill=tk.X)
    sby.pack(side=tk.RIGHT, fill=tk.Y)
    tv = ttk.Treeview(frame, yscrollcommand=sby.set, xscrollcommand=sbx.set)
    sbx.config(command=tv.xview)
    sby.config(command=tv.yview)
    tv["columns"] = ("team", "opponent", "date", "w/l", "min", "pts", "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm",
                     "fta", "ftp", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "pf", "+/-", "opts", "advscore")
    for stat in tv["columns"]:
        tv.column(stat, width=80, anchor=tk.CENTER)
    tv.column("#0", width=0, stretch=tk.NO)
    tv.heading("#0", text="", anchor=tk.CENTER)
    for stat in tv["columns"]:
        tv.heading(stat, text=stat, anchor=tk.CENTER)
    for index, game in enumerate(season.games):
        tv.insert(parent="", index="end", iid=str(index), text="", values=tuple([str(i) for i in vars(game).values()]))
    tv.pack(fill="both", expand=True)
    root.mainloop()

season = Season(None).load("season.csv")

season.show()
season.plot("pts", "ast")

while True:
    full_input = input("> ").strip()
    command = full_input.split(" ")[0]
    args = full_input.split(" ")[1:]
    new_season = season.__getattribute__(command)(*args)
    if type(new_season) == Season:
        season = new_season
    elif new_season is not None:
        print(new_season)
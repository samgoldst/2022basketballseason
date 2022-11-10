"""https://server.thecoderschool.com/appgallery/super.php"""

from __future__ import annotations
import copy
import csv


class Game:
    def __init__(self, game_data: list[str]):
        self.team, self.opponent, self.date, self.outcome = game_data[:4]
        self.min, self.pts, self.fgm, self.fga, self.fgp, self.tpm, self.tpa, self.tpp, self.ftm, self.fta, self.ftp, \
            self.oreb, self.dreb, self.reb, self.ast, self.stl, self.blk, self.tov, self.pf, self.pm = [
                float(i) for i in game_data[4:]]

    def toString(self) -> str:
        return str(vars(self).values())

    def getId(self) -> str:
        return self.team + ' ' + self.date


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

    def filter(self, stat: str, minimum: float, comparison: str):
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
            output.append(list(vars(game).values()))
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
                setattr(game, stat, value)
        return self

    def load(self, file: str):
        with open(file) as data:
            for a in csv.reader(data, delimiter='\t'):
                self.games.append(Game(a))
        return self

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



#regular filter
Season(None).load("season.csv").multi_filter([("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

#find by points, outcome
Season(None).load("season.csv").find("pts", "120").find("outcome", "L").out()

# delete game
Season(None).load("season.csv").delete_game("HOU 12/20/21").multi_filter(
    [("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

# add game
newGame = Game(
    "UTA	OKC	04/06/22	W	100	100	100	100	100	100	100	100	100	100	100	100	39	55	29	7	10	13	13	-10".split(
        "\t"))
Season(None).load("season.csv").add_game(newGame).multi_filter([("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

# edit stat
Season(None).load("season.csv").add_game(newGame).edit_stat("UTA 04/06/22", "fgm", 10000.0).multi_filter(
    [("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

# save to file
Season(None).load("season.csv").add_game(newGame).edit_stat("UTA 04/06/22", "fgm", 10000.0).multi_filter(
    [("fgp", 55, "greater"), ("pm", 0, "lower")]).save("output.csv")

#get average
print(Season(None).load("season.csv").find("outcome", "W").average("pts"), "\n")

#get win percentage of teams in games where there points contained the digit 2
print(Season(None).load("season.csv").find("pts", "2").winPercentage(), "\n")
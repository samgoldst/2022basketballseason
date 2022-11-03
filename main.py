"""https://server.thecoderschool.com/appgallery/super.php"""

from __future__ import annotations
import copy
import csv

class Game:
    def __init__(self, game_data: list[str]):
        self.team, self.opponent, self.date, self.outcome = game_data[:4]
        self.min, self.pts, self.fgm, self.fga, self.fgp, self.tpm, self.tpa, self.tpp, self.ftm, self.fta, self.ftp, self.oreb, self.dreb, self.reb, self.ast, self.stl, self.blk, self.tov, self.pf, self.pm = [float(i) for i in game_data[4:]]

    def toString(self):
        return vars(self).values()

    def getId(self):
        return self.team + ' ' + self.date

class Season:
    def __init__(self, games: list[list[str]] | list[Game]):
        if type(games[0]) == list:
            self.games = [Game(game) for game in games]
        else:
            self.games = games

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


'''DOESNT WORK YET'''

    def save(self, filename: str):
        output = []
        for game in self.games:
            output.append(str(game.toString())[12:-1])
        with open(filename, "w") as file:
            writer = csv.writer(file, delimiter='\t')
            for g in output:
                writer.writerows(output)

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

with open("season.csv") as data:
    games = [a for a in csv.reader(data, delimiter='\t')]

    Season(games).multi_filter([("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

    #delete game
    Season(games).delete_game("HOU 12/20/21").multi_filter([("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

    #add game
    newGame = Game("UTA	OKC	04/06/22	W	100	100	100	100	100	100	100	100	100	100	100	100	39	55	29	7	10	13	13	-10".split("\t"))
    Season(games).add_game(newGame).multi_filter([("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

    #edit game
    Season(games).add_game(newGame).edit_stat("UTA 04/06/22", "fgm", 10000.0).multi_filter([("fgp", 55, "greater"), ("pm", 0, "lower")]).out()

    #save game DOESN'T WORK YET
    Season(games).add_game(newGame).edit_stat("UTA 04/06/22", "fgm", 10000.0).multi_filter([("fgp", 55, "greater"), ("pm", 0, "lower")]).save("output.csv")


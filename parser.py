from bs4 import BeautifulSoup
import requests


# Game is a container for a single game data
class Game(object):
    stats = ['points', 'minutes', 'fouls', 'fouled', '2points made',
             '2s attempts', '3s made', '3s attempts', 'free throws made',
             'free throws attempts', 'offensive rebounds',
             'defensive rebounds', 'blocks made', 'blocked', 'turnovers',
             'steals', 'assists', 'OER', 'plusminus']

    def __init__(self, team_A, team_B):
        self.teams = [team_A, team_B]
        self.players = [dict(), dict()]
        self.points = [0, 0]

    def check_row(row):
        l = len(row)
        if l != len(Game.stats):
            return False
        for i, el in enumerate(row):
            # plusminus could be negative
            if i < (l - 1) and el < 0:
                return False
        return True

    def set_player(self, name, team, row):
        if not Game.check_row(row):
            return
        t = 0 if team == self.teams[0] else 1
        self.players[t][name] = row[:]


class Parser:

    """ parse_game parses a single match and produces
    a Game object containing all the data. """
    def parse_game(link, team_A, team_B):

        # TODO: handle exceptions
        r = requests.get(link)
        soup = BeautifulSoup(r.text)
        game = Game(team_A, team_B)
        tables = soup.find_all("table")
        teamA_table = tables[9]
        teamB_table = tables[10]
        players_A = teamA_table.find_all("tr")
        players_B = teamB_table.find_all("tr")
        for i in range(2, len(players_A) - 1):
            raw_stats = players_A[i].find_all("td")
            name = raw_stats[2].get_text().strip()
            row = Parser.parse_row(raw_stats[3:])
            game.set_player(name, team_A, row)

        for i in range(2, len(players_B) - 1):
            raw_stats = players_B[i].find_all("td")
            name = raw_stats[2].get_text().strip()
            row = Parser.parse_row(raw_stats[3:])
            game.set_player(name, team_B, row)

        return game

    def parse_row(raw_row):
        stats = []
        # j = 0
        # ignore all the useless stats
        to_ignore = [6, 7, 10, 13, 16, 22]
        for i, el in enumerate(raw_row):
            if i in to_ignore:
                continue
            try:
                clean_el = float(el.get_text().strip())
            except ValueError:
                print(el.get_text())
            stats.append(clean_el)
        return stats

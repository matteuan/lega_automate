from bs4 import BeautifulSoup
import requests


# Game is a container for a single game data
class Game(object):

    def __init__(self, team_A, team_B):
        self.teams = [team_A, team_B]
        self.players = [dict(), dict()]
        self.points = [0, 0]

    def set_player(self, name, team, row):
        t = 0 if team == self.teams[0] else 1
        self.players[t][name] = row[:]


class Parser:

    """ parse_game parses a single match and produces
    a Game object containing all the data. """
    def parse_game(link):

        # TODO: handle exceptions
        r = requests.get(link)
        soup = BeautifulSoup(r.text())
        # I should already know the name of the teams
        name_A = "pippo"
        name_B = "paperino"
        game = Game(name_A, name_B)
        # iterate over looking for data and set players stats
        return game

from bs4 import BeautifulSoup
import requests
import sys


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
            raise Exception("Not a valid stat row")
        t = 0 if team == self.teams[0] else 1
        self.players[t][name] = row[:]
        self.points[t] += row[0]

    # csv-like representation
    def __str__(self):
        lines = []

        lines.append(self.teams[0] + ", " + str(self.points[0]))
        for name, stats in self.players[0].items():
            lines.append(name + ", " + ", ".join(map(str, stats)))

        lines.append(self.teams[1] + ", " + str(self.points[1]))
        for name, stats in self.players[1].items():
            lines.append(name + ", " + ", ".join(map(str, stats)))

        return "\n".join(lines)


class Parser:

    """ parse_game parses a single match and produces
    a Game object containing all the data. """
    def parse_game(link, team_A, team_B):

        # TODO: handle exceptions, maybe to implement above
        r = requests.get(link)
        soup = BeautifulSoup(r.text.encode('utf8'))
        game = Game(team_A, team_B)
        tables = soup.find_all("table")

        players_A = tables[9].find_all("tr")
        for i in range(2, len(players_A) - 2):
            raw_stats = players_A[i].find_all("td")
            name = raw_stats[2].get_text().strip().replace('\xa0', ' ')
            row = Parser.parse_row(raw_stats[3:])
            game.set_player(name, team_A, row)

        players_B = tables[10].find_all("tr")
        for i in range(2, len(players_B) - 2):
            raw_stats = players_B[i].find_all("td")
            name = raw_stats[2].get_text().strip().replace('\xa0', ' ')
            row = Parser.parse_row(raw_stats[3:])
            game.set_player(name, team_B, row)

        return game

    """ parse_row parses a single row in a single match table
    """
    def parse_row(raw_row):
        stats = []
        # ignore all the useless stats
        to_ignore = [6, 7, 10, 13, 16, 22]
        for i, el in enumerate(raw_row):
            if i in to_ignore:
                continue
            try:
                clean_el = el.get_text().strip()
                num = 0.0 if not clean_el else float(clean_el)
            except ValueError:
                print("This is not a number: " + el.get_text())
            stats.append(num)
        return stats

    """ parse_gamestand parses a page like http://195.56.77.208/stand
        and it calls all the links, returning data from each match. """
    def parse_gamestand(link):
        r = requests.get(link)
        soup = BeautifulSoup(r.text.encode('utf8'))
        raw_matches = soup.find_all("table")[7].find_all("tr")
        raw_matches = raw_matches[2:]
        matches = []
        for i in range(0, len(raw_matches), 2):
            a = raw_matches[i].find_all("a")
            b = raw_matches[i + 1].find_all("a")
            team_A = a[0].text.replace('\xa0', ' ')
            team_B = b[0].text.replace('\xa0', ' ')
            link = a[1].attrs['href']
            matches.append(Parser.parse_game(link, team_A, team_B))
            print("Succesfully parsed: {A} vs {B}".format(A=team_A, B=team_B))

        return matches


def main():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " [link]")
    link = sys.argv[1]

    # TODO: regex to check the link
    matches = Parser.parse_gamestand(link)
    print(matches[0])

if __name__ == "__main__":
    main()

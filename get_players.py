""" get_players retrieve all the players and fill the players table.
It is a one time script."""
from bs4 import BeautifulSoup
from threading import Thread
import requests
import sys
import sqlite3

team_to_id = dict()
team_to_id[""] = 0

def set_team_ids(db_file):
    conn = sqlite3.connect(db_file)
    for team_id, name in conn.execute("SELECT * FROM teams"):
        team_to_id[name] = team_id
    conn.close()

class SinglePlayer(Thread):

    def __init__(self, name, link, db_file):
        Thread.__init__(self)
        self.name = name
        self.link =  link
        self.db = db_file

    def run(self):
        r = requests.get(self.link)
        soup = BeautifulSoup(r.text)
        team = soup.find("a", class_="w tdn").getText()
        if not team in team_to_id:
            print("Warning: {} not found".format(team))
            return
        team = team_to_id[team]
        trs = soup.find_all("tr")
        height = trs[9].find_all("td")[3].text.split(" ")[0].strip()
        weight = trs[10].find_all("td")[3].text.split(" ")[0].strip()
        birthday = trs[10].find_all("td")[1].text.strip()
        write_database(self.db, [self.name, height, weight, birthday, team])
        print("Parsed {}".format(self.name))

def parse_players(link, db_file):
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    raw_players = soup.findAll("a", class_="sch_ris")
    for pl in raw_players:
        name = pl.get_text().replace('\xa0', ' ')
        th = SinglePlayer(name, pl["href"], db_file)
        th.start()
        # players.append(parse_single_player(name, pl["href"]))

def write_database(db_file, player):
    conn = sqlite3.connect(db_file)

    conn.execute('INSERT INTO players VALUES ' +
                 '(NULL, "{}","{}","{}","{}", "{}", "0.0")'.
                 format(*player))

    conn.commit()
    conn.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " [db_file] [link]")
        return
    link = sys.argv[2]
    db_file = sys.argv[1]
    set_team_ids(db_file)
    parse_players(link, db_file)

if __name__ == "__main__":
    main()

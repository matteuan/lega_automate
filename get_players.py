""" get_players retrieve all the players and fill the players table.
It is a one time script."""
from bs4 import BeautifulSoup
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


def parse_single_player(name, link):
    r = requests.get(link)
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
    return [name, height, weight, birthday, team]


def parse_players(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    raw_players = soup.findAll("a", class_="sch_ris")
    players = []
    for pl in raw_players:
        name = pl.get_text().replace('\xa0', ' ')
        players.append(parse_single_player(name, pl["href"]))
        print("Succesfuly parsed {}".format(name))
    return players


def write_database(db_file, players):
    conn = sqlite3.connect(db_file)
    p_id = 1
    for player_info in players:
        player_info = [str(p_id)] + player_info
        p_id += 1
        conn.execute('INSERT INTO players VALUES ' +
                     '("{}","{}","{}","{}","{}", "{}", "0.0")'.
                     format(*player_info))

    conn.commit()
    conn.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " [db_file] [link]")
        return
    link = sys.argv[2]
    db_file = sys.argv[1]
    set_team_ids(db_file)

    players = parse_players(link)
    write_database(db_file, players)

if __name__ == "__main__":
    main()

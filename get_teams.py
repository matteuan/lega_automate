""" get_players retrieve all teams and fill the teams table.
It is a one time script. Typical link is http://195.56.77.208/team/"""
from bs4 import BeautifulSoup
import requests
import sys
import sqlite3


def parse_teams(link):
    team_to_id = dict()
    team_to_id[""] = 0

    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")

    raw_teams = soup.findAll("a", class_="sch_ris ds_black")
    max_idx = team_to_id[max(team_to_id, key=team_to_id.get)]
    for r_team in raw_teams:
        name =  r_team.text
        if not name in team_to_id:
            max_idx += 1
            team_to_id[name] = max_idx
    return team_to_id


def write_database(db_file, teams):
    conn = sqlite3.connect(db_file)
    for name, team_id in teams.items():
        if not name:
            continue
        conn.execute('INSERT OR IGNORE INTO teams VALUES ' +
                     '("{}","{}")'.
                     format(team_id, name))
        print("Written the team: " + name)

    conn.commit()
    conn.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " [db_file] [link]")
        return
    link = sys.argv[2]
    db_file = sys.argv[1]

    teams = parse_teams(link)
    write_database(db_file, teams)

if __name__ == "__main__":
    main()

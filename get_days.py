from bs4 import BeautifulSoup
import requests
import sys
import sqlite3
import datetime


""" get all the links for gamestands of 2015/16 """
def get_gamestands_1516():
    gamestands = []
    for i in range(14350,14365):
        gamestands.append("http://195.56.77.208/stand/?from=2015&lea=219&i=1&round=" +
                          str(i) + "&rfrom=2015&rlea=219&ri=1")
    for i in range(14365,14380):
        gamestands.append("http://195.56.77.208/stand/?from=2015&lea=219&i=2&round=" +
                          str(i) + "&rfrom=2015&rlea=219&ri=1")
    return gamestands

""" get all the links for gamestands of 2016/17 """
def get_gamestands_1617():
    gamestands = []
    for i in range(14400,14415):
        gamestands.append("http://195.56.77.208/stand/?from=2016&lea=221&i=1&round=" +
                          str(i) + "&rfrom=2016&rlea=221&ri=1")
    for i in range(14415,14430):
        gamestands.append("http://195.56.77.208/stand/?from=2016&lea=221&i=2&round=" +
                          str(i) + "&rfrom=2016&rlea=221&ri=2")
    return gamestands

def parse_range_date(gamestand_link):
    r = requests.get(gamestand_link)
    soup = BeautifulSoup(r.text.encode('utf8'), "lxml")
    dates_raw = soup.findAll("td", class_="fs12")

    dates = [ datetime.datetime.strptime(el.get_text()[:10], "%d/%m/%Y") for el in dates_raw]
    start, end = min(dates), max(dates)
    return (start, end)

def write_database(db_file, start, end, year, link):
    conn = sqlite3.connect(db_file)
    conn.execute('INSERT OR IGNORE INTO championshipDays VALUES ' +
                 '(NULL, {}, "{}", "{}", "{}")'.
                 format(year, start, end, link))

    conn.commit()
    conn.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " [db_file] [year]")
        return
    year = int(sys.argv[2])
    if  year != 1617 and year != 1516:
        print("Selected a wrong year")
        return
    db_file = sys.argv[1]
    gamestands = []
    if year == 1617:
        gamestands = get_gamestands_1617()
    else:
        gamestands = get_gamestands_1516()
    for gs in gamestands:
        start, ending  = parse_range_date(gs)
        write_database(db_file, start, ending, year, gs)


if __name__ == "__main__":
    main()

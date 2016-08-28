CREATE TABLE players(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name varchar(255),
	height int,
	weight int,
	birthday date,
	team int,
	role real,
	UNIQUE(id, name)
);

CREATE TABLE teams(
	id int,
	name varchar(255),
	PRIMARY KEY(id ASC),
	UNIQUE(id, name)
);

CREATE TABLE games(
	id int,
	teamA int,
	teamB int,
	pointsA int,
	pointsB int,
	champDay int,
	statsA varchar(2047),
	statsB varchar(2047),
	PRIMARY KEY(id ASC)
);

CREATE TABLE championshipDays(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	year int, -- e.g. 1617 for 2016/17
	start datetime,
	ending datetime,
	link varchar(512) -- the link for the stand
);

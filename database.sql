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
	id int,
	start datetime,
	ending datetime,
	PRIMARY KEY(id)
);

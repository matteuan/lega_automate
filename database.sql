CREATE TABLE players(
	id int,
	name varchar(255),
	height int,
	weight int,
	birthday date,
	team int, 
	role real, # 0.0 coach, 1.0(pure center) -> 5.0 (pure play)
	PRIMARY KEY(id ASC)
);

CREATE TABLE teams(
	id int,
	name varchar(255),
	coach int,
	PRIMARY KEY(id ASC)
);

CREATE TABLE games(
	id int,
	teamA int,
	teamB int,
	pointsA int,
	pointsB int,
	eventDate datetime,
	champDay int,
	statsA varchar(2047), # serialized singular stats
	statsB varchar(2047), 
	PRIMARY KEY(id ASC)
);

CREATE TABLE championshipDays(
	id int,
	start datetime,
	ending datetime,
	PRIMARY KEY(id)
);


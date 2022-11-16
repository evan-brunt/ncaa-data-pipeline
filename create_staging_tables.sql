DROP TABLE IF EXISTS drives_staging;
CREATE TABLE drives_staging (
	game_id integer, 
	drive_num integer,
	offense_id integer,
	result varchar,
	num_plays integer,
	yards integer, 
	time_of_poss varchar
);

CREATE TABLE IF NOT EXISTS drives (
	game_id integer, 
	drive_num integer, 
	offense_id integer, 
	result varchar, 
	num_plays integer, 
	yards integer, 
	time_of_poss_seconds integer
);

DROP TABLE IF EXISTS teams_staging;
CREATE TABLE teams_staging (
	team_id integer,
	long_name varchar,
	short_name varchar,
	abbrev varchar,
	conference varchar,
	division varchar
);


CREATE TABLE IF NOT EXISTS teams (
	team_id integer,
	long_name varchar,
	short_name varchar,
	abbrev varchar,
	conference varchar,
	division varchar
);

CREATE TABLE IF NOT EXISTS scoreboards (
	game_id integer,
	team_id integer,
	first_quarter smallint,
	second_quarter smallint,
	third_quarter smallint,
	fourth_quarter smallint,
	total smallint,
	overtime smallint
);

DROP TABLE IF EXISTS games_staging;
CREATE TABLE games_staging (
	year smallint,
	week smallint, 
	game_id integer, 
	away_team_id integer, 
	home_team_id integer,
	date varchar,
	status varchar
);

CREATE TABLE IF NOT EXISTS games (
	year smallint,
	week smallint, 
	game_id integer, 
	away_team_id integer, 
	home_team_id integer,
	date timestamp,
	status varchar
);

DROP TABLE IF EXISTS team_stats_staging;
CREATE TABLE team_stats_staging (
	game_id integer,
	team_id integer, 
	firstDowns smallint,
	thirdDownEff varchar,
	fourthDownEff varchar,
	totalYards smallint,
	netPassingYards smallint,
	completionAttempts varchar,
	yardsPerPass float,
	interceptions smallint,
	rushingYards smallint, 
	rushingAttempts smallint,
	yardsPerRushAttempt float,
	totalPenaltiesYards varchar,
	turnovers smallint,
	fumbles_lost smallint,
	possessionTime varchar
);
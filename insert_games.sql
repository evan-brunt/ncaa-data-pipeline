INSERT INTO games (year, week, game_id, away_team_id, home_team_id, date, status)
SELECT year, week, game_id, away_team_id, home_team_id, date::timestamp, status
FROM games_staging;
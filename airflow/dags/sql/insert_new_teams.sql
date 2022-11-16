INSERT INTO teams 
(SELECT * 
	FROM teams_staging 
	WHERE team_id 
	NOT IN 
	(SELECT team_id FROM teams)
) 

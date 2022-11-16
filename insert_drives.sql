INSERT INTO drives
( 
	SELECT 
	game_id, drive_num, offense_id, result, num_plays, yards, SPLIT_PART(time_of_poss,':', 1)::smallint * 60 + SPLIT_PART(time_of_poss,':', 2)::smallint as time_of_poss_seconds 
	FROM drives_staging
)
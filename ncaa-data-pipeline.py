from __future__ import annotations

from airflow import DAG
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import get_current_context
import logging
import pendulum

conn_id = 'redshift'
arn = 'arn:aws:iam::570616463213:role/redshift_s3_readonly'

@dag(schedule='@weekly',
	start_date=pendulum.datetime(2022, 9, 3),
	catchup=True,
	max_active_runs=1)
def ncaaf_data_pipeline():
	@task
	def copy_data_from_s3_to_redshift(table_name, file_name):
		context = get_current_context()
		execution_date = context['execution_date']
		start_date = pendulum.datetime(2022, 9, 3)
		year = execution_date.year
		week = execution_date.week_of_year - start_date.week_of_year + 1

		s3_path = f's3://ebrunt-espn-data/ncaa-data/{ year }/{ week }/{ file_name }'
		copy_sql = f"COPY { table_name } FROM '{ s3_path }' IAM_ROLE '{ arn }' json 'auto ignorecase'"
		
		postgres = PostgresHook.get_hook(conn_id)
		postgres.run(copy_sql)

	create_staging_tables = PostgresOperator(task_id='create_staging_tables', postgres_conn_id=conn_id, sql='sql/create_staging_tables.sql')
	
	copy_data = copy_data_from_s3_to_redshift.expand_kwargs([
		{'table_name': 'teams', 'file_name': 'teams.json'},
		{'table_name': 'scoreboards', 'file_name': 'scoreboards.json'},
		{'table_name': 'drives', 'file_name': 'drives.json'},
		{'table_name': 'team_stats_staging', 'file_name': 'team-stats.json'},
		{'table_name': 'games_staging', 'file_name': 'games.json'}
		])
	
	insert_new_teams = PostgresOperator(task_id='insert_new_teams', postgres_conn_id=conn_id, sql='sql/insert_new_teams.sql')
	insert_drives = PostgresOperator(task_id='insert_drives', postgres_conn_id=conn_id, sql='sql/insert_drives.sql')
	insert_games = PostgresOperator(task_id='insert_games', postgres_conn_id=conn_id, sql='sql/insert_games.sql')



	#DATES
	#QUALITY CHECK


	
	create_staging_tables >> copy_data
	copy_data >> insert_new_teams
	copy_data >> insert_drives
	copy_data >> insert_games

ncaaf_data_pipeline()
	


	# COPY DATA TO STAGING
	# INSERT STAGING DATA TO FINAL TABLES
	# CHECK THAT CURRENT WEEKS GAMES WERE SUCESSFULLY UPLOADED
	# PERFORM ANALYSIS
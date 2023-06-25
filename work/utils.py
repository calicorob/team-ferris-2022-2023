__all__ = ["get_event_stats"]

from config import *
import pandas as pd

def get_event_stats()->pd.DataFrame:
    query = """

        WITH ds AS
(
SELECT
    *
    ,LEAD(end_start_relative_score,1) OVER(PARTITION BY guid, team_id ORDER BY end_num ASC) AS last_end_relative_score
FROM data.unnested_boxscore
), rs AS
(
SELECT
    *
    ,last_end_relative_score - end_start_relative_score  AS end_result
FROM ds
), hammer_efficiency AS 
(

SELECT
     team_name
    ,team_id
    ,event_id
    ,COUNT(DISTINCT end_guid) AS ends_played
    ,COUNT(DISTINCT CASE WHEN end_start_hammer THEN end_guid ELSE NULL END) AS ends_with_hammer
    ,COUNT(DISTINCT CASE WHEN end_start_hammer AND end_result = 0 THEN end_guid ELSE NULL END) AS ends_with_hammer_blanked
    ,COUNT(DISTINCT CASE WHEN end_start_hammer AND end_result >= 2 THEN end_guid ELSE NULL END) AS ends_converted
    ,COUNT(DISTINCT CASE WHEN end_start_hammer AND end_result < 0 THEN end_guid ELSE NULL END) AS ends_steal_given_up
    ,COUNT(DISTINCT CASE WHEN NOT end_start_hammer THEN end_guid ELSE NULL END) AS ends_without_hammer
    ,COUNT(DISTINCT CASE WHEN NOT end_start_hammer AND end_result = 0 THEN end_guid ELSE NULL END) AS ends_without_hammer_blanked
    ,COUNT(DISTINCT CASE WHEN NOT end_start_hammer AND end_result = -1 THEN end_guid ELSE NULL END) AS ends_forced
    ,COUNT(DISTINCT CASE WHEN NOT end_start_hammer AND end_result > 0 THEN end_guid ELSE NULL END) AS ends_stolen
    
FROM rs
WHERE  end_score <> 'X'
GROUP BY
     1
    ,2
    ,3
), event_stats AS
(

SELECT
     b1.team_name
    ,b1.team_id
    ,b1.event_id
    ,COUNT(DISTINCT b1.guid) AS games_played
    ,COUNT(DISTINCT CASE WHEN b1.hammer_start THEN b1.guid ELSE NULL END) AS games_with_hammer_to_start
    ,COUNT(DISTINCT CASE WHEN b1.final_score > b2.final_score THEN b1.guid ELSE NULL END) AS wins
FROM data.unnested_boxscore b1
LEFT JOIN data.unnested_boxscore b2
ON b2.guid = b1.guid AND b2.team_id <> b1.team_id

GROUP BY
     1
    ,2
    ,3
)
SELECT
     es.*
    ,he.ends_played
    ,he.ends_with_hammer
    ,he.ends_with_hammer_blanked
    ,he.ends_converted
    ,ROUND((he.ends_converted / CAST((he.ends_with_hammer - he.ends_with_hammer_blanked) AS NUMERIC(10,6))),4) AS hammer_conversion
    ,he.ends_without_hammer
    ,he.ends_without_hammer_blanked
    ,he.ends_forced
    ,ROUND((he.ends_forced/CAST((he.ends_without_hammer - he.ends_without_hammer_blanked) AS NUMERIC(10,6))),4) AS force_conversion
    ,he.ends_stolen
    ,ROUND((he.ends_stolen/CAST((he.ends_without_hammer - he.ends_without_hammer_blanked) AS NUMERIC(10,6))),4) AS steal_conversion
    ,he.ends_steal_given_up
    ,ROUND((he.ends_steal_given_up / CAST((he.ends_with_hammer - he.ends_with_hammer_blanked) AS NUMERIC(10,6))),4) AS stolen_pct
FROM event_stats es
LEFT JOIN hammer_efficiency he
ON he.team_id = es.team_id AND he.event_id = es.event_id;

    """
    df = pd.read_sql(sql=query,con=db_engine)
    return df
if __name__ == '__main__':
    main()
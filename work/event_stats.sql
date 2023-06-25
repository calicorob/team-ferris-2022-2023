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
WHERE b1.team_name = 'Pat Ferris'
GROUP BY
    1
    ,2
    ,3;


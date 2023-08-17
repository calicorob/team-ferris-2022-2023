WITH ds AS
(
    SELECT
         b1.*
        ,b2.final_score AS final_score_other_team
        ,b1.final_score > b2.final_score AS won_game
    FROM data.unnested_boxscore b1
    LEFT JOIN data.unnested_boxscore b2
    ON b2.guid = b1.guid AND b2.team_id <> b1.team_id AND b2.end_num = b1.end_num
)


SELECT
     team_name
    ,end_num
    ,end_start_hammer
    ,end_start_relative_score
    ,AVG(CAST(won_game AS INT)) AS win_pct
    ,COUNT(*) AS situations_count
FROM ds
WHERE team_name = 'Pat Ferris' AND ABS(end_start_relative_score) BETWEEN 0 AND 2
GROUP BY
     1
    ,2
    ,3
    ,4
ORDER BY
    2 ASC, 3, 4 ASC
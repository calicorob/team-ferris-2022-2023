DROP TABLE IF EXISTS data.test;

CREATE TABLE data.test 
AS
WITH ds AS
(
SELECT
     b.team_name
    ,b.hammer_start
    ,CAST(b.final_score AS INT) AS final_score
    ,CAST(b.draw_num AS INT) AS draw_num
    ,b.draw
    ,b.guid
    ,b.href
    ,SUBSTRING(b.href FROM '^.*teamid=(\d*)[#&].*') AS team_id
    ,SUBSTRING(b.href FROM '^.*eventid=(\d*)[#&].*') AS event_id
    ,hp.end_start_hammer
    ,hp.end_result
    ,hp.idx
    ,hp.end_start_relative_score
FROM data.boxscore b
CROSS JOIN UNNEST(b.hammer_progress,b.score,b.relative_score) WITH ORDINALITY AS hp(end_start_hammer,end_result,end_start_relative_score,idx)
)
SELECT
    *
FROM ds;


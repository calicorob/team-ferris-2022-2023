CREATE DATABASE ferris;

\c ferris;

CREATE SCHEMA data;


CREATE TABLE data.boxscore
(
     team_name TEXT
    ,href TEXT
    ,hammer_start BOOLEAN
    ,score VARCHAR(2)[]
    ,final_score VARCHAR(2)
    ,draw_num SMALLINT
    ,draw TEXT
    ,hammer_progress BOOLEAN[]
    ,relative_score SMALLINT[]
    ,guid TEXT


);
from config import *
import czapi.api as api
import czapi


def test_main()->None:
    event = api.Event(cz_event_id=7508)
    boxscores = event.get_flat_boxscores(flat=False)



    with db_engine.connect() as con:
        con.execute(
             boxscore_table.insert()
            ,[

                {
                     'team_name':boxscore.team_name
                    ,'href':boxscore.href
                    ,'hammer_start':boxscore.hammer_start
                    ,'score':boxscore.score
                    ,'final_score':boxscore.final_score
                    ,'draw_num':boxscore.draw_num
                    ,'draw':boxscore.draw
                    ,'hammer_progress' : boxscore.hammer_progression
                    ,'relative_score' : boxscore.relative_score
                    ,'guid' : boxscore.guid
                }
            
            for boxscore in boxscores] # if statement is because czapi is dumb
        )


        con.commit()
    


if __name__ == '__main__':

    test_main()
from config import *
import czapi.api as api
from czapi.core.errors import InvalidScoreError
from sqlalchemy import inspect


def create_or_replace_boxscore_table():
    if inspect(db_engine).has_table(table_name=boxscore_table.name,schema=boxscore_table.schema):
        with db_engine.connect() as con:
            boxscore_table.drop(bind=con)
            con.commit()
    boxscore_meta.create_all(db_engine)


def main():
    create_or_replace_boxscore_table()
    for cz_event_id in events:
        print('Scraping event: %s'%cz_event_id)
        try:
            event = api.Event(cz_event_id=cz_event_id,delay=2,verbose=True)
        except InvalidScoreError as e:
            print("Error with event id: %s"%cz_event_id)
            print(e)
            continue
        except AttributeError as e:
            print("Error with event id: %s"%cz_event_id)
            print(e)
            continue
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
                for boxscore in boxscores]
            )
            con.commit()
    

def test_scrape()->None:
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
    main()
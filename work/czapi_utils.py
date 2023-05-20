import pandas as pd
import czapi.api as api

def make_frame_from_event(event:api.Event)->pd.DataFrame:
    return pd.concat([pd.DataFrame(data=boxscore,columns=api.game_data_column_headers) for boxscore in event.get_flat_boxscores()],axis=0,sort=True).reset_index(drop=True)
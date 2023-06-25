__all__ = ["get_event_stats"]

from config import *
import pandas as pd

def get_event_stats()->pd.DataFrame:
    query = """

        SELECT 
            *
        FROM data.event_result;

    """
    df = pd.read_sql(sql=query,con=db_engine)
    return df
if __name__ == '__main__':
    pass
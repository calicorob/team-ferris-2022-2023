
from sqlalchemy_utils import create_database,database_exists
from config import *

def create_db()->None:
    if not database_exists(url=db_engine.url): create_database(url=db_engine.url)
def create_schema()->None:
    if not inspector.has_schema(schema_name=data_schema_name):
        with db_engine.connect() as con:
            con.execute(data_schema)
            con.commit()
def create_table()->None:
    if not inspector.has_table(table_name=boxscore_table.name,schema=data_schema_name): boxscore_meta.create_all(db_engine)


def main()->None:
    create_db()
    if database_exists(url=db_engine.url): print('Database ferris exists')
    create_schema()
    if inspector.has_schema(schema_name='data'):print('Schema data exists')
    create_table()
    if inspector.has_table(table_name='boxscore',schema='data'): print('Table data.boxscore in ferris db exists')
    





if __name__ == '__main__':
    main()
    
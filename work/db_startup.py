from sqlalchemy import URL, create_engine,text,schema
from sqlalchemy import inspect
from sqlalchemy_utils import create_database,database_exists
from sqlalchemy import Table, Column, String, ARRAY, Text, MetaData, Boolean, SmallInteger, BigInteger



# DB con
url_object = URL.create(
    "postgresql+pg8000",
    username="postgres",
    password="postgres",  # plain (unescaped) text
    host="db",
    database="ferris",
)

db_engine = create_engine(url_object)
inspector = inspect(db_engine)

# schema
data_schema = schema.CreateSchema(name='data',if_not_exists=True)

# tables
meta = MetaData()
table = Table(
    'boxscore'
    ,meta
    ,Column(name = 'team_name',type_=Text)
    ,Column(name = 'href',type_ = Text)
    ,Column(name='hammer_start',type_ = Boolean)
    ,Column(name='score',type_=ARRAY(String(2)))
    ,Column(name='final_score',type_ = String(2))
    ,Column(name='draw_num',type_ = SmallInteger)
    ,Column(name='draw',type_=Text)
    ,Column(name='hammer_progress',type_=ARRAY(Boolean))
    ,Column(name='relative_score',type_=ARRAY(SmallInteger))
    ,Column(name='guid',type_=BigInteger)
    ,schema='data'

)


def create_db()->None:
    if not database_exists(url=db_engine.url): create_database(url=db_engine.url)
def create_schema()->None:
    if not inspector.has_schema(schema_name='data'):
        with db_engine.connect() as con:
            con.execute(data_schema)
            con.commit()
def create_table()->None:
    if not inspector.has_table(table_name='boxscore',schema='data'): meta.create_all(db_engine)


def main()->None:
    create_db()
    if database_exists(url=db_engine.url): print('Database ferris exists')
    create_schema()
    if inspector.has_schema(schema_name='data'):print('Schema data exists')
    create_table()
    if inspector.has_table(table_name='boxscore',schema='data'): print('Table data.boxscore exists')
    





if __name__ == '__main__':
    main()
    
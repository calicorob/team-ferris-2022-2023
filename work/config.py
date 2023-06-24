__all__ = ['db_engine', 'data_schema','data_schema_name','boxscore_meta','boxscore_table','events']


from sqlalchemy import Table, Column, String, ARRAY, Text, MetaData, Boolean, SmallInteger, BigInteger
from sqlalchemy import URL, create_engine,text,schema
from sqlalchemy import inspect


# DB con
url_object = URL.create(
    "postgresql+pg8000",
    username="postgres",
    password="postgres",  # plain (unescaped) text
    host="db",
    database="ferris",
)

db_engine = create_engine(url_object)

# schema
data_schema_name = 'data'
data_schema = schema.CreateSchema(name=data_schema_name,if_not_exists=True)

# tables
boxscore_meta = MetaData()
boxscore_table = Table(
    'boxscore'
    ,boxscore_meta
    ,Column(name = 'team_name',type_=Text)
    ,Column(name = 'href',type_ = Text)
    ,Column(name='hammer_start',type_ = Boolean)
    ,Column(name='score',type_=ARRAY(String(2)))
    ,Column(name='final_score',type_ = String(2))
    ,Column(name='draw_num',type_ = SmallInteger)
    ,Column(name='draw',type_=Text)
    ,Column(name='hammer_progress',type_=ARRAY(Boolean))
    ,Column(name='relative_score',type_=ARRAY(SmallInteger))
    ,Column(name='guid',type_=Text)
    ,schema=data_schema_name

)


events = [
     7508
    ,7450
    ,7403
    ,7543
    ,7405
    ,7472
    ,7473
    ,7135
    ,7707
    ,7319
    
]

if __name__ == '__main__':
    pass
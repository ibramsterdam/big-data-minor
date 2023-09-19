import pandas as pd
from sqlalchemy import create_engine, select, MetaData, Table



df=pd.read_csv('../data/population.csv', sep=',')

engine = create_engine('sqlite:///population.sqlite')
df.to_sql(name='population',con=engine,if_exists='fail',index=False)

# connection = engine.connect()
# metadata = MetaData()
# population_table = Table('population', metadata)

# print(repr(population_table))

from sqlalchemy import Column, Integer, String, DateTime, create_engine, Float, Boolean, MetaData, inspect
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
metadata = MetaData()

class User_Tasks(Base):
    __tablename__ = "Tasks information"

    id = Column("id", Integer, primary_key=True)
    t_text = Column("Task text", String)
    t_position_x = Column("Task x position", Float)
    t_position_y = Column("Task y position", Float)
    t_date = Column("Task's due date", DateTime)
    t_chosen = Column("Task is clicked", Boolean)
    bad_points = Column("Bad points", Integer)
    t_finished = Column("Task is done", Boolean)

def create_table():
    Base.metadata.create_all(engine)

    table_info = inspect(engine)
    table_name = table_info.get_table_names()
    print(table_name)
    columns = table_info.get_columns(table_name)
    
    for column in columns:
        print(f"Nazev je {column['name']} a je typem {column['type']}")


create_table()

from sqlalchemy import Column, Integer, String, Date, create_engine, Float, Boolean, MetaData, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
metadata = MetaData()

class User_Tasks(Base):
    __tablename__ = "Tasks information"

    id = Column("id", Integer, primary_key=True)
    t_text = Column("Task text", String)
    t_position_x = Column("Task x position", Float)
    t_position_y = Column("Task y position", Float)
    t_date = Column("Task's due date", Date)
    t_chosen = Column("Task is clicked", Boolean)
    bad_points = Column("Bad points", Integer)
    t_finished = Column("Task is done", Boolean)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()    

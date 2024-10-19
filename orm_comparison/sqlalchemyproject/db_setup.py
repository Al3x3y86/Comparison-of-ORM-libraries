from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///sqlalchemy_db.sqlite3"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

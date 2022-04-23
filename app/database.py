from requests import Session, session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import psycopg
#from psycopg.rows import dict_row
#import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




##while True:

#    try:
#        conn = psycopg.connect(host='localhost', dbname='pythonapi', user='postgres',
#        password='Password', row_factory=dict_row)
#        cursor = conn.cursor()
#        print ("Connected to DB")
#        break
#    except Exception as error:
#        print("Connection Failed")
#        print ("Error:", error)
#        time.sleep(2)

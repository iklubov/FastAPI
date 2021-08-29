import csv

from sqlalchemy import create_engine, Column, Integer, Date, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from schemas import ItemModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def create_item(uid, columns, row):
    item_data = {c: r for c, r in zip(columns, row)}
    item_data['id'] = uid
    item = ItemModel(**item_data)
    db_item = Item(**item.dict())
    return db_item


def parse_csv():
    columns = []
    rows = []
    with open('data/dataset.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if not columns:
                columns = row[0].split(',')
            else:
                rows.append(row[0].split(','))
    return columns, rows


def fill_database():
    columns, rows = parse_csv()
    uid = 0
    db: Session = get_db()
    # NOT PRODUCTION DECISION
    db.query(Item).delete()
    for row in rows:
        db_item = create_item(uid, columns, row)
        db.add(db_item)
        uid += 1
    db.commit()
    db.close()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    channel = Column(String)
    country = Column(String)
    os = Column(String)
    impressions = Column(Integer)
    clicks = Column(Integer)
    installs = Column(Integer)
    spend = Column(Float)
    revenue = Column(Float)

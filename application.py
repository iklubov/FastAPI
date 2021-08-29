from datetime import date
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Body
import csv

from sqlalchemy import Date, func, desc
from sqlalchemy.exc import CompileError
from sqlalchemy.orm import Session

from sql_app import models, crud
from sql_app.database import engine, get_db
from sql_app.examples import IMPRESSIONS_CLICKS_BEFORE01062017, INSTALLS_OS_MAY2017, REVENUE_01062017_US, \
    CPI_SPEND_CANADA
from sql_app.schemas import ItemCreate, Item, QueryModel, ItemBase

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# todos
# mix id into model
# what the fuck is Depends
# check for database consistency
# url for localhost - in settings


def create_item(db, id, columns, row):
    item_data = {c:r for c,r in zip(columns, row)}
    item_data['id'] = id
    item: ItemCreate = ItemCreate(**item_data)
    crud.create_item(db, item)
    print('Item created', item)

@app.post("/query/")
def read_columns(
        query: QueryModel = Body(
            ...,
            examples={
                "impressions_clicks_before01062017": IMPRESSIONS_CLICKS_BEFORE01062017,
                "installs_os_may2017": INSTALLS_OS_MAY2017,
                "revenue_01062017_us": REVENUE_01062017_US,
                "cpi_spend_canada": CPI_SPEND_CANADA
                },
            ),
        ):
    db: Session = get_db()
    columns, filters, groups, orders = query.getQuery()
    try:
        result = db.query(*columns).filter(*filters).group_by(*groups).order_by(*orders).all()
    except CompileError:
        result = 'No result due to error'
    db.close()
    return result

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
    id = 0
    db: Session = get_db()
    for row in rows:
        create_item(db, id, columns, row)
        id+=1
    db.close()

#fill_database()

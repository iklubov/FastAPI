from fastapi import FastAPI, Body

from sqlalchemy.exc import CompileError
from sqlalchemy.orm import Session

from database import engine, get_db, fill_database, Base
from examples import IMPRESSIONS_CLICKS_BEFORE01062017, INSTALLS_OS_MAY2017, REVENUE_01062017_US, \
    CPI_SPEND_CANADA, FULL_TABLE_QUERY, JUNE_01_2017
from schemas import QueryModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/query/")
def read_columns(
        query: QueryModel = Body(
            ...,
            examples={
                "impressions_clicks_before01062017": IMPRESSIONS_CLICKS_BEFORE01062017,
                "installs_os_may2017": INSTALLS_OS_MAY2017,
                "revenue_01062017_us": REVENUE_01062017_US,
                "cpi_spend_canada": CPI_SPEND_CANADA,
                "full_table_query": FULL_TABLE_QUERY,
                "june_01_2017": JUNE_01_2017,
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

fill_database()

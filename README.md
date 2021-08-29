## Introduction

This application creates database from csv file and provides access to the database using POST request
The application based on [FastAPI](https://fastapi.tiangolo.com) framework which use [SQLAlchemy](https://www.sqlalchemy.org/)
framework with it's Python database wrapper. I used SQLLite database here.

## Usage

Install all packets from requirements.txt. Then [run fastapi](https://fastapi.tiangolo.com/#run-it).
You can find examples of all queries from the task in examples.py. Also you can find them on http://127.0.0.1:8000/docs, where all of them are presented. 
## Request body structure

Request body is json like this:
````json
{
  "columns": [...], SELECT
  "filters": [...], WHERE
  "groups": [...],  GROUP_BY
  "orders": [...],  ORDER_BY
}
````
### SELECT - "columns" json part

````json
{  
  "name": "channel"
}
````
is "SELECT channel FROM table"
````json
{
  "name": "impressions",
  "function": "sum",
  "label": "impressions",
}
````
is "SELECT SUM(impressions) FROM table AS impressions"
````json
[
  {
    "columnFunctions": [
      {
        "name": "clicks",
        "function": "avg",
        "label": "clicks",
      },
      {
        "name": "installs",
        "function": "avg",
        "label": "installs",
      },
    ],
    "operator": "truediv",
    "label": "CPI",
  },
]
````
is "SELECT (AVG(clicks) AS clicks) / AVG(installs) AS installs) FROM table AS CPI"

Functions SUM and AVG are supported and div operation is also supported

### WHERE = "filters" json part

````json
{
  "name": "date",
  "relation": "eq",
  "value": "2017-06-01"
}
````
is "WHERE date == '2017-06-01'"

relations supported = "lt", "le", "ge", "gt", "eq", "ne", "between_op"

### GROUP_BY = "groups" json part

````json
{
"name": "date"
}
````
is "GROUP_BY(date)"

### ORDER_BY - "orders"

````json
{
    "name": "date",
    "desc": false,
    "label": "",
}
````
is ORDER_BY(date)

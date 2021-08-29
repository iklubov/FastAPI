## Introduction

This application creates database from csv file and provides access to the database using POST request
The application based on [FastAPI](https://fastapi.tiangolo.com) framework which use [SQLAlchemy](https://www.sqlalchemy.org/)
framework with its Python database wrapper. I used SQLLite database here.

## Usage

Install all packets from requirements.txt. Then [run fastapi](https://fastapi.tiangolo.com/#run-it).
You can find examples of all queries from the task in examples.py. Also, you can find them on http://127.0.0.1:8000/docs, where all of them are presented.

Either you can send POST request on http://127.0.0.1:8000/query/ using any method you prefer. The jsons for test requests are below

### The number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
````json
{
  "columns": [
    {
      "name": "channel"
    },
    {
      "name": "country"
    },
    {
      "name": "impressions",
      "function": "sum",
      "label": "impressions"
    },
    {
      "name": "clicks",
      "function": "sum",
      "label": "clicks"
    }
  ],
  "filters": [
    {
      "name": "date",
      "relation": "lt",
      "value": "2017-6-1"
    }
  ],
  "groups": [
    {
      "name": "channel"
    },
    {
      "name": "country"
    }
  ],
  "orders": [
    {
      "name": "",
      "desc": true,
      "label": "clicks"
    }
  ]
}
````

### The number of installs that occurred in May 2017 on iOS, broken down by date, sorted by date in ascending order

````json
{
  "columns": [
    {
      "name": "date"
    },
    {
      "name": "installs",
      "function": "sum",
      "label": "installs"
    }
  ],
  "filters": [
    {
      "name": "date",
      "relation": "between_op",
      "value": [
        "2017-05-01",
        "2017-05-31"
      ]
    }
  ],
  "groups": [
    {
      "name": "date"
    }
  ],
  "orders": [
    {
      "name": "date",
      "desc": false,
      "label": ""
    }
  ]
}
````

### Revenue, earned on June 1, 2017, in US, broken down by operating system and sorted by revenue in descending order


````json
{
  "columns": [
    {
      "name": "revenue",
      "function": "sum",
      "label": "total_revenue"
    }
  ],
  "filters": [
    {
      "name": "date",
      "relation": "eq",
      "value": "2017-06-01"
    }
  ],
  "groups": [
    {
      "name": "os"
    }
  ],
  "orders": [
    {
      "name": "",
      "desc": true,
      "label": "total_revenue"
    }
  ]
}
````

### CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order


````json
{
  "columns": [
    {
      "columnFunctions": [
        {
          "name": "clicks",
          "function": "avg",
          "label": "clicks"
        },
        {
          "name": "installs",
          "function": "avg",
          "label": "installs"
        }
      ],
      "operator": "truediv",
      "label": "CPI"
    }
  ],
  "filters": [
    {
      "name": "country",
      "relation": "eq",
      "value": "CA"
    }
  ],
  "groups": [
    {
      "name": "channel"
    }
  ],
  "orders": [
    {
      "name": "",
      "desc": true,
      "label": "CPI"
    }
  ]
}
````

### SELECT * FROM table


````json
{}
````

## Request body structure

Request body is json like this:
````json
{
  //list of columns (optional)
  "columns": [],
  //list of filters (optional)
  "filters": [],
  //list of columns to group (optional)
  "groups": [],
  //list of columns to order (optional)
  "orders": []
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
  "label": "impressions"
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
        "label": "clicks"
      },
      {
        "name": "installs",
        "function": "avg",
        "label": "installs"
      }
    ],
    "operator": "truediv",
    "label": "CPI"
  }
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
    "label": ""
}
````
is ORDER_BY(date)

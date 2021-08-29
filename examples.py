IMPRESSIONS_CLICKS_BEFORE01062017 = {
    "summary": "impressions and clicks before 01062017 by clicks",
    "description": "The number of impressions and clicks that occurred before the 1st of June 2017, "
                   "broken down by channel and country, sorted by clicks in descending order.",
    "value": {
        "columns": [
            {
                "name": "channel",
            },
            {
                "name": "country",
            },
            {
                "name": "impressions",
                "function": "sum",
                "label": "impressions",
            },
            {
                "name": "clicks",
                "function": "sum",
                "label": "clicks",
            },

        ],
        "filters": [
            {
                "name": "date",
                "relation": "lt",
                "value": "2017-6-1",
            },
        ],
        "groups": [
            {
                "name": "channel",
            },
            {
                "name": "country",
            },
        ],
        "orders": [
            {
                "name": "",
                "desc": True,
                "label": "clicks",
            },
        ],
    }
}

INSTALLS_OS_MAY2017 = {
    "summary": "installs in May 2017 by date",
    "description": "The number of installs that occurred in May of 2017 on iOS, broken down by date, "
                   "sorted by date in ascending order",
    "value": {
        "columns": [
            {
                "name": "date",
            },
            {
                "name": "installs",
                "function": "sum",
                "label": "installs",
            },
        ],
        "filters": [
            {
                "name": "date",
                "relation": "between_op",
                "value": ['2017-05-01', '2017-05-31'],
            },
        ],
        "groups": [
            {
                "name": "date",
            },
        ],
        "orders": [
            {
                "name": "date",
                "desc": False,
                "label": "",
            },
        ],
    }
}

REVENUE_01062017_US = {
    "summary": "revenue on June 1, 2017 in US",
    "description": "Revenue, earned on June 1, 2017 in US, broken down by operating system and "
                   "sorted by revenue in descending order",
    "value": {
        "columns": [
            {
                "name": "revenue",
                "function": "sum",
                "label": "total_revenue",
            },
        ],
        "filters": [
            {
                "name": "date",
                "relation": "eq",
                "value": '2017-06-01',
            },
        ],
        "groups": [
            {
                "name": "os",
            },
        ],
        "orders": [
            {
                "name": "",
                "desc": True,
                "label": "total_revenue",
            },
        ],
    }
}

CPI_SPEND_CANADA = {
    "summary": "CPI and spend for Canada",
    "description": "CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order",
    "value": {
        "columns": [
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
        ],
        "filters": [
            {
                "name": "country",
                "relation": "eq",
                "value": 'CA',
            },
        ],
        "groups": [
            {
                "name": "channel",
            },
        ],
        "orders": [
            {
                "name": "",
                "desc": True,
                "label": "CPI",
            },
        ],
    }
}

FULL_TABLE_QUERY = {
    "summary": "all table query",
    "description": "SELECT * FROM table",
    "value": {},
}

JUNE_01_2017 = {
    "summary": "01 June 2017",
    "description": "SELECT * FROM table 01 June 2017",
    "value": {
        "filters": [
            {
                "name": "date",
                "relation": "eq",
                "value": '2017-06-01',
            },
        ],
    },
}

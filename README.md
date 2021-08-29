This application creates database from csv file and provides access to the database using POST request
The application based on FastAPI framework. Requests from the task are in examples.py

I used local server for test. Url is # todo

Request suppports SELECT, WHERE, GROUP_BY, ORDER_BY

Request body is json with optional fields: 
    'columns' = field OR field label OR fields (SELECT PART)
    'filters' = conditions for column values (WHERE PART)
    'groups' = columns to group (GROUP_BY part)
    'orders' == order of columns (ORDER_BY part)

validation is executed using Pydantic models

request body is something like
##### EXAMPLE FROM CODE

you may use http://127.0.0.1:8000/docs for testing 
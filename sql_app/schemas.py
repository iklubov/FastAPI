from enum import Enum
from typing import List, Optional, Type, Union

from pydantic import BaseModel, validator
from pydantic.schema import date
from sqlalchemy import func, desc
from sqlalchemy.sql import functions, operators
from sqlalchemy.sql.functions import _GenericMeta
import operator

from sqlalchemy.util import symbol

from sql_app import models
from sql_app.models import Item

sqlFunctions = func.sum, func.avg
sqlFunctionNames = [f._FunctionGenerator__names[0] for f in sqlFunctions]

arithmeticOperators = operators.div,
relationOperators = operators.lt, operators.le, operators.gt, operators.ge, operators.ne, operators.eq, operators.between_op
validOperatorDict = {op.__name__: op for op in arithmeticOperators + relationOperators}

arithmeticAttributes = 'truediv',
comparisonAttributes = "lt", "le", "ge", "gt", "eq", "ne"
additionalComparisonAttributes = "between_op",


class ItemBase(BaseModel):
    id: int
    date: date
    channel: str
    country: str
    os: str
    impressions: int
    clicks: int
    installs: int
    spend: float
    revenue: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    pass

    class Config:
        orm_mode = True


class ColumnModel(BaseModel):
    name: str

    @validator('name')
    def name_valid(cls, v):
        if getattr(models.Item, v, None) is None:
             raise ValueError('column %s is not valid column name' % v)
        return v

    def getQuery(self):
        return getattr(models.Item, self.name)

class ColumnFunctionModel(ColumnModel):
    function: str
    label: str

    @validator('function')
    def function_valid(cls, v):
        if v != "" and v not in sqlFunctionNames:
            raise ValueError('function name %s is not valid function name' % v)
        return v

    def getQuery(self):
        return getattr(func, self.function)(getattr(models.Item, self.name)).label(self.label)

class MultipleColumnsFunctionModel(BaseModel):
    columnFunctions: List[ColumnFunctionModel]
    operator: str
    label: str

    @validator('operator')
    def value_valid(cls, v, values):
        if v != "" and v not in arithmeticAttributes:
            raise ValueError('function name %s is not valid operator' % v)
        return v

    def getQuery(self):
        return validOperatorDict[self.operator](*(model.getQuery() for model in self.columnFunctions)).label(self.label)


class FilterModel(ColumnModel):
    relation: str
    value: Union[str, List[str]]

    @validator('relation')
    def relation_valid(cls, v):
        if v not in comparisonAttributes+additionalComparisonAttributes:
            raise ValueError('function name %s is not valid function name' % v)
        return v

    @validator('value')
    def value_valid(cls, v, values):
        if values['relation'] in comparisonAttributes and not isinstance(v, str):
            raise ValueError('value for relation %s must be string' % values['relation'])
        if values['relation'] in additionalComparisonAttributes and not isinstance(v, list):
            raise ValueError('value for relation %s must be list' % values['relation'])
        if values['relation'] in additionalComparisonAttributes and values['name'] != 'date':
            raise ValueError('between is used only for dates')
        return v

    def getQuery(self):
        label = getattr(models.Item, self.name)
        value = (self.value,) if type(self.value) == str else self.value
        return validOperatorDict[self.relation](label, *value)


class GroupModel(ColumnModel):

    def getQuery(self):
        return getattr(models.Item, self.name)

class OrderModel(BaseModel):
    name :str = ''
    desc: bool = False
    label: str = ''

    @validator('name')
    def name_valid(cls, v):
        if v and getattr(models.Item, v, None) is None:
            raise ValueError('column %s is not valid column name' % v)
        return v

    @validator("label")
    def label_and_name_valid(cls, v, values):
        bothFilled = 'name' in values and values['name'] and v
        noneFilled = not v and ('name' not in values or not values['name'])
        if bothFilled or noneFilled:
            raise ValueError('you shoud fill either name or label')
        return v

    def getQuery(self):
        label = getattr(models.Item, self.name) if self.name else self.label
        return label if not self.desc else desc(label)

class QueryModel(BaseModel):
    columns: List[Union[ColumnFunctionModel, ColumnModel, MultipleColumnsFunctionModel]]
    filters: List[FilterModel]
    groups: List[GroupModel]
    orders: List[OrderModel]

    def getQuery(self):
        return [c.getQuery() for c in self.columns], \
            [f.getQuery() for f in self.filters], \
            [g.getQuery() for g in self.groups], \
            [o.getQuery() for o in self.orders]



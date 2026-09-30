from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class Operator(str, Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    IN = "IN"
    NOT_IN = "NOT_IN"


class Logic(str, Enum):
    AND = "AND"
    OR = "OR"


class Rule(BaseModel):
    attribute: str
    operator: Operator
    value: Any


class ConditionGroup(BaseModel):
    logic: Logic
    conditions: list[Rule | ConditionGroup]
    
class Scheme(BaseModel):
    scheme_id: str
    name: str
    description: str
    benefits: Any
    eligibility: ConditionGroup
    documents: list[str]
    application: Any
    sources: list[str]
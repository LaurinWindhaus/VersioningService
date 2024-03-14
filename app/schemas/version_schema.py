from pydantic import BaseModel, validator
from typing import Any, Dict
import json
from datetime import datetime


class VersionSchema(BaseModel):
    old_json: Dict[str, Any]
    new_json: Dict[str, Any]
    document_type: str
    document_id: int
    created_by: str

    @validator('old_json', 'new_json', pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")
        elif isinstance(v, dict):
            return v
        raise ValueError("Invalid type")


class VersionResponseSchema(BaseModel):
    document_type: str
    document_id: str
    version: int
    json_data_changes: str
    created_at: Any 
    created_by: str

    @validator('created_at', pre=True, always=True)
    def format_datetime(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()  # Convert datetime to ISO 8601 string format
        return value
    
    class Config:
        from_attributes = True


class VersionChangeSchema(BaseModel):
    document_type: str
    document_id: int
    target_version: int
    current_version: int
    current_json: Dict[str, Any]

    @validator('current_json', pre=True)
    def parse_json(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")
        elif isinstance(v, dict):
            return v
        raise ValueError("Invalid type")
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetJsonSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return str(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _schema_generator: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return {"type": "string"}

class MongoDBConfig:
    collection_name: str
    indexes: List[Dict[str, Any]] = []

class BaseDBModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid)
        }
        populate_by_name = True
        arbitrary_types_allowed = True 
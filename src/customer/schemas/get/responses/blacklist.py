from typing import List, Optional
from pydantic import BaseModel

from pydantic import BaseModel, Field
from bson import ObjectId


class DocumentID(BaseModel):
    documentType: str
    documentNumber: str


class Phones(BaseModel):
    local_format: str
    intl_format: str
    areaCode: str
    countryCode: str
    isMain: bool


class Emails(BaseModel):
    email: str
    isMain: bool


class Languages(BaseModel):
    language: str
    is_main: bool


class BlacklistCustomer(BaseModel):
    id: str = Field(..., alias="_id")
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    last_name: str
    age: int
    email: List[Emails]
    phone: List[Phones]
    address: List[str]
    documentId: List[DocumentID]
    nationality: str
    civilStatus: str
    languages: List[Languages]
    birthdate: str
    associated_sensors: List[str]
    blacklist_status: bool
    blacklist_enable_motive: List[str]
    blacklist_disable_motive: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SearchCustomersResponse(BaseModel):
    customers: List[BlacklistCustomer]
    total_items: int
    total_show: int
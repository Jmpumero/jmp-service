from typing import List, Optional, Any
from fastapi.openapi.models import Link

from pydantic import BaseModel, Field, validator
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DocumentID(BaseModel):
    documentType: str
    documentNumber: str


class Phones(BaseModel):
    local_format: Optional[str]
    intl_format: str
    areaCode: Optional[str]
    countryCode: Optional[str]
    isMain: bool


class Emails(BaseModel):
    email: str
    isMain: bool


class Languages(BaseModel):
    language: str
    isMain: bool


class SocialMedia(BaseModel):
    name_social_media: str
    customer_social_media: str


class Addresses(BaseModel):
    address: str
    isMain: bool


class BlacklistLog(BaseModel):
    date: str
    motives: List[str]
    type: str


# OJO quitar todos los ""
class CreateCustomerBody(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    last_name: str
    full_name: Optional[str]
    nationality: List[str]
    phone: List[Phones]
    address: List[Addresses]
    postal_address: str
    email: List[Emails]
    documentId: List[DocumentID]
    civil_status: str
    age: int
    birthdate: str = ""  # format '%Y-%m-%d
    languages: List[Languages]
    signature: Optional[str]
    social_media: Optional[List[SocialMedia]] = []
    customer_avatar: Optional[str]
    customer_status: bool = True
    blacklist_status: bool = False
    associated_sensors: Optional[List[str]] = []
    country: Optional[str] = ""
    city: Optional[str]
    postalCode: Optional[str]
    blacklist_last_enabled_motive: Optional[List[str]] = []
    blacklist_last_disabled_motive: Optional[List[str]] = []
    create_at: str  # format '%Y-%m-%dT%H:%M:%S', 2021-12-31T23:59:59
    update_at: str = ""  # format '%Y-%m-%dT%H:%M:%S'
    delete_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S'
    general_score: Optional[int]
    stenant: Optional[Any]
    gender: Optional[str]
    profession: Optional[str] = ""
    total_childrens: Optional[int] = 0
    blacklist_log: Optional[List[BlacklistLog]]
    # class Config:  # valida si falta un campo/campo desconocido

    @validator("address")
    def address_must_contain_object(cls, a):
        if len(a) == 0:
            raise ValueError("must contain a object address")
        return a

    @validator("phone")
    def phone_must_contain_object(cls, a):
        if len(a) == 0:
            raise ValueError("must contain a object phone")
        return a

    @validator("email")
    def email_must_contain_object(cls, a):
        if len(a) == 0:
            raise ValueError("must contain a object phone")
        return a

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = "forbid"


class UpdateCustomerBody(BaseModel):
    id: str = Field(..., alias="_id")
    name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    nationality: Optional[List[str]]
    phone: Optional[List[Phones]]
    address: Optional[List[Addresses]]
    postal_address: Optional[str]
    email: Optional[List[Emails]]
    documentId: Optional[List[DocumentID]]
    civil_status: Optional[str]
    age: Optional[int]
    birthdate: Optional[str]
    languages: Optional[List[Languages]]
    social_media: Optional[List[SocialMedia]]
    customer_avatar: Optional[str]
    signature: Optional[str]
    update_at: Optional[str]
    blacklist_last_enabled_motive: Optional[List[str]] = []
    blacklist_last_disabled_motive: Optional[List[str]] = []
    postalCode: Optional[str]
    country: Optional[str]
    city: Optional[str]
    stenant: Optional[Any]
    gender: Optional[str]
    profession: Optional[str]
    total_childrens: Optional[int]
    blacklist_log: Optional[BlacklistLog]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        extra = "forbid"


class MergeCustomerBody(BaseModel):
    id_parent_a: str
    id_parent_b: str
    name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    nationality: Optional[List[str]]
    phone: Optional[List[Phones]]
    address: Optional[List[Addresses]]
    postal_address: Optional[str]
    email: Optional[List[Emails]]
    documentId: List[DocumentID]
    civil_status: Optional[str]
    age: Optional[int]
    birthdate: Optional[str]
    languages: Optional[List[Languages]]
    signature: Optional[str]
    social_media: Optional[List[SocialMedia]] = []
    customer_avatar: Optional[str]
    customer_status: bool = True
    blacklist_status: Optional[bool]
    associated_sensors: Optional[List[str]] = []
    country: Optional[str] = None
    city: Optional[str]
    postalCode: Optional[str]
    blacklist_last_enabled_motive: Optional[List[str]] = []
    blacklist_last_disabled_motive: Optional[List[str]] = []
    create_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S', 2021-12-31T23:59:59
    update_at: Optional[str] = ""  # format '%Y-%m-%dT%H:%M:%S'
    stenant: Optional[Any]
    gender: Optional[str]
    profession: Optional[str]
    total_childrens: Optional[int]
    blacklist_log: Optional[BlacklistLog]

    class Config:  # valida si falta un campo/campo desconocido
        extra = "forbid"

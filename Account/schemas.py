from tkinter import N
from ninja import Schema
from typing import Optional
from pydantic import EmailStr, Field


class AccountCreate(Schema):
    first_name: str
    last_name: str 
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str
    phone_number : str =None
    address : str = None

class AccountOut(Schema):
    first_name: str = None
    last_name: str  = None
    email: EmailStr
    phone_number: Optional[str]
    address: str = None

class SigninSchema(Schema):
    email: EmailStr
    password: str

class AccountUpdate(Schema):
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: str

class ChangePasswordSchema(Schema):
    old_password: str
    new_password1: str
    new_password2: str

class TokenOut(Schema):
    access: str


class AuthOut(Schema):
    token: TokenOut
    account: AccountOut


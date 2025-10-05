from pydantic import BaseModel

class PhoneRequest(BaseModel):
    phone: str

class CodeVerifyRequest(BaseModel):
    phone: str
    code: str

class TwoFAVerifyRequest(BaseModel):
    phone: str
    password: str

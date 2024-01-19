from pydantic import BaseModel, Field

class User(BaseModel):
    firebase_uid : str = Field(default="uninitialized")
    created_at : str
    complaints : list[str] = Field(default=None)
    donations : list[str] = Field(default=None)
    location : str
    type : str = Field(default="citizen")

class Complaints(BaseModel):
    cid : str = Field(default="uninitialized")
    user : User
    timestamp : str
    category : str
    description : str
    area : str
    address : str
    # images : str | list[str]
    images : str

class Donation(BaseModel):
    did : str = Field(default="uninitialized")
    user : list[User]
    timestamp : str
    amount : str

class Notifications(BaseModel):
    nid : str = Field(default="uninitialized")
    timestamp : str
    user : User
    area : str
    message : str
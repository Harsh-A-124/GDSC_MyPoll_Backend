from pydantic import BaseModel, Field

class User(BaseModel):
    firebase_uid : str = Field(default="uninitialized")
    created_at : str = Field(default="uninitialized")
    name : str
    email : str
    mobileno : str
    password : str
    complaints : list[str] = Field(default=[])
    donations : list[str] = Field(default=[])
    location : str
    type : str = Field(default="citizen")

class Complaints(BaseModel):
    cid : str = Field(default="uninitialized")
    # user : User
    user_firebase_id : str   
    timestamp : str
    category : str
    description : str
    area : str
    address : str
    # images : str | list[str]
    images : str

class Donation(BaseModel):
    did : str = Field(default="uninitialized")
    # user : list[User]
    user_firebase_id : str
    timestamp : str
    amount : str

class Notifications(BaseModel):
    nid : str = Field(default="uninitialized")
    timestamp : str
    # user : User
    # user_firebase_id : str
    area : str
    message : str

class Banner(BaseModel):
    bid : str = Field(default = "uninitialized")
    timestamp : str
    image : str
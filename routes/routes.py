from typing import Union
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from models.models import User, Donation, Complaints, Notifications
from dbconfig.dbconfig import conn, db
from json_conv.json_conv import json_user_doc,json_complaints_doc,json_donation_doc,json_notification_doc,jsonify_complaintss,jsonify_donations,jsonify_notifications,jsonify_users
from bson import ObjectId
import json

route = APIRouter()

#ObjectID Parameter validation function
def is_valid_objectid(s):
    try:
        s_object_id = ObjectId(s)
        return True
    except:
        return False
    
#Landing Endpoint for testing    
@route.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs/")

#User Endpoints
@route.post("/createuser/{firebase_user_id}", status_code=201)
def create_user(firebase_user_id: str, user: User):
    user_check = db.users.find_one({"firebase_uid" : firebase_user_id})
    if not user_check:
        cuser_dict = user.model_dump()
        if cuser_dict["firebase_uid"] == "uninitialized":
            cuser_dict["firebase_uid"] = firebase_user_id
        cuser_doc = db.users.insert_one(cuser_dict)
        return JSONResponse(content={"message" : "User Successfully Created", "firebase_uid:" : firebase_user_id, "uid" : str(cuser_doc.inserted_id)})
    else:
        return JSONResponse({"message" : "User Firebase ID Conflict"},status_code=409)

@route.get("/readuser/{firebase_user_id}", status_code=200)
def read_user(firebase_user_id: str):
    # ruser_id = ObjectId(user_id)
    ruser_doc = db.users.find_one({"firebase_uid" : firebase_user_id})
    # if ruser_doc:
    #     ruser_doc['_id'] = str(ruser_doc['_id'])
    if ruser_doc:
        return JSONResponse(content=json.dumps(json_user_doc(ruser_doc)))
    else:
        return JSONResponse(content={"message" : "User Not Found"},status_code=404)

@route.put("/updateuser/{firebase_user_id}", status_code=200)
def update_user(firebase_user_id: str, update_user_data: dict):
    user_check = db.users.find_one({"firebase_uid" : firebase_user_id})
    if user_check:
        # uuser_id =  ObjectId(user_id)
        # uuser_data = user_data.model_dump()
        if "firebase_uid" in update_user_data.keys():
            del update_user_data["firebase_uid"]
        if "created_at" in update_user_data.keys():
            del update_user_data["created_at"]
        uuser_doc = db.users.update_one({"firebase_uid": firebase_user_id}, {"$set": update_user_data})
        updated_user = db.users.find_one({"firebase_uid" : firebase_user_id})
        return JSONResponse(content={"message" : "User Updated Successfully", "Updated User" : json.dumps(json_user_doc(updated_user))})
    else:
        return JSONResponse(content={"message" : "User Not Found"},status_code=404)
    
@route.delete("/deleteuser/{firebase_user_id}", status_code=200)
def delete_user(firebase_user_id: str):
    # duser_id = ObjectId(user_id)
    user_check = db.users.find_one({"firebase_uid" : firebase_user_id})
    if user_check:
        deleted_user_dict = dict(user_check)
        deleted_user_uid = str(deleted_user_dict["_id"])
        duser_doc = db.users.delete_one({"firebase_uid" : firebase_user_id})
        return JSONResponse(content={"message": "User Deleted","deleted_firebase_uid:" : firebase_user_id, "deleted_uid" : deleted_user_uid})
    else:
        return JSONResponse(content={"message" : "User Not Found"},status_code=404)

#Complaint Endpoints
@route.post("/createcomplaint", status_code=201)
def create_complaint(complaint: Complaints):
    ccomplaint_dict = complaint.model_dump()
    if ccomplaint_dict["cid"] != "uninitialized":
        cid_validity = is_valid_objectid(ccomplaint_dict["cid"])
        if cid_validity:
            complaint_check = db.complaints.find_one({"_id" : ObjectId(ccomplaint_dict["cid"])})
            if not complaint_check:
                ccomplaint_doc = db.complaints.insert_one(ccomplaint_dict)
                ccomplaint_dict["cid"] = str(ccomplaint_doc.inserted_id)
                cucomplaint_doc = db.complaints.update_one({"_id": ccomplaint_doc.inserted_id}, {"$set": {"cid":str(ccomplaint_doc.inserted_id)}})
                return JSONResponse(content={"message" : "Complaint Successfully Created", "cid" : ccomplaint_dict["cid"]})
            else:
                return JSONResponse({"message" : "Complaint Firebase ID Conflict"},status_code=409)
        else:
            return JSONResponse({"message" : "Invalid ID"},status_code=400)
    else:
        ccomplaint_doc = db.complaints.insert_one(ccomplaint_dict)
        ccomplaint_dict["cid"] = str(ccomplaint_doc.inserted_id)
        cucomplaint_doc = db.complaints.update_one({"_id": ccomplaint_doc.inserted_id}, {"$set": {"cid":str(ccomplaint_doc.inserted_id)}})
        return JSONResponse(content={"message" : "Complaint Successfully Created", "cid" : ccomplaint_dict["cid"]})

@route.get("/readcomplaint/{complaint_id}", status_code=200)
def read_complaint(complaint_id: str):
    rcomplaint_doc = db.complaints.find_one({"cid" : complaint_id})
    if rcomplaint_doc:
        return JSONResponse(content=json.dumps(json_complaints_doc(rcomplaint_doc)))
    else:
        return JSONResponse(content={"message" : "Complaint Not Found"},status_code=404)

@route.put("/updatecomplaint/{complaint_id}", status_code=200)
def update_complaint(complaint_id: str, update_complaint_data: dict):
    complaint_check = db.complaints.find_one({"cid" : complaint_id})
    if complaint_check:
        if "cid" in update_complaint_data.keys():
            del update_complaint_data["cid"]
        if "user" in update_complaint_data.keys():
            del update_complaint_data["user"]
        ucomplaint_doc = db.complaints.update_one({"cid": complaint_id}, {"$set": update_complaint_data})
        updated_complaint = db.complaints.find_one({"cid" : complaint_id})
        return JSONResponse(content={"message" : "Complaint Updated Successfully", "Updated Complaint" : json.dumps(json_complaints_doc(updated_complaint))})
    else:
        return JSONResponse(content={"message" : "Complaint Not Found"},status_code=404)
    
@route.delete("/deletecomplaint/{complaint_id}", status_code=200)
def delete_complaint(complaint_id: str):
    # dcomplaint_id = ObjectId(complaint_id)
    complaint_check = db.complaints.find_one({"cid" : complaint_id})
    if complaint_check:
        deleted_complaint_dict = dict(complaint_check)
        deleted_complaint_cid = str(deleted_complaint_dict["_id"])
        dcomplaint_doc = db.complaints.delete_one({"cid" : complaint_id})
        return JSONResponse(content={"message": "Complaint Deleted","deleted_cid:" : deleted_complaint_cid})
    else:
        return JSONResponse(content={"message" : "Complaint Not Found"},status_code=404)
    
#Notification Endpoints
@route.post("/createnotification", status_code=201)
def create_notification(notification: Notifications):
    cnotification_dict = notification.model_dump()
    if cnotification_dict["nid"] != "uninitialized":
        nid_validity = is_valid_objectid(cnotification_dict["nid"])
        if nid_validity:
            notification_check = db.notifications.find_one({"_id" : ObjectId(cnotification_dict["nid"])})
            if not notification_check:
                cnotification_doc = db.notifications.insert_one(cnotification_dict)
                cnotification_dict["nid"] = str(cnotification_doc.inserted_id)
                cunotification_doc = db.notifications.update_one({"_id": cnotification_doc.inserted_id}, {"$set": {"nid":str(cnotification_doc.inserted_id)}})
                return JSONResponse(content={"message" : "Notification Successfully Created", "nid" : cnotification_dict["nid"]})
            else:
                return JSONResponse({"message" : "Notification Firebase ID Conflict"},status_code=409)
        else:
            return JSONResponse({"message" : "Invalid ID"},status_code=400)
    else:
        cnotification_doc = db.notifications.insert_one(cnotification_dict)
        cnotification_dict["nid"] = str(cnotification_doc.inserted_id)
        cunotification_doc = db.notifications.update_one({"_id": cnotification_doc.inserted_id}, {"$set": {"nid":str(cnotification_doc.inserted_id)}})
        return JSONResponse(content={"message" : "Notification Successfully Created", "nid" : cnotification_dict["nid"]})

@route.get("/readnotification/{notification_id}", status_code=200)
def read_notification(notification_id: str):
    rnotification_doc = db.notifications.find_one({"nid" : notification_id})
    if rnotification_doc:
        return JSONResponse(content=json.dumps(json_notification_doc(rnotification_doc)))
    else:
        return JSONResponse(content={"message" : "Notification Not Found"},status_code=404)

@route.put("/updatenotification/{notification_id}", status_code=200)
def update_notification(notification_id: str, update_notification_data: dict):
    notification_check = db.notifications.find_one({"nid" : notification_id})
    if notification_check:
        if "nid" in update_notification_data.keys():
            del update_notification_data["nid"]
        if "user" in update_notification_data.keys():
            del update_notification_data["user"]
        unotification_doc = db.notifications.update_one({"nid": notification_id}, {"$set": update_notification_data})
        updated_notification = db.notifications.find_one({"nid" : notification_id})
        return JSONResponse(content={"message" : "Notification Updated Successfully", "Updated Notification" : json.dumps(json_notification_doc(updated_notification))})
    else:
        return JSONResponse(content={"message" : "Notification Not Found"},status_code=404)
    
@route.delete("/deletenotification/{notification_id}", status_code=200)
def delete_notification(notification_id: str):
    # dnotification_id = ObjectId(notification_id)
    notification_check = db.notifications.find_one({"nid" : notification_id})
    if notification_check:
        deleted_notification_dict = dict(notification_check)
        deleted_notification_nid = str(deleted_notification_dict["_id"])
        dnotification_doc = db.notifications.delete_one({"nid" : notification_id})
        return JSONResponse(content={"message": "Notification Deleted","deleted_nid:" : deleted_notification_nid})
    else:
        return JSONResponse(content={"message" : "Notification Not Found"},status_code=404)
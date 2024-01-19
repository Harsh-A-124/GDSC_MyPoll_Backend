import json

def json_user_doc(user_doc) -> dict:
    return {
        "uid" : str(user_doc["_id"]),
        "firebase_uid" : str(user_doc["firebase_uid"]),
        "created_at" : user_doc["created_at"],
        "name" : user_doc["name"],
        "email" : user_doc["email"],
        "mobileno" : user_doc["mobileno"],
        # "password" : user_doc["password"],
        "complaints" : user_doc["complaints"],
        "donations" : user_doc["donations"],
        "location" : user_doc["location"],
        "type" : user_doc["type"],
    }

def json_complaints_doc(complaints_doc) -> dict:
    return {
        "cid" : str(complaints_doc["_id"]),
        "timestamp" : complaints_doc["timestamp"],
        # "user" : complaints_doc["user"],
        "user_firebase_id" : complaints_doc["user_firebase_id"],
        "category" : complaints_doc["category"],
        "description" : complaints_doc["description"],
        "area" : complaints_doc["area"],
        "address" : complaints_doc["address"],
        "images" : complaints_doc["images"],
        "status" : complaints_doc["status"]
    }

def json_donation_doc(donation_doc) -> dict:
    return {
        "did" : str(donation_doc["_id"]),
        # "user" : donation_doc["user"],
        "user_firebase_id" : donation_doc["user_firebase_id"],
        "timestamp" : donation_doc["timestamp"],
        "amount" : donation_doc["amount"],
    }

def json_notification_doc(notification_doc) -> dict:
    return {
        "nid" : str(notification_doc["_id"]),
        # "user" : notification_doc["user"],
        # "user_firebase_id" : notification_doc["user_firebase_id"],
        "timestamp" : notification_doc["timestamp"],
        "area" : notification_doc["area"],
        "message" : notification_doc["message"],
    }

def json_banner_doc(banner_doc) -> dict:
    return {
        "bid" : str(banner_doc["_id"]),
        "timestamp" : banner_doc["timestamp"],
        "image" : banner_doc["image"]
    }

def jsonify_users(user_docs) -> list:
    return [json.dumps(json_user_doc(user_doc)) for user_doc in user_docs]

def jsonify_complaintss(complaints_docs) -> list:
    return [json.dumps(json_complaints_doc(complaints_doc)) for complaints_doc in complaints_docs]

def jsonify_donations(donation_docs) -> list:
    return [json.dumps(json_donation_doc(donation_doc)) for donation_doc in donation_docs]

def jsonify_notifications(notification_docs) -> list:
    return [json.dumps(json_notification_doc(notification_doc)) for notification_doc in notification_docs]

def jsonify_banners(banner_docs) -> list:
    return [json.dumps(json_banner_doc(banner_doc)) for banner_doc in banner_docs]
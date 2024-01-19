from pymongo import MongoClient

MONGO_URI = "mongodb+srv://hankstark1204:lmfao1204@gdscmypolldb.kmjfnvw.mongodb.net/"

conn = MongoClient(MONGO_URI)
db = conn.gdsc_mypoll_backend_db
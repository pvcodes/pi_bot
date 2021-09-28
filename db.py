import json
from dotenv import load_dotenv
import os
from pymongo import MongoClient

BASEPATH = os.getcwd()
load_dotenv()

# DB_CLUSTER = os.getenv(f'DB_CLUSTER')
DB_CLUSTER = os.environ['DB_CLUSTER']
DB_NAME = os. environ['DB_NAME']
DB_UNAME = os.environ['DB_UNAME']
DB_PSWRD = os.environ['DB_PSWRD']

db_connstr = f'mongodb+srv://{DB_UNAME}:{DB_PSWRD}@{DB_CLUSTER}.dshjj.mongodb.net/{DB_NAME}?retryWrites=true&w=majority'
# print(db_connstr)

try:
    client = MongoClient(db_connstr)
    db = client['db_pibot']
    # print(db)
except Exception as e:
    db = None
    print(
        f'---------------------------\n{e}\n-----------------------------------')

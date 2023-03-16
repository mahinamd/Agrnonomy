import os
import pymongo

from Agronomy.sensitive import selfDecode
from dotenv import load_dotenv

load_dotenv()


def get_collection(index):
    client = pymongo.MongoClient(selfDecode(os.environ['HOST_LINK']) + selfDecode(os.environ['HOST_PERMISSION']))
    db = client[selfDecode(os.environ['DB_NAME'])]
    data_collection = None
    if index == 1:
        data_collection = db[selfDecode(os.environ['COLLECTION_NAME_1'])]
    elif index == 2:
        data_collection = db[selfDecode(os.environ['COLLECTION_NAME_2'])]

    return data_collection

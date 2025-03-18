from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient
load_dotenv()
import os
MONGO_DB_URL=os.getenv("str")
client=MongoClient(MONGO_DB_URL)
db=client['TnC_Analyser']
collection=db['Cluster96']

def save_to_db(text,named_entities,risk_categories,risk_score,risk_terms,summary,rc):
    entry={
        "Text":text,
        "Summary":summary,
        "keywords":named_entities,
        "Risk_categories":risk_categories,
        "Risk_terms":risk_terms,
        "Risk score":risk_score,
        "Recommendation":rc
    }
    collection.insert_one(entry)
    return entry
def find_in_db(text):
    existingif=collection.find_one({"text":text},{"_id":0})
    return existingif
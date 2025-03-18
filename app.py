from db_pipeline import save_to_db,find_in_db
from classifier import detector
from summarizer import summarize
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
load_dotenv()
import os
MONGO_DB_URL=os.getenv("str")
client=MongoClient(MONGO_DB_URL)
db=client['TnC_Analyser']
collection=db['Cluster96']
from config import SUMMARIZATION_MODEL
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from config import SPACY_MODEL
import spacy
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
app=FastAPI(title="Terms and Conditions Analyser")
origins=["http://localhost:5173","http://127.0.0.1:5173", "http://localhost:3000",
    "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
nlpmodel=spacy.load(SPACY_MODEL)
class TnCRequest(BaseModel):
    tncreq: str
def cleanout(data):
    if isinstance(data,list):
        return [{k:v for k,v in doc.items() if k!="_id"} for doc in data]
    elif isinstance(data,dict):
        return {k:v for k,v in data.items() if k!="_id"}
    return data    
@app.get('/')
def default():
    return {"Welcome":"Welcome to T&C Analyser by Rohan Mishra"}

@app.post('/analyze')
def analyser(request: TnCRequest):
    tncreq=request.tncreq
    existing_if=find_in_db(tncreq)
    if existing_if:
       response_data = jsonable_encoder(existing_if, custom_encoder={ObjectId: str})
       return JSONResponse(content=response_data)
    summary=summarize(tncreq)
    named_entities,risk_categories,risk_score,risk_terms=detector(tncreq)
    rc="Recommended: You can accept!!!" if risk_score<50.0 else "Not Recommended: You should not accept!!!"
    res=save_to_db(tncreq,named_entities,risk_categories,risk_score,risk_terms,summary,rc)
    return JSONResponse(content=cleanout(res))
if __name__=='__main__':
    uvicorn.run("app:app",host="127.0.0.1",port=8000,reload=True)



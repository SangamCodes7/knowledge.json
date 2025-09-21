# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import json
from fuzzywuzzy import process

app = FastAPI()

# Load knowledge base
with open("knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

class Query(BaseModel):
    language: str
    question: str

@app.post("/ask")
def ask_bot(query: Query):
    best_match = None
    highest_score = 0
    for item in knowledge:
        q_text = item["question"].get(query.language, "")
        score = process.extractOne(query.question, [q_text])[1]
        if score > highest_score:
            highest_score = score
            best_match = item
    if best_match and highest_score > 60:
        return {"answer": best_match["answer"][query.language]}
    else:
        return {"answer": "Sorry, I don't know the answer to that."}

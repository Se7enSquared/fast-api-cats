import json
from fastapi import FastAPI

app = FastAPI()

with open('cats.json') as f:
    cats = json.load(f)


@app.get('/')
def home():
    return {'data': 'Welcome to CatAPI'}


import json
from fastapi import FastAPI

app = FastAPI()

with open('cats.json') as f:
    cats = json.load(f)


@app.get('/')
def home():
    return {'data': 'Welcome to CatAPI'}


@app.get('/get-cat/{cat_id}')
def get_cat(cat_id: int = Path(None, description='The cat\'s id number')):
    cat_id = str(cat_id)
    return cats[cat_id]


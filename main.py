import json
from typing import Optional
from fastapi import FastAPI, Path

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


@app.get('/get-by-name/')
def get_cat_by_name(*, name: Optional[str]):
    return next(
        (cats[cat_id] for cat_id in cats
            if cats[cat_id]['name'].lower() == name.lower()),
        {'Data': 'Not found'}
    )

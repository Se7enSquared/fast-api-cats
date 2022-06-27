import json
from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Cat(BaseModel):
    name: str
    age: int
    color: str
    temperament: str
    weight_in_lbs: float
    description: str
    image: Optional[str] = None


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


@app.post("/add-cat/{cat_id}")
def add_cat(cat_id: int, cat: Cat):
    if cat_id in cats:
        return {'Error': 'Item id already exists'}

    cats[cat_id] = {
        'name': cat.name.title(),
        'age': cat.age,
        'color': cat.color.lower(),
        'temperament': cat.temperament.lower(),
        'weight_in_lbs': cat.weight_in_lbs,
        'description': cat.description,
        'image': cat.image
    }
    return cats[cat_id]

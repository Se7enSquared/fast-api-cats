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


class UpdateCat(BaseModel):
    name: Optional[str]
    age: Optional[int]
    color: Optional[str]
    temperament: Optional[str]
    weight_in_lbs: Optional[float]
    description: Optional[str]
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
            if cats[cat_id].name.lower() == name.lower()),
        {'Data': 'Not found'}
    )


@app.post("/add-cat/{cat_id}")
def add_cat(cat_id: int, cat: Cat):
    if cat_id in cats:
        return {'Error': 'Cat id already exists'}

    cats[cat_id] = cat
    return cats[cat_id]


@app.put("/edit-cat/{cat_id}")
def edit_cat(cat_id: int, cat: UpdateCat):
    if cat_id not in cats:
        return {'Error': 'Cat id not found'}

    cats[cat_id].update(cat)
    return cats[cat_id]

import json
from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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


def convert_json_to_pydantic(file: str, model: BaseModel) -> dict:
    with open(file, 'r') as f:
        items = json.loads(f.read())
        new_dict = {int(item): model(**items[item]) for item in items}
    return new_dict


cats = convert_json_to_pydantic('cats.json', Cat)

print(cats)

@app.get('/index/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request, 'cats': cats}
    return templates.TemplateResponse("index.html", context)


@app.get('/get-cats/')
def get_cats():
    return cats


@app.get('/get-cat/{cat_id}')
def get_cat(cat_id: int = Path(None, description='The cat\'s id number')):
    if cat_id not in cats:
        raise HTTPException(status_code=404, detail="Cat id not found")
    return cats[cat_id]


@app.get('/get-by-name/')
def get_cat_by_name(*, name: Optional[str]):
    for cat_id in cats:
        if cats[cat_id].name.lower() == name.lower():
            return cats[cat_id]
    raise HTTPException(status_code=404, detail=f"Cat {name} not found")


@app.post("/add-cat/")
def add_cat(cat: Cat):
    cat_id = len(cats) + 1
    if cat.name in cats:
        raise HTTPException(status_code=409,
                            detail="Cat already exists (name must be unique)")
    cats[cat_id] = cat
    return cats[cat_id]


@app.put("/edit-cat/{cat_id}")
def edit_cat(cat_id: int, cat: UpdateCat):
    if cat_id not in cats:
        raise HTTPException(status_code=404, detail="Cat id not found")

    if cat.name:
        cats[cat_id].name = cat.name
    if cat.age:
        cats[cat_id].age = cat.age
    if cat.color:
        cats[cat_id].color = cat.color
    if cat.temperament:
        cats[cat_id].temperament = cat.temperament
    if cat.weight_in_lbs:
        cats[cat_id].weight_in_lbs = cat.weight_in_lbs
    if cat.description:
        cats[cat_id].description = cat.description
    if cat.image:
        cats[cat_id].image = cat.image

    return cats[cat_id]


@app.delete("/del-cat/{cat_id}")
def del_cat(cat_id: int):
    if cat_id not in cats:
        raise HTTPException(status_code=404, detail="Cat id not found")

    cat_name = cats[cat_id].name
    del cats[cat_id]
    raise HTTPException(status_code=200, detail=f'{cat_name} deleted :(')

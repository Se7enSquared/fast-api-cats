import json
from typing import Optional

from fastapi import FastAPI, Path, Request
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


# TODO: Parse to dict so I don't have to cast to string
# values are pydantic objects
# BITE 345
with open('cats.json', 'r') as f:
    cats = json.loads(f.read())

print(cats)

@app.get('/index/', response_class=HTMLResponse)
def index(request: Request):
    context = {'request': request, 'cats': cats}
    return templates.TemplateResponse("index.html", context)


#Todo: Add back the get-all-cats

@app.get('/get-cat/')
def get_cat(cat_id: int = Path(None, description='The cat\'s id number')):
    cat_id = str(cat_id)
    if cat_id not in cats:
        return {'Error': 'Cat does not exist'}
    # because json doesn't allow int objects as keys,
    # have to convert to string
    return cats[cat_id]


@app.get('/get-by-name/')
def get_cat_by_name(*, name: Optional[str]):
    return next(
        (cats[cat_id] for cat_id in cats
         if cats[cat_id]['name'].lower() == name.lower()),
        {'Data': 'Not found'}
    )

# TODO: Convert json to pydantic objects
# TODO:
#     if entry_id not in food_log:
#         raise HTTPException(status_code=404, detail="Food entry not found")
# TODO: Also do for get-cat-by-name Read this: https://stackoverflow.com/questions/11746894/what-is-the-proper-rest-response-code-for-a-valid-request-but-an-empty-data
# TODO: get next cat id and assign
# TODO: Get rid of cat_id being passed in
@app.post("/add-cat/")
def add_cat(cat: Cat):
    # TODO: Generate a new id in here with len(cats)
    if cat.name in cats:
        return {'Error': 'Cat id already exists'}

    cats[cat.id] = cat
    return cats[cat.id]


@app.put("/edit-cat/{cat_id}")
def edit_cat(cat_id: int, cat: UpdateCat):
    cat_id = str(cat_id)
    if cat_id not in cats:
        return {'Error': 'Cat id not found'}

    # TODO: Fix. I know this must be bad code.
    if cat.name:
        cats[cat_id]['name'] = cat.name
    if cat.age:
        cats[cat_id]['age'] = cat.age
    if cat.color:
        cats[cat_id]['color'] = cat.color
    if cat.temperament:
        cats[cat_id]['temperament'] = cat.temperament
    if cat.weight_in_lbs:
        cats[cat_id]['weight_in_lbs'] = cat.weight_in_lbs
    if cat.description:
        cats[cat_id]['description'] = cat.description
    if cat.image:
        cats[cat_id]['image'] = cat.image

    return cats[cat_id]


@app.delete("/del-cat/{cat_id}")
def del_cat(cat_id: int):
    cat_id = str(cat_id)
    if cat_id not in cats:
        return {'Error': 'Cat does not exist'}

    cat_name = cats[cat_id]['name']
    del cats[cat_id]
    return {'Data': f'{cat_name} deleted :('}

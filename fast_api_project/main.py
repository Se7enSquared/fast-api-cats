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
    """ Pydantic model for a cat """
    name: str
    age: int
    color: str
    temperament: str
    weight_in_lbs: float
    description: str
    image: Optional[str] = None


class UpdateCat(BaseModel):
    """ Pydantic model for updating a cat including
        optional parameters for partial edits """
    name: Optional[str]
    age: Optional[int]
    color: Optional[str]
    temperament: Optional[str]
    weight_in_lbs: Optional[float]
    description: Optional[str]
    image: Optional[str] = None


def load_data(file: str, model: BaseModel) -> dict:
    """ load json file data into a dict of given pydantic model """
    with open(file, 'r') as f:
        items = json.loads(f.read())
        new_dict = {int(item): model(**items[item]) for item in items}
    return new_dict


cats = load_data('fast_api_project/cats.json', Cat)


@app.get('/index/', response_class=HTMLResponse)
def index(request: Request):
    """ returns jinja template with cat data to index route """
    context = {'request': request, 'cats': cats}
    return templates.TemplateResponse("index.html", context)


@app.get('/get-cats/')
def get_cats():
    """ return all cats """
    return cats


@app.get('/get-cat/{cat_id}')
def get_cat(cat_id: int = Path(None, description='The cat\'s id number')):
    """ get cat by given id """
    if cat_id not in cats:
        raise HTTPException(status_code=404, detail="Cat id not found")
    return cats[cat_id]


@app.get('/get-by-name/')
def get_cat_by_name(*, name: Optional[str]):
    """ return cat which matches the given name """
    return next(
        (cats[cat_id] for cat_id in cats
            if cats[cat_id].name.lower() == name.lower()),
        {}
    )


@app.post("/add-cat/", status_code=200)
def add_cat(cat: Cat):
    """ add a cat to the dict """
    cat_id = len(cats) + 1
    if cat.name in cats:
        raise HTTPException(status_code=409,
                            detail="Cat already exists (name must be unique)")
    cats[cat_id] = cat
    return cats[cat_id]


@app.patch("/edit-cat/{cat_id}", status_code=200)
def edit_cat(cat_id: int, cat: UpdateCat):
    """ edit data for the given cat id
        accepts partial data """
    if cat_id not in cats:
        raise HTTPException(status_code=404, detail="Cat id not found")

    update_cat = cats[cat_id]
    update_fields = {
        key: value for key, value in cat.dict().items() if value is not None
    }
    for key, value in update_fields.items():
        setattr(update_cat, key, value)

    return update_cat


@app.delete("/del-cat/{cat_id}", status_code=204)
def del_cat(cat_id: int):
    """ delete the cat for the given id """
    if cat_id not in cats:
        raise HTTPException(status_code=404, detail="Cat id not found")

    del cats[cat_id]
    return {"ok": True}

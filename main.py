from enum import Enum
from fastapi import FastAPI

app = FastAPI()


class PropertyModel(str, Enum):
    property1 = 'property1'
    property2 = 'property2'
    property3 = 'property3'


@app.get("/")
async def root():
    return {"message": "Hi Mom"}


@app.get("/test/{test_property}")
async def test(test_property: PropertyModel):
    if test_property == PropertyModel.property1:
        return {"property_name": "property1", "property_value": "value1"}
    if test_property == PropertyModel.property2:
        return {"property_name": "property2", "property_value": "value2"}
    if test_property == PropertyModel.property3:
        return {"property_name": "property3", "property_value": "value3"}


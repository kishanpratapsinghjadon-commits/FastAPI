from fastapi import FastAPI , Path ,  HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated
import json

app = FastAPI()

class pateint(BaseModel):

    id:Annotated[int, Field(..., description='Id of the pateint', examples=['01'])]
    name:Annotated[str , Field(..., description='Name of the pateint')]
    age:Annotated[int, Field(...,gt=0, lt=150 , description='Age of the pateint')]
    weight:Annotated[float, Field(..., gt=0, description='Weight of he pateint')]
    height:Annotated[float , Field(..., gt=0, description='Heght of the pateint')]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi


def load_data():
    with open('pateint.json' , 'r') as f:
            data = json.load(f)
            return data 

def save_data(data):
    with open('pateint.json' , 'w') as f:
            data = json.dump(data, f)            

   

@app.get("/")
def hello():
    return {"Pateint management system API"}

@app.get("/about")
def about():
    return {"A fully funtional Api to manage pateint records"}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/pateint/{pateint_id}')
def view_pateint(pateint_id: int = Path(..., description='ID of the pateint in DB', examples={'example1': {'summary': 'Example patient ID', 'value': 1}})):
    
    data = load_data()

    for pateint in data:
        if pateint.get("id") == pateint_id:
            return pateint
    raise HTTPException(status_code=404, detail='pateint data not found')

@app.get('/sort')
def sort_pateints(sort_by : str = Query(..., description='sort on the basis of height , weight_kg or bmi') , order : str = Query("asc", description = "sort in asc or desc order")):
    valid_fields =['height' , 'weight_kg' , 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 , detail='Invalid field slect from{valid_filds}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400 , detail = 'Invalid order selected')

    data = load_data()

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data, key = lambda x: x.get(sort_by, 0), reverse = sort_order)

    return sorted_data

@app.post('/create')
def create_pateint(pateint:pateint):

    #load existing data
    data = load_data()

    # Check whether a record with this ID already exists.
    if any(existing.get("id") == pateint.id for existing in data):
        raise HTTPException(status_code=400, detail= 'Pateint already exists')

    # Add the patient while preserving the JSON file's list structure.
    data.append(pateint.model_dump())

    #save into json file
    save_data(data)

    return JSONResponse(status_code=201 , content={'message': 'pateint created succesfully'})
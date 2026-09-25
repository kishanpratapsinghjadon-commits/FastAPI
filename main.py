from fastapi import FastAPI , Path ,  HTTPException , Query
import json

app = FastAPI()

def load_data():
    with open('pateint.json' , 'r') as f:
            data = json.load(f)

    return data 

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
def view_pateint(pateint_id: int = Path(..., description='ID of the pateint in DB', example='1')):
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
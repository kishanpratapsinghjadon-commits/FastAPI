from fastapi import FastAPI
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
def view_pateint(pateint_id: int):
    data = load_data()

    for pateint in data:
        if pateint.get("id") == pateint_id:
            return pateint
    return {'error': 'pateint data not found'}


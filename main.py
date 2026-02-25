from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def patients_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data    


@app.get("/")
def root():
    return {"message": "Hello Patients"}

@app.get("/patients")
def patients():
    return("message:List Of Patients")

@app.get("/view")
def view():
    data=patients_data()
    return data

@app.get('/Single/{patient_id}')
def view_Single(patient_id:str=Path (...,description="patient id required",example='P001')):
 with open("patients.json",'r') as f:    
    data= json.load(f)
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(404,detail="patient not found")

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sort by patients id,height,bmi'),
order:str=Query('asc',description='Sort from asc to dsc or dsc to asc')):
    
     valid_fields = ['height','weight','bmi']
     
     if sort_by not in valid_fields:
         raise HTTPException(status_code=400,detail='Invalid Fild select from {valid_fileds}')
     
     if order not in ['asc','dsc']:
         raise HTTPException(status_code=400,detail='Invalid Order in asc or dsc')
     
     data=patients_data()
     
     sort_order= True if order=='dsc'else False
     
     sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)
     
     return sorted_data
     
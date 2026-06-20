import joblib
import pandas as pd
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from sklearn.preprocessing import LabelEncoder

import tables
import schemas
from database import engine,get_db

tables.base.metadata.create_all(bind=engine)

app = FastAPI(title="Heart disease prediction using API")

model = joblib.load('model.pkl')
columns = joblib.load("columns.pkl")

le = LabelEncoder()
binary_col = ['sex','fbs','exang']

def predict(data: dict):
    df = pd.DataFrame([data])

    df['sex'] = df['sex'].map({'Male': 1, 'Female': 0})
    df['fbs'] = df['fbs'].map({'True': 1, 'False': 0, True: 1, False: 0})
    df['exang'] = df['exang'].map({'True': 1, 'False': 0, True: 1, False: 0})

    df = pd.get_dummies(df, columns=['cp', 'thal', 'restecg', 'slope'], drop_first=True)
    df = df.reindex(columns=columns, fill_value=0)

    pred = model.predict(df)[0]
    return int(pred)

@app.post("/predict",response_model=schemas.Response)
def add(patient: schemas.Input, db:Session = Depends(get_db)):
    pred = predict(patient.model_dump())

    db_patient = tables.Patient(
        age=patient.age,
        sex=patient.sex,
        cp=patient.cp,
        trestbps=patient.trestbps,
        chol=patient.chol,
        fbs=patient.fbs,
        restecg=patient.restecg,
        thalch=patient.thalch,
        exang=patient.exang,
        oldpeak=patient.oldpeak,
        slope=patient.slope,
        ca=patient.ca,
        thal=patient.thal,
        prediction=pred
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient

@app.get("/patients",response_model=list[schemas.Response])
def get_all(db : Session=Depends(get_db)):
    return db.query(tables.Patient).all()

@app.get("/patient/{p_id}",response_model=schemas.Response)
def get_patient(p_id:int,db:Session = Depends(get_db)):
    exist = db.query(tables.Patient).filter(tables.Patient.id == p_id).first()
    if not exist:
        raise HTTPException(status_code=404,detail='patient not found')

    return exist

@app.put("/patient/{p_id}",response_model=schemas.Response)
def update_patient(p_id:int,updated:schemas.Input,db:Session=Depends(get_db)):
    exist = db.query(tables.Patient).filter(tables.Patient.id == p_id).first()
    if not exist:
        raise HTTPException(status_code=404,detail='patient not found')

    for key,value in updated.model_dump().items():
        setattr(exist,key,value)

    pred = predict(updated.model_dump())
    exist.prediction = pred

    db.commit()
    db.refresh(exist)
    return exist

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(tables.Patient).filter(tables.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return {"message": f"Patient {patient_id} deleted successfully"}

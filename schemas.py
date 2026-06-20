# schemas

from pydantic import BaseModel

class Input(BaseModel):
    age: int
    sex: str
    cp: str
    trestbps: float
    chol: float
    fbs: str
    restecg: str
    thalch: float
    exang: str
    oldpeak: float
    slope: str
    ca: float
    thal: str

class Response(BaseModel):
    id:         int
    age:        int
    sex:        str
    prediction: int

    class Config:
        from_attributes = True


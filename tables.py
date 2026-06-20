#tables file

from sqlalchemy import Column,String,Integer,Float
from database import base

class Patient(base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    sex = Column(String)
    cp = Column(String)
    trestbps = Column(Float)
    chol = Column(Float)
    fbs = Column(String)
    restecg = Column(String)
    thalch = Column(Float)
    exang = Column(String)
    oldpeak = Column(Float)
    slope = Column(String)
    ca = Column(Float)
    thal = Column(String)
    prediction = Column(Integer)


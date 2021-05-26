"""Machine learning functions"""

# import logging
import joblib

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, validator

# log = logging.getLogger(__name__)
router = APIRouter()

templates = Jinja2Templates(directory="app/frontend/templates/")

model = joblib.load("app/ml_viz/model.joblib")

# class Item(BaseModel):
#     """Use this data model to parse the request body JSON."""

#     x1: float = Field(..., example=3.14)
#     x2: int = Field(..., example=-42)
#     x3: str = Field(..., example='banjo')

#     def to_df(self):
#         """Convert pydantic object to pandas dataframe with 1 row."""
#         return pd.DataFrame([dict(self)])

#     @validator('x1')
#     def x1_must_be_positive(cls, value):
#         """Validate that x1 is a positive number."""
#         assert value > 0, f'x1 == {value}, must be > 0'
#         return value


# @router.post('/predict')
# async def predict(item: Item):
#     """
#     Make random baseline predictions for classification problem 🔮
#     ### Request Body
#     - `x1`: positive float
#     - `x2`: integer
#     - `x3`: string
#     ### Response
#     - `prediction`: boolean, at random
#     - `predict_proba`: float between 0.5 and 1.0, 
#     representing the predicted class's probability
#     Replace the placeholder docstring and fake predictions with your own model.
#     """
#     X_new = item.to_df()
#     log.info(X_new)
#     y_pred = random.choice([True, False])
#     y_pred_proba = random.random() / 2 + 0.5
#     return {
#         'prediction': y_pred,
#         'probability': y_pred_proba
#     }

@router.get('/prediction', response_class=HTMLResponse)
def display_index(request: Request):
    return templates.TemplateResponse('prediction.html', {"request": request})

@router.post('/prediction')
async def predict(property_type, room_type, accommodates, bathrooms, bedrooms, beds, city):
    df = pd.DataFrame(columns=["property_type", "room_type", "accommodates", "bathrooms", "bedrooms", "beds", "city"],
    data=[[property_type, room_type, accommodates, bathrooms, bedrooms, beds, city]])
    y_pred = model.predict(df)[0][0]
    result = np.exp(y_pred)
    return np.round(result, 2)

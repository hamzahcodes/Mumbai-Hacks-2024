from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pandas as pd
from pydantic import BaseModel

analytics_router = APIRouter()

class Item(BaseModel):
    income_level: dict
    region: dict
    product_month: list[list]
    place_festival: list[list]

months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

@analytics_router.get('/')
async def get_chart_data():
    df = pd.read_csv('C:/Users/Zakia/Desktop/Pr/fastapi/customer_data.csv')

    income_level = df['Income Level'].value_counts().to_dict()
    region = df['Region'].value_counts().to_dict()
    df['Month'] = pd.DatetimeIndex(df['Last Purchase Date']).month
    df['Month'] = df['Month'].map(months)
    products = df.groupby(['Month', 'Purchase History']).size().reset_index(name='Count')
    # print(products.columns)
    products_month = [
        products['Month'].to_list(), products['Purchase History'].to_list(), products['Count'].to_list(), 
    ]
    # print(products_month)

    urban_rural = df.groupby(['Urban/Rural', 'Festival Engagement']).size().reset_index(name='Count')
    place_festival = [
        urban_rural['Urban/Rural'].to_list(), urban_rural['Festival Engagement'].to_list(), urban_rural['Count'].to_list(), 
    ]
    print(place_festival)

    json_compatible_item_data = jsonable_encoder(Item(income_level=income_level, region=region, product_month=products_month, place_festival=place_festival))
    return JSONResponse(content=json_compatible_item_data)
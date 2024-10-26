from fastapi import FastAPI
from src.analytics.routes import analytics_router
from src.models.routes import models_router
from src.predict.routes import predict_router
from fastapi.middleware.cors import CORSMiddleware

version = 'v1'

app = FastAPI(
    title='InsightCRM APIs',
    description='A RESTful API for a insight CRM data',
    version=version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router,prefix=f"/api/{version}/analytics", tags=['analytics'])
app.include_router(models_router,prefix=f"/api/{version}/models", tags=['models'])
app.include_router(predict_router,prefix=f"/api/{version}/predict", tags=['predict'])
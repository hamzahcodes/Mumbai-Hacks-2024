from fastapi import APIRouter
from pydantic import BaseModel
from src.models.data import model_metrics

models_router=APIRouter()

class MLModel(BaseModel):
    model_name: str
    silhouette_score: float
    davies_bouldin_index: float
    calinski_harabasz_index: float


@models_router.get('/', response_model=list[MLModel])
async def get_trained_models():
    print(model_metrics)
    return model_metrics


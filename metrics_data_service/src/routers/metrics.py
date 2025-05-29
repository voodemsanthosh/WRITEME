from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, dependencies # Updated relative imports

router = APIRouter(
    tags=["metrics"], # Add tags for OpenAPI docs
)

@router.post("/metrics/", response_model=schemas.Metric)
def create_metric_endpoint(
    metric: schemas.MetricCreate, db: Session = Depends(dependencies.get_db)
):
    # TODO: Add more specific error handling if needed
    return crud.create_metric(db=db, metric=metric)

@router.get("/metrics/", response_model=List[schemas.Metric])
def read_metrics_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    metrics = crud.get_metrics(db, skip=skip, limit=limit)
    return metrics

@router.get("/metrics/{metric_id}", response_model=schemas.Metric)
def read_metric_endpoint(metric_id: int, db: Session = Depends(dependencies.get_db)):
    db_metric = crud.get_metric(db, metric_id=metric_id)
    if db_metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return db_metric

@router.get("/metrics-data", response_model=List[schemas.Metric])
def get_metrics_data( # Renamed function, made it synchronous
    skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)
):
    metrics = crud.get_metrics(db=db, skip=skip, limit=limit)
    return metrics

# TODO: Add endpoints for updating and deleting metrics
# @router.put("/metrics/{metric_id}", response_model=schemas.Metric)
# def update_metric_endpoint(...):
#     pass

# @router.delete("/metrics/{metric_id}", response_model=schemas.Metric) # Or just a status code
# def delete_metric_endpoint(...):
#     pass

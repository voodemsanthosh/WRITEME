from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_metric(db: Session, metric_id: int):
    return db.query(models.Metric).filter(models.Metric.id == metric_id).first()

def get_metrics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Metric).offset(skip).limit(limit).all()

def create_metric(db: Session, metric: schemas.MetricCreate):
    db_metric = models.Metric(
        name=metric.name,
        value=metric.value,
        source=metric.source,
        timestamp=metric.timestamp if metric.timestamp else datetime.utcnow()
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

# TODO: Implement update_metric and delete_metric functions
# def update_metric(db: Session, metric_id: int, metric_update: schemas.MetricUpdate):
#     pass

# def delete_metric(db: Session, metric_id: int):
#     pass

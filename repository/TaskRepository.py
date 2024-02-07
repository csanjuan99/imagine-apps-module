import models.Task as Task
from schemas.Task import Task as TaskModel
from sqlalchemy.orm import Session


def get_tasks_by_user_id(db: Session, user_id: int) -> list[TaskModel]:
    return db.query(Task).filter(Task.user_id == user_id).all()


def get_task_by_id(db: Session, task_id: int) -> TaskModel:
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, user_id: int, title: str, description: str):
    db_task = Task(user_id=user_id, description=description, title=title)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def remove_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return db_task


def update_task(db: Session, task_id: int, title: str, description: str, completed: bool):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db_task.title = title
    db_task.description = description
    db_task.completed = completed
    db.commit()
    db.refresh(db_task)
    return db_task

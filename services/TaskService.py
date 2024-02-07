from repository import TaskRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.Task import Task


def get_task_by_id(db: Session, task_id: int) -> Task:
    task = TaskRepository.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


def get_tasks_by_user_id(db: Session, user_id: int) -> list[Task]:
    tasks = TaskRepository.get_tasks_by_user_id(db, user_id)
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found")
    return tasks


def create_task(db: Session, user_id: int, title: str, description: str) -> Task:
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is required")
    if not title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required")
    return TaskRepository.create_task(db, user_id, title, description)


def remove_task(db: Session, task_id: int) -> Task:
    if not task_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task ID is required")
    task = get_task_by_id(db, task_id)
    return TaskRepository.remove_task(db, task.id)


def update_task(db: Session, task_id: int, title: str, description: str, completed: bool) -> Task:
    if not task_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task ID is required")
    task = get_task_by_id(db, task_id)
    return TaskRepository.update_task(db, task.id, title, description, completed)

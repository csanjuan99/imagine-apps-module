import services.TaskService as TaskService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sql_app.database import get_db
from schemas.Task import TaskCreate, Task, TaskUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get('/tasks/{user_id}', response_model=list[Task])
async def read_tasks_by_user_id(token: Annotated[str, Depends(oauth2_scheme)], user_id: int,
                                db: Session = Depends(get_db)):
    return TaskService.get_tasks_by_user_id(db, user_id)


@router.post('/tasks/{user_id}', response_model=Task)
async def create_task(token: Annotated[str, Depends(oauth2_scheme)], user_id: int, task: TaskCreate,
                      db: Session = Depends(get_db)):
    return TaskService.create_task(db, user_id, task.title, task.description)


@router.delete('/tasks/{task_id}', response_model=Task)
async def remove_task(token: Annotated[str, Depends(oauth2_scheme)], task_id: int, db: Session = Depends(get_db)):
    return TaskService.remove_task(db, task_id)


@router.put('/tasks/{task_id}', response_model=Task)
async def update_task(token: Annotated[str, Depends(oauth2_scheme)], task_id: int, task: TaskUpdate,
                      db: Session = Depends(get_db)):
    return TaskService.update_task(db, task_id, task.title, task.description, task.completed)

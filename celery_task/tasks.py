from celery import shared_task
from sqlalchemy.orm import Session
from schemas import CreateAndUpdateGazeInfo
from typing import List
from fastapi import HTTPException
from database import get_db
from models import GazeInfo
from sqlalchemy.exc import SQLAlchemyError

@shared_task(bind=True, autoretry_for=(SQLAlchemyError,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='gaze_infos_1:create_gaze_info_tasks_1')
def create_gaze_info_tasks_1(self, gaze_info: List[CreateAndUpdateGazeInfo], session: Session = None) -> str:
    try:
        if session is None:
            session = next(get_db())

        
        chunk_size = 100  
        for i in range(0, len(gaze_info), chunk_size):
            chunk = gaze_info[i:i + chunk_size]
            new_gaze_infos = [GazeInfo(**tempData.dict()) for tempData in chunk]
            session.bulk_save_objects(new_gaze_infos)
        
        session.commit()
        return "task executed in db"
    except SQLAlchemyError as e:
        return f"Error during database operation: {str(e)}"


# @shared_task(bind=True, autoretry_for=(SQLAlchemyError,), retry_backoff=True, retry_kwargs={"max_retries": 5},
#              name='gaze_infos_2:create_gaze_info_tasks_2')
# def create_gaze_info_tasks_2(self, gaze_info: List[CreateAndUpdateGazeInfo], session: Session = None) -> str:
#     try:
#         if session is None:
#             session = next(get_db())

        
#         chunk_size = 100  
#         for i in range(0, len(gaze_info), chunk_size):
#             chunk = gaze_info[i:i + chunk_size]
#             new_gaze_infos = [GazeInfo(**tempData.dict()) for tempData in chunk]
#             session.bulk_save_objects(new_gaze_infos)
        
#         session.commit()
#         return "task executed in db"
#     except SQLAlchemyError as e:
#         return f"Error during database operation: {str(e)}"

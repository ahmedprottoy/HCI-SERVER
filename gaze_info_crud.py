from typing import List
from sqlalchemy.orm import Session
from exceptions import StudentInfoNotFoundError, StudentInfoInfoAlreadyExistError
from models import GazeInfo
from schemas import CreateAndUpdateGazeInfo
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy import func
from typing import Optional


def create_gaze_info(session : Session ,gaze_info: CreateAndUpdateGazeInfo) -> str:
    try:
        new_gaze_info = GazeInfo(**gaze_info.dict())
        session.add(new_gaze_info)
        session.commit()
    except Exception as e:
        print(e)
    
    return "Gaze Info Created"


def get_gaze_infos(session: Session, limit: int, offset: int) -> List[GazeInfo]:
    return session.query(GazeInfo).offset(offset).limit(limit).all()

    
def get_gaze_infos_by_student_id(session: Session, student_id: int, start_timestamp: str, end_timestamp: str, limit: Optional[int] = None, offset: Optional[int] = None) -> List[GazeInfo]:
    try:
        query = session.query(GazeInfo).filter(
            GazeInfo.student_id == student_id,
            GazeInfo.Timestamp >= start_timestamp,
            GazeInfo.Timestamp <= end_timestamp
        )

        if limit is not None:
            query = query.limit(limit)
        
        if offset is not None:
            query = query.offset(offset)
        
        return query.all()
    except Exception as e:
        raise e


def get_gaze_count(session: Session) -> int:
    count = session.query(func.count(GazeInfo.id)).scalar()
    return count

def truncate_gaze_table(session: Session):
    session.query(GazeInfo).delete()
    session.commit()
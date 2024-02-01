from typing import List
from sqlalchemy.orm import Session
from exceptions import StudentInfoNotFoundError, StudentInfoInfoAlreadyExistError
from models import GazeInfo
from schemas import CreateAndUpdateGazeInfo
from fastapi import APIRouter, Depends, HTTPException
from database import get_db


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

def get_gaze_info_count(session: Session) -> int:
    return session.query(GazeInfo).count()
from typing import List
from sqlalchemy.orm import Session
from exceptions import StudentInfoNotFoundError, StudentInfoInfoAlreadyExistError
from models import StudnetInfo, ClassTimestampRecord
from schemas import CreateAndUpdateStudent, ClassTimestampSingleRecord

def get_all_student(session: Session, limit: int, offset: int) -> List[StudnetInfo]:
    return session.query(StudnetInfo).offset(offset).limit(limit).all()


def get_student_info_by_id(session: Session, _id: int) -> StudnetInfo:
    student_info = session.query(StudnetInfo).get(_id)

    if student_info is None:
        raise StudentInfoNotFoundError

    return student_info

def get_student_info_by_email(session: Session, _email : str) -> StudnetInfo:
    student_info = session.query(StudnetInfo).filter(StudnetInfo.email == _email).first()

    if student_info is None:
        raise StudentInfoNotFoundError
    
    return student_info


def create_student(session: Session, student_info: CreateAndUpdateStudent) -> StudnetInfo:
    student_details = session.query(StudnetInfo).filter(StudnetInfo.email == student_info.email).first()
    if student_details is not None:
        return student_details

    new_Student_info = StudnetInfo(**student_info.dict())
    session.add(new_Student_info)
    session.commit()
    session.refresh(new_Student_info)
    return new_Student_info


def add_class_record(session: Session, class_time_stamp: ClassTimestampSingleRecord) -> ClassTimestampRecord:
    try:
        single_class_record = ClassTimestampRecord(**class_time_stamp.dict())
        session.add(single_class_record)
        session.commit()
        session.refresh(single_class_record)
        return single_class_record
    except Exception as ex:
        print(ex)
        return None
    
def get_class_records(session: Session) -> List[ClassTimestampRecord]:
    return session.query(ClassTimestampRecord).all()
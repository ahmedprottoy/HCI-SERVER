from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from student_crud import get_all_student, get_student_info_by_id, create_student, get_student_info_by_email, add_class_record
from database import get_db
from exceptions import InfoException
from schemas import Student, CreateAndUpdateStudent, PaginatedStudentInfo, ClassTimestampRecord, ClassTimestampSingleRecord


router = APIRouter()

@cbv(router)
class Student:
    session: Session = Depends(get_db)

    @router.get("/students", response_model=PaginatedStudentInfo)
    def list_student(self, limit: int = 10, offset: int = 0):

        students_list = get_all_student(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": students_list}

        return response
    
    @router.post("/students")
    def add_student(self, student_info: CreateAndUpdateStudent):

        try:
            student_info = create_student(self.session, student_info)
            return student_info
        except InfoException as cie:
            raise HTTPException(**cie.__dict__)
    
    @router.get("/students/{student_id}", response_model=Student)
    def get_student_info(self, student_id: int):
        try:
            student_info = get_student_info_by_id(self.session, student_id)
            return student_info
        except InfoException as cie:
            raise HTTPException(**cie.__dict__)
    
    @router.get("/student", response_model=Student)
    def get_student_info_by_email(self, email: str):
        try:
            student_info = get_student_info_by_email(self.session, email)
            return student_info
        except InfoException as cie:
            raise HTTPException(**cie.__dict__)

    @router.post("/teacher/addRecord")
    def add_class_record_to_db(self, classRecord: ClassTimestampSingleRecord):
        added_record = add_class_record(self.session, classRecord)
        if added_record == None:
            raise HTTPException(500, "Could not add record")
        return add_class_record
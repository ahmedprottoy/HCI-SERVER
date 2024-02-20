from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from gaze_info_crud import create_gaze_info, get_gaze_infos,  get_gaze_infos_by_student_id,get_gaze_count,truncate_gaze_table
from database import get_db
from schemas import GazeInfo, PaginatedGazeInfo, CreateAndUpdateGazeInfo
from typing import List
from celery_task.tasks import create_gaze_info_tasks_1

router = APIRouter()

@cbv(router)
class GazeInfo:
    session: Session = Depends(get_db)

    @router.post("/gaze")
    async def add_gazeInfo(self, gaze_info: List[CreateAndUpdateGazeInfo]):

        try:
            gaze_task = create_gaze_info_tasks_1.apply_async(args=[gaze_info])
            return str(gaze_task.id)
            # for tempData in gaze_info:
                # print(tempData.dict())
                # gaze_info = create_gaze_info(self.session, tempData)
                 
                
            
        except Exception as cie:
            print(**cie.__dict__)

    
    @router.get("/gaze", response_model=PaginatedGazeInfo)
    def list_gaze_info(self, limit: int = 10, offset: int = 0):

        gaze_list = get_gaze_infos(self.session, limit, offset)
        response = {"limit": limit, "offset": offset, "data": gaze_list}

        return response

    @router.get("/gaze/{student_id}")
    async def get_gaze_info_by_student_id(self, student_id: int, start_timestamp: str, end_timestamp: str, limit: int = 10, offset: int = 0):
        try:
            gaze_list = get_gaze_infos_by_student_id(
                self.session, student_id, start_timestamp, end_timestamp, limit, offset
            )
            response = {
                "student_id": student_id,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "data": gaze_list,
            }
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    @router.put("/gaze/{student_id}")
    async def update_gaze_info_by_student_id(self, student_id: int, start_timestamp: str, end_timestamp: str):
        try:
            gaze_list = get_gaze_infos_by_student_id(
                self.session, student_id, start_timestamp, end_timestamp
            )
            
            for gaze_info in gaze_list:
                gaze_info.isMindWandered = True
                
            self.session.commit()
            
            return {"message": "Gaze info updated successfully"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
    @router.get("/gaze_count")
    def get_gaze_count(self):
        count = get_gaze_count(self.session)
        return {"count": count}


    @router.delete("/gaze/truncate")
    def truncate_gaze_table(self):
        truncate_gaze_table(self.session)
        return {"message": "Gaze table truncated successfully"}

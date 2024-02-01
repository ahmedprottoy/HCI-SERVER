from PyTrack.Stimulus import Stimulus
import pandas as pd
import numpy as np
import os
from sqlalchemy.orm import Session
from models import GazeInfo, StudnetInfo, GazeInfoDerived
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import itertools
from sqlalchemy import update, insert
from config import DB_URL

def _batch_iter(n, iterable):
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            return
        yield batch

def main():
    
    analysis_fold = os.path.abspath("PyTrack_Sample_Data/SMI" )
    dfname = "smi_eyetracker_freeviewing.csv"
    dfpath = '{}/{}'.format(analysis_fold, dfname)
    DATABASE_URL = DB_URL

    db_engine = create_engine(DATABASE_URL, echo = False)
    SessionLocal = sessionmaker(bind=db_engine)
    db = SessionLocal()

    students = db.query(StudnetInfo).all()
    
    for student in students:
        query = db.query(GazeInfo).order_by(GazeInfo.Timestamp).filter(GazeInfo.student_id == student.id).execution_options(stream_results=True)

        sensor_dict = {
            "EyeTracker":
            {
            "Sampling_Freq": 1000,
            "Display_width": student.displayWidth,
            "Display_height": student.displayHeight,
            "aoi": [0, 0, student.displayWidth, student.displayHeight]
            }
        }
        batchNo = 1
        
        for batch in _batch_iter(2000, query):
            df = pd.DataFrame(columns = ['Timestamp',	'StimulusName',	'EventSource', 'GazeLeftx',	'GazeRightx',	'GazeLefty',	'GazeRighty',	'PupilLeft',	'PupilRight',	'FixationSeq',	'SaccadeSeq',	'Blink',	'GazeAOI'])
            for datumn in batch:
                # print(datumn.Timestamp + " : " + str(datumn.id))
                new_row = {
                    'Timestamp' : datumn.Timestamp,
                    'StimulusName' : 'stimulus_0',
                    'EventSource' : 'ET',
                    'GazeLeftx' : datumn.GazeLeftx,
                    'GazeRightx' : datumn.GazeRightx,
                    'GazeLefty' : datumn.GazeLefty,
                    'GazeRighty' : datumn.GazeRighty,
                    'PupilLeft' : datumn.PupilLeft,
                    'PupilRight' : datumn.PupilRight,
                    'FixationSeq' : datumn.FixationSeq,
                    'SaccadeSeq' : datumn.SaccadeSeq,
                    'Blink' : datumn.Blink,
                    'GazeAOI' : datumn.GazeAOI
                    }
                try:
                    up = update(GazeInfo).values({"batchNo" : batchNo}).where(GazeInfo.id == datumn.id)
                    db.execute(up)
                    db.commit()
                except:
                    print("Error occured while updating gaze info of student : " + str(student.id) + " data id : " + str(datumn.id) + " , batch : " + str(batchNo))
                
                df = pd.concat([df, pd.DataFrame.from_dict([new_row])])

            print("Update done for batch : " + str(batchNo) + ", Student id : " + str(student.id))
                
            
            df['PupilLeft']  = df['PupilLeft'] * 0.2645833333
            df['PupilRight']  = df['PupilRight'] * 0.2645833333

            if(df.size != 0):
                
                stim = Stimulus(path=analysis_fold, data=df, sensor_names=sensor_dict)
                stim.findEyeMetaData()
                features = stim.sensors["EyeTracker"].metadata 

                for i in range(len(features['sacc_vel'])):
                    _in = insert(GazeInfoDerived).values(
                        time_to_peak_pupil = features['time_to_peak_pupil'],
                        peak_pupil = features['peak_pupil'],
                        pupil_mean = features['pupil_mean'],
                        pupil_slope = features['pupil_slope'],
                        pupil_area_curve = features['pupil_area_curve'],
                        blink_rate = features['blink_rate'],
                        peak_blink_duration = features['peak_blink_duration'],
                        avg_blink_duration = features['avg_blink_duration'],
                        fixation_count = features['fixation_count'],
                        max_fixation_duration = features['max_fixation_duration'],
                        avg_fixation_duration = features['avg_fixation_duration'],
                        sacc_count  = features['sacc_count'],
                        sacc_duration = features['sacc_duration'][i],
                        sacc_vel = features['sacc_vel'][i],
                        sacc_amplitude  = features['sacc_amplitude'][i],
                        micro_sacc_count  = features['ms_count'],
                        first_pass_duration  = features['first_pass_duration'],
                        second_pass_duration = features['second_pass_duration'],
                        batchNo = batchNo
                        )
                    db.execute(_in)
                    db.commit()
                print("Write done for derived value for batch : " + str(batchNo) + " ,Student id : " + str(student.id))
                batchNo = batchNo + 1
                    
               
if __name__ == "__main__":
    main()
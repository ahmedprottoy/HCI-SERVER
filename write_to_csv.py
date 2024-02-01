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
import csv


def _batch_iter(n, iterable):
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            return
        yield batch


def main():

    analysis_fold = os.path.abspath("PyTrack_Sample_Data/SMI")
    dfname = "smi_eyetracker_freeviewing.csv"
    dfpath = '{}/{}'.format(analysis_fold, dfname)
    DATABASE_URL = DB_URL

    db_engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=db_engine)
    db = SessionLocal()

    students = db.query(StudnetInfo).all()

    csv_file_path = "data.csv"
    print("writing started ... \n")
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['id', 'student_id', 'Timestamp', 'GazeX', 'GazeY',
                      'GazeLeftx', 'GazeLefty', 'GazeRightx', 'GazeRighty',
                      'PupilLeft', 'PupilRight', 'FixationSeq', 'SaccadeSeq',
                      'Blink', 'GazeAOI', 'isMindWandered', 'batchNo']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for student in students:
            query = db.query(GazeInfo).order_by(GazeInfo.Timestamp).filter(
                GazeInfo.student_id == student.id).execution_options(stream_results=True)

            for batch in _batch_iter(2000, query):
                for entry in batch:

                    csv_writer.writerow({
                        'id': entry.id,
                        'student_id': entry.student_id,
                        'Timestamp': entry.Timestamp,
                        'GazeX': entry.GazeX,
                        'GazeY': entry.GazeY,
                        'GazeLeftx': entry.GazeLeftx,
                        'GazeLefty': entry.GazeLefty,
                        'GazeRightx': entry.GazeRightx,
                        'GazeRighty': entry.GazeRighty,
                        'PupilLeft': entry.PupilLeft,
                        'PupilRight': entry.PupilRight,
                        'FixationSeq': entry.FixationSeq,
                        'SaccadeSeq': entry.SaccadeSeq,
                        'Blink': entry.Blink,
                        'GazeAOI': entry.GazeAOI,
                        'isMindWandered': entry.isMindWandered,
                        'batchNo': entry.batchNo
                    })
                print("Writing completed for a batch ... \n")
        print("Writing Finished ... \n")


if __name__ == "__main__":
    main()


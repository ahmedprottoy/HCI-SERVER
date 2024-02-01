from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Enum, Boolean, Float
from database import Base, db_engine
import enum
from sqlalchemy.dialects.mysql import dialect
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import relationship

class Gender(str, enum.Enum):
    male = "M"
    female = "F"
    other = "O"

class StudnetInfo(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50))
    gender = Column(Enum(Gender))
    useGlass = Column(Boolean)
    displayWidth = Column(Integer)
    displayHeight = Column(Integer)
    age = Column(Integer)
    education = Column(String(50))
    accuracy = Column(Float)

class GazeInfo(Base):
    __tablename__ = "gaze_info"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    Timestamp = Column(String(15))
    GazeX = Column(Float)
    GazeY = Column(Float)
    GazeLeftx = Column(Float)
    GazeLefty = Column(Float)
    GazeRightx = Column(Float)
    GazeRighty = Column(Float)
    PupilLeft = Column(Float)
    PupilRight = Column(Float)
    FixationSeq = Column(Float)
    SaccadeSeq = Column(Float)
    Blink = Column(Float)
    GazeAOI = Column(Float)
    isMindWandered = Column(Boolean)
    batchNo = Column(Integer)

class GazeInfoDerived(Base):
    __tablename__ = "gaze_info_derived"

    id = Column(Integer, primary_key=True, index=True)
    time_to_peak_pupil = Column(Integer)
    peak_pupil = Column(Float)
    pupil_mean = Column(Float)
    pupil_slope = Column(Float)
    pupil_area_curve = Column(Float)
    blink_rate = Column(Float)
    peak_blink_duration = Column(Integer)
    avg_blink_duration = Column(Integer)
    fixation_count = Column(Integer)
    max_fixation_duration = Column(Integer)
    avg_fixation_duration = Column(Float)
    sacc_count = Column(Integer)
    sacc_duration = Column(Integer)
    sacc_vel = Column(Float)
    sacc_amplitude = Column(Float)
    micro_sacc_count = Column(Integer)
    first_pass_duration = Column(Integer)
    second_pass_duration = Column(Integer)
    batchNo = Column(Integer)

class ClassTimestampRecord(Base):
    __tablename__ = "class_timestamp_record"

    id = Column(Integer, primary_key=True, index=True)
    Timestamp = Column(String(15))
    Text = Column(String(20))

Base.metadata.create_all(db_engine)
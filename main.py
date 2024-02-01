from fastapi import FastAPI
import student_apis, gaze_info_apis
from fastapi.middleware.cors import CORSMiddleware
# import sys, os
# print(str(sys.path[0]))
# sys.path.append(os.path.join(sys.path[0],'/config'))
from _config.celery_utils import create_celery

origins = ["*"]
app = FastAPI()
app.celery_app = create_celery()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(student_apis.router)
app.include_router(gaze_info_apis.router)

celery = app.celery_app
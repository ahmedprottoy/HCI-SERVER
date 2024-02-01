class InfoException(Exception):
    ...


class StudentInfoNotFoundError(InfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Student Info Not Found"


class StudentInfoInfoAlreadyExistError(InfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Student Info Already Exists"
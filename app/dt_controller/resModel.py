class BaseModel:
    def __init__(self, data):
        self.data = data

class SuccessModel(BaseModel):
    def __init__(self, data):
        super().__init__(data)
        self.errno = 0

class ErrorModel(BaseModel):
    def __init__(self, data):
        super().__init__(data)
        self.errno = -1
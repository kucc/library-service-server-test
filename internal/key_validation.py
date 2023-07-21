from fastapi import HTTPException

class ForeignKeyValidationError(HTTPException):
    def __init__(self, detail:tuple):
        super().__init__(status_code=400, detail=f"Invalid ForeignKey, The {detail[0]} {detail[-1]} does not exist.")

class ItemKeyValidationError(HTTPException):
    def __init__(self, detail:tuple):
        super().__init__(status_code=400, detail=f"Invalid ItemKey, The {detail[0]} {detail[-1]} does not exist.")
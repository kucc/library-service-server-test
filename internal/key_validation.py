from fastapi import HTTPException, status

class ForeignKeyValidationError(HTTPException):
    def __init__(self, detail:tuple):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ForeignKey, The {detail[0]} {detail[-1]} does not exist.")

class ItemKeyValidationError(HTTPException):
    def __init__(self, detail:tuple):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ItemKey, The {detail[0]} {detail[-1]} does not exist.")
from fastapi import APIRouter

# main.py 에 api 위에 데코레이터로 @app.post("/users/create") 라고 쓰던 것 중에
# 공통되어 묶을 부분 ("/users") 를 prefix 에 넣자.
# ("/users/") 라고 마지막에 슬레시 '/' 를 넣으면 안 된다. 마지막 슬레시는 빼주자.
router = APIRouter(
	prefix="/users",
    tags=["users"]
)

# app/routers/users.py

from app.user_controller import UserController
user_controller = UserController()



# 데코레이터에는 main.py 에서 prefix 에 떼어주고 난 다음 남은 부분. 을 넣어주자
@router.post("/delete")
async def delete_user(username:str = Form(), password:str = Form()):
	result = await user_controller.delete_user(username, password)
	return result
    

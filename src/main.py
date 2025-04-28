from fastapi import FastAPI,Body,HTTPException
from pydantic import BaseModel
app=FastAPI()

'''
서버가 살아 있는지 테스트
요청이 오면 key : ping, value : pong를 반환
'''
@app.get("/")
def halth_check_handler():
    return {"ping": "pong"}

todo_data={
    1:{
        "id":1,
        "contents":"실전! fastapi 색션 0 수강",
        "is_done": True,
    },
    2:{
        "id":2,
        "contents":"실전! fastapi 색션 1 수강",
        "is_done": False,
    },
    3:{
        "id":3,
        "contents":"실전! fastapi 색션 2 수강",
        "is_done": False,
    },
}

#전체 todo 리스트 가져오기
@app.get("/todos",status_code=200)
def get_todos_handler(order:str | None=None):#쿼리 파라미터가 필수는 아님!!,
    ret=list(todo_data.values())
    if order and order=="DESC":#order 가 있고 그 값이 DESC 라면
        return ret[::-1]
    return ret

#단일 조회 todo , 1 2 3 을 키값으로 해서
@app.get("/todos/{todo_id}",status_code=200)
def get_todo_handler(todo_id:int):
    todo=todo_data.get(todo_id)
    if todo:
        return todo
    # return todo_data.get(todo_id,{})#값이 없다면 {} 빈 리스트 반환
    raise HTTPException(status_code=404,detail="ToDo Not Found")

class CreateTodoRequest(BaseModel):
    id:int
    contents:str
    is_done:bool

#todo 생성
@app.post("/todos",status_code=201)
def create_todo_handler(request:CreateTodoRequest):
          todo_data[request.id] = request.dict()#request객체를 dictionary로 변환

'''     
        여기에서는 3개의 값을 받는게 아니라 is_done만 받을거다
        요청 body에서 is_done이라는 값을 꼭 받아야 합니다 (...은 필수 의미)
		embed=True라서 body 안에
        {
            "is_done": true
        }
        이렇게 감싸진 형태로 받아야 함
'''
#todo 내용 수정
@app.patch("/todos/{todo_id}",status_code=200)
def update_todo_handler(
        todo_id:int,
        is_done:bool=Body(...,embed=True),
):
    todo=todo_data.get(todo_id)
    if todo:#만약에 todo 가 있다면 새로운 값으로 업데이트
        todo["is_done"] = is_done
        return todo
    # return {}#새로운 todo 가 없다면 빈 리스트 반환
    raise HTTPException(status_code=404,detail="ToDo Not Found")
@app.delete("/todos/{todo_id}",status_code=204)
def delete_todo_handler(todo_id:int):
    todo=todo_data.pop(todo_id,None)#키값이 없는 경우에 대비해서 None을 추가
    # return todo_data#남은 데이터 반환
    #204코드는 return 안 해도 된다
    if todo:
        return
    raise HTTPException(status_code=404,detail="ToDo Not Found")
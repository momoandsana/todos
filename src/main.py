from typing import List

from fastapi import FastAPI,Body,HTTPException,Depends

from schema.request import CreateTodoRequest

'''
Body->http 요청의 본문(body)에서 값을 빼올 때 사용
HttpException->오류 상태를 응답할 때 사용
'''

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.response import ToDoSchema
from schema.response import ToDoListSchema

from sqlalchemy.orm import Session

'''
BaseModel을 상속해서 데이터 구조(모양)를 정의하면,
fastapi가 자동으로 검사와 변환 수행
'''
app=FastAPI()
#FastAPI()를 실행해서 app이라는 웹 서버 프로그램 인스턴스 생성

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
def get_todos_handler(
        order:str | None=None,
        session:Session=Depends(get_db)
)->ToDoListSchema:
    todos:List[ToDo]=get_todos(session=session)

    if order and order=="DESC":#order 가 존재하고 그 값이 DESC 라면
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )

    return ToDoListSchema(
        todos=[
            ToDoSchema.from_orm(todo)
            for todo in todos
        ]
    )

#단일 조회 todo , 1 2 3 을 키값으로 해서
@app.get("/todos/{todo_id}",status_code=200)
def get_todo_handler(
        todo_id:int,
        session:Session=Depends(get_db)
):
    todo:ToDo|None=get_todo_by_todo_id(session=session,todo_id=todo_id)

    if todo:
        return ToDoSchema.from_orm(todo)
    # return todo_data.get(todo_id,{})#값이 없다면 {} 빈 리스트 반환
    raise HTTPException(status_code=404,detail="ToDo Not Found")


#todo 생성
@app.post("/todos",status_code=201)
def create_todo_handler(
        request: CreateTodoRequest,
        session:Session=Depends(get_db)
)->ToDoSchema:
          todo:ToDo=ToDo.create(request=request) # 여기까지는 id=none
          todo:ToDo=create_todo(session=session,todo=todo) # 여기부터 아이디 부여

          return ToDoSchema.from_orm(todo)
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
        session:Session=Depends(get_db)
):
   todo:ToDo|None=get_todo_by_todo_id(session=session,todo_id=todo_id)
   if todo:
       todo.done() if is_done else todo.undone()
       #update, 삼항 연산자->아직 디비에는 저장x

       todo:ToDo=update_todo(session=session,todo=todo)

       return ToDoSchema.from_orm(todo)#update
   raise HTTPException(status_code=404,detail="ToDo Not Found")
@app.delete("/todos/{todo_id}",status_code=204)
def delete_todo_handler(
        todo_id:int,
        session:Session=Depends(get_db)
):
    todo:ToDo|None=get_todo_by_todo_id(session=session,todo_id=todo_id)
    if not todo:

        raise HTTPException(status_code=404, detail="ToDo Not Found")
    # delete
    delete_todo(session=session, todo_id=todo_id)

from typing import List

from sqlalchemy import select,delete
from sqlalchemy.orm import Session

from database.orm import ToDo

def get_todos(session:Session)->List[ToDo]:
    return list(session.scalars(select(ToDo)))

def get_todo_by_todo_id(session:Session,todo_id:int) -> ToDo|None:
    return session.scalar(select(ToDo).where(ToDo.id==todo_id))

def create_todo(session:Session,todo:ToDo)->ToDo:
    session.add(instance=todo)
    session.commit() # todo의 아이디를 할당
    session.refresh(instance=todo)# 메모리는 id를 모르므로 refresh를 통해 디비에서 할당한 아이디를 메모리에도 저장하여 보여주게 된다
    return todo

def update_todo(session:Session,todo:ToDo)->ToDo:
    session.add(instance=todo)
    session.commit()
    session.refresh(instance=todo)
    return todo

def delete_todo(session:Session,todo_id:int)->None:
    session.execute(delete(ToDo).where(ToDo.id==todo_id))
    session.commit()
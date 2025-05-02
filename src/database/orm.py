from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean,Column,Integer,String

from schema.request import CreateTodoRequest

Base = declarative_base()

class ToDo(Base):
    __tablename__="todo"

    id=Column(Integer,primary_key=True,index=True)
    contents=Column(String(256),nullable=False)
    is_done=Column(Boolean,nullable=False)

    def __repr__(self):
        return f"ToDo(id={self.id}, contents='{self.contents}', is_done={self.is_done})"

    @classmethod
    def create(cls,request:CreateTodoRequest)->"ToDo":
        return cls(
            contents=request.contents,
            is_done=request.is_done,
        )

    def done(self)->"ToDo":
        self.is_done=True
        #send email, 유지보수가 쉬워짐, 새로운 기능 추가하기 좋아
        return self

    def undone(self)->"ToDo":
        self.is_done=False
        return self
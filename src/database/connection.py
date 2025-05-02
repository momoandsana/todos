from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL="mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine=create_engine(DATABASE_URL,echo=True)
#디버깅 환경에서는 echo=True, 어떤 쿼리가 나가고 있는지 확인하기 위해

SessionFactory=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    session=SessionFactory()
    try:
        yield session
    finally:
        session.close()

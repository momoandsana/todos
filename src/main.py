from fastapi import FastAPI

app=FastAPI()

'''
서버가 살아 있는지 테스트
요청이 오면 key : ping, value : pong를 반환
'''
@app.get("/")
def halth_check_handler():
    return {"ping": "pong"}
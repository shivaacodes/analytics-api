from fastapi import FastAPI

app=FastAPI()

@app.get("/test")
def first_api():
    return {"Hello":"world"}
from fastapi import FastAPI

app = FastAPI(title="Phase-2 Todo Backend")

@app.get("/")
def root():
    return {"message": "Backend running"}


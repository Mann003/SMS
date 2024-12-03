from fastapi import FastAPI

from router.route import studentRouter

app = FastAPI()

app.include_router(studentRouter)


@app.get("/")
async def root():
    return {"message": "Welcome to Student Management System"}

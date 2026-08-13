from fastapi import FastAPI, status
from fastapi.responses import JSONResponse


app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "Watch this week's lecture",
        "done": True
    },
    {
        "id": 2,
        "title": "Go to the gym",
        "done": False
    },
    {
        "id": 3,
        "title": "Finish the assignment",
        "done": False
    }
]

@app.get("/")
async def root():
    return {"name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def return_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {"error": f"Task {id} was not found"}
    )

@app.post("/tasks")
async def new_task(task: dict):
    task["title"] = task.get("title", "")
    if not task["title"] or not task["title"].strip():
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"error": "Task title cannot be empty"}
        )
    task["id"] = len(tasks) + 1
    task["done"] = False
    tasks.append(task)
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = task
    )
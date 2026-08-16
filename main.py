from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, Response


app = FastAPI()

# Create list of initial tasks
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

# API description
@app.get("/")
async def root():
    return {"name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] }

# Check server status
@app.get("/health")
async def health():
    return {"status": "ok"}

# Return the entire list of tasks
@app.get("/tasks")
async def get_tasks():
    return tasks

# Return a task with a specific ID
@app.get("/tasks/{id}")
async def return_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    # If a task with the provided ID doesn't exist, return status 404
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {"error": f"Task {id} was not found"}
    )

# Create a new task
@app.post("/tasks")
async def new_task(task: dict):
    title = task.get("title", "")
    if not title or not title.strip():
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"error": "Task title cannot be empty"}
        )

    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "title" : title,
        "id" : new_id,
        "done" : False
    }
    tasks.append(new_task)

    # Return status 201, indicating successful creation of the task
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = new_task
    )

# Update an existing task
@app.put("/tasks/{id}")
async def update_task(id: int, updates: dict):
    # Make sure that there are updates to be done
    if not updates:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"error": "Empty/invalid body"}
        )
    # Make sure that updates contain at least one of the required fields
    if "title" not in updates and "done" not in updates:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"error": "Empty/invalid body: updates must have at least one of the following: title or done"}
        )
    # Make sure that updates do not contain any undesired keys
    allowed_keys = {"title", "done"}
    extra_keys = set(updates.keys()) - allowed_keys
    if extra_keys:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {"error": "Empty/invalid body: updates contain invalid keys"}
        )
    # If we want to update "title", it cannot be an empty string
    if "title" in updates:
        if not isinstance(updates["title"], str) or not updates["title"].strip():
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {"error": "Empty/invalid body: 'title' cannot be empty"}
            )
    # Make sure that "done" is a boolean value
    if "done" in updates:
        if not isinstance(updates["done"], bool):
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {"error": "Empty/invalid body: 'done' must be a boolean value (True/False)"}
            )
    # Get ID of the task we want to update and update it
    for task in tasks:
        if task["id"] == id:
            if "title" in updates:
                task["title"] = updates["title"]
            if "done" in updates:
                task["done"] = updates["done"]
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = task
            )
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {"error": "Unknown id"}
    )

# Delete an existing task
@app.delete("/tasks/{id}")
async def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return Response(
                status_code = status.HTTP_204_NO_CONTENT
            )
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {"error": "Unknown id"}
    )
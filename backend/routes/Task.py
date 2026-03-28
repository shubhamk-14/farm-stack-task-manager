from fastapi import APIRouter,HTTPException
from models.Task import Task as TaskModel,tranformTask
from config.db import db as Mongo_db
import bson

route = APIRouter(prefix="/api/v1", tags=["Task"])

taskCollection = Mongo_db["task"]

@route.post("/create",tags=["Task"])
async def addTask(data: TaskModel):
   doc= await taskCollection.insert_one(data.dict())

   await taskCollection.find_one({"_id":doc.inserted_id})
#    task['_id'] = str(task['_id'])

   return {
       "msg":"Task Created !"
   }



@route.get("/get",tags=["Task"])
async def getAllTask():
    docs = taskCollection.find({})
    tasks = []

    async for task in docs:
        tasks.append(tranformTask(task))

    return tasks



@route.patch("/update/{id}",tags=["Task"])
async def updateTask(id:str):
    if(not bson.ObjectId.is_valid(id)):
        raise HTTPException(400,"Id is not valid")
    await taskCollection.update_one({"_id":bson.ObjectId(id)},{
        "$set":{
            "is_complete":True
        }
    })
    return {
        "msg":"Task Updated"
    }

@route.delete("/delete/{id}", tags=["Task"])
async def deleteTask(id: str):
    if not bson.ObjectId.is_valid(id):
        raise HTTPException(400, "Id is not valid")
    result = await taskCollection.delete_one({"_id": bson.ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Task not found")
    return {
        "msg": "Task Deleted"
    }


@route.get("/get/{id}",tags=['Todo'])
async def getTask(id:str):
    pass



@route.put("/update/{id}",tags=['Todo'])
async def updateTaskById(id:str):
   pass

    

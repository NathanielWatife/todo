from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create a todo 
@app.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(request:schemas.Todo, db: Session=Depends(get_db)):
    new_todo = models.TodoModel(task=request.task)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# get all the todo list from the database
@app.get('/todo', status_code=status.HTTP_200_OK)
def show_all_todo(db: Session=Depends(get_db)):
    todo = db.query(models.TodoModel).all()
    return todo 



# get only the one todo by id
@app.get('/todo/{id}', status_code=status.HTTP_200_OK)
def show_single_todo(id, response:Response, db: Session=Depends(get_db)):
    list = db.query(models.TodoModel).filter(models.TodoModel.id== id).first()
    if not list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Id {id} is not found on our server. Please the correct ID to get you the output"
        )
    return list

@app.delete('/todo/{id}', status_code=status.HTTP_410_GONE)
def erase_list(id, response:Response, db: Session = Depends(get_db)):
    list = db.query(models.TodoModel).filter(models.TodoModel.id == id).first()
    if list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {id} is not found"
        )
    db.delete(list)
    db.commit()
    return {"message": f"Todo list with ID {id} has been deleted successfully"}

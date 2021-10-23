from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users", response_model=List[schemas.User])
def read_users(workspace_id: int, db: Session = Depends(get_db)):
    users = crud.get_users_by_workspace(db=db, workspace_id=workspace_id)
    return users

@app.post("/users", response_model=schemas.User)
def create_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user_create=user_create)

@app.get("/workspaces", response_model=schemas.Workspace)
def read_workspace(workspace_id: int, db: Session = Depends(get_db)):
    db_workspace = crud.get_workspace(db=db, workspace_id=workspace_id)
    if db_workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return db_workspace

@app.post("/workspaces", response_model=schemas.Workspace)
def create_workspace(workspace_create: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    db_workspace = crud.get_workspace_by_name(db=db, workspace_name=workspace_create.name)
    if db_workspace:
        raise HTTPException(status_code=400, detail="Workspace already registered")
    return crud.create_workspace(db=db, workspace_create=workspace_create)

def get_workspace_edit(db: Session, workspace_update: schemas.WorkspaceEdit):
    db_user = crud.get_user(db=db, user_id=workspace_update.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_workspace = crud.get_workspace(db=db, workspace_id=workspace_update.id)
    if db_workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    return [ db_user, db_workspace ]

@app.put("/workspaces/user", response_model=schemas.Workspace)
def add_user_to_workspace(workspace_update: schemas.WorkspaceEdit, db: Session = Depends(get_db)):
    db_user, db_workspace = get_workspace_edit(db=db, workspace_update=workspace_update)
    for user in db_workspace.users:
        if user.id == workspace_update.user_id:
            raise HTTPException(status_code=400, detail="User already registered to workspace")
    return crud.add_user_to_workspace(db=db, db_user=db_user, db_workspace=db_workspace)

@app.delete("/workspaces/user", response_model=schemas.Workspace)
def delete_user_from_workspace(workspace_update: schemas.WorkspaceEdit, db: Session = Depends(get_db)):
    db_user, db_workspace = get_workspace_edit(db=db, workspace_update=workspace_update)
    for user in db_workspace.users:
        if user.id == workspace_update.user_id:
            return crud.remove_user_to_workspace(db=db, db_user=db_user, db_workspace=db_workspace)
    raise HTTPException(status_code=404, detail="User not found")
from typing import List
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas
from .crud import crud_user, crud_workspace
from .database import SessionLocal, engine
from .core import security

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/user/{user_id}", response_model=schemas.User, dependencies=[Depends(oauth2_scheme)])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users", response_model=List[schemas.User], dependencies=[Depends(oauth2_scheme)])
def read_users(workspace_id: int, db: Session = Depends(get_db)):
    users = crud_user.get_users_by_workspace(db=db, workspace_id=workspace_id)
    return users

@app.post("/user", response_model=schemas.User)
def create_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db=db, email=user_create.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user_create=user_create)

@app.get("/workspace/{workspace_id}", response_model=schemas.Workspace, dependencies=[Depends(oauth2_scheme)])
def read_workspace(workspace_id: int, db: Session = Depends(get_db)):
    db_workspace = crud_workspace.get_workspace(db=db, workspace_id=workspace_id)
    if db_workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return db_workspace

@app.post("/workspace", response_model=schemas.Workspace, dependencies=[Depends(oauth2_scheme)])
def create_workspace(workspace_create: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    db_workspace = crud_workspace.get_workspace_by_name(db=db, workspace_name=workspace_create.name)
    if db_workspace:
        raise HTTPException(status_code=400, detail="Workspace already registered")
    return crud_workspace.create_workspace(db=db, workspace_create=workspace_create)

def get_workspace_edit(db: Session, workspace_update: schemas.WorkspaceEdit):
    db_user = crud_user.get_user(db=db, user_id=workspace_update.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_workspace = crud_workspace.get_workspace(db=db, workspace_id=workspace_update.id)
    if db_workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    return [ db_user, db_workspace ]

@app.put("/workspace/user", response_model=schemas.Workspace, dependencies=[Depends(oauth2_scheme)])
def add_user_to_workspace(workspace_update: schemas.WorkspaceEdit, db: Session = Depends(get_db)):
    db_user, db_workspace = get_workspace_edit(db=db, workspace_update=workspace_update)
    for user in db_workspace.users:
        if user.id == workspace_update.user_id:
            raise HTTPException(status_code=400, detail="User already registered to workspace")
    return crud_workspace.add_user_to_workspace(db=db, db_user=db_user, db_workspace=db_workspace)

@app.delete("/workspace/user", response_model=schemas.Workspace, dependencies=[Depends(oauth2_scheme)])
def delete_user_from_workspace(workspace_update: schemas.WorkspaceEdit, db: Session = Depends(get_db)):
    db_user, db_workspace = get_workspace_edit(db=db, workspace_update=workspace_update)
    for user in db_workspace.users:
        if user.id == workspace_update.user_id:
            return crud_workspace.remove_user_to_workspace(db=db, db_user=db_user, db_workspace=db_workspace)
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    email = form_data.username
    user = crud_user.authenticate(
        db, email, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": security.create_access_token(
            user.id
        ),
        "token_type": "bearer",
    }

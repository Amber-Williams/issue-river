from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import crud_user

def get_workspace(db: Session, workspace_id: int):
    return db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()

def get_workspace_by_name(db: Session, workspace_name: str):
    return db.query(models.Workspace).filter(models.Workspace.name == workspace_name).first()

def create_workspace(db: Session, workspace_create: schemas.WorkspaceCreate):
    db_user = crud_user.get_user(db, workspace_create.user_id)
    db_workspace = models.Workspace(name=workspace_create.name)
    db_workspace.users.append(db_user)
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    db.refresh(db_user)
    return db_workspace

def add_user_to_workspace(db: Session, db_user: models.User, db_workspace: models.Workspace):
    db_workspace.users.append(db_user)
    db.commit()
    db.refresh(db_workspace)
    db.refresh(db_user)
    return db_workspace

def remove_user_to_workspace(db: Session, db_user: models.User, db_workspace: models.Workspace):
    db_workspace.users.remove(db_user)
    db.commit()
    db.refresh(db_workspace)
    db.refresh(db_user)
    return db_workspace

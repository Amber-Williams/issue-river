from sqlalchemy.orm import Session

from . import models, schemas

def get_users_by_workspace(db: Session, workspace_id: int):
    return db.query(models.User).filter(models.User.workspace == workspace_id).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_create: schemas.UserCreate):
    fake_hashed_password = user_create.password + "notactuallyhashedyet"
    db_user = models.User(
        email=user_create.email, 
        first_name=user_create.first_name, 
        last_name=user_create.last_name, 
        hashed_password=fake_hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_workspace(db: Session, workspace_id: int):
    return db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()

def get_workspace_by_name(db: Session, workspace_name: str):
    return db.query(models.Workspace).filter(models.Workspace.name == workspace_name).first()

def create_workspace(db: Session, workspace_create: schemas.WorkspaceCreate):
    db_user = get_user(db, workspace_create.user_id)
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

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, workspace={self.workspace}) role={self.role}>"

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    workspace = Column(Integer, ForeignKey('workspace.id'), nullable=True)

class Workspace(Base):
    def __repr__(self):
        return f"<Workspace(id={self.id}, name={self.name}, users={self.users})>"

    __tablename__ = "workspace"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User")



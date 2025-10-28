from fastapi import FastAPI, Depends, Path, HTTPException
from models import PIM, Base
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class ProjectRequest(BaseModel):
    project_number: str = Field(min_length=14, max_length=17)
    team: str = Field(min_length=2, max_length=3)
    engineer: str = Field(min_length=3, max_length=50)
    customer: str = Field(min_length=3, max_length=50)
    project_name: str = Field(min_length=1, max_length=100)
    progress: int = Field(ge=0, le=100)


class ProjectUpdate(BaseModel):
    project_number: str = Field(min_length=14, max_length=17)
    progress: int = Field(ge=0, le=100)


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(PIM).all()


@app.get("/project/{project_id}", status_code=status.HTTP_200_OK)
async def read_project_by_id(db: db_dependency, project_id: int = Path(gt=0)):
    project_model = db.query(PIM).filter(PIM.id == project_id).first()
    if project_model is not None:
        return project_model
    raise HTTPException(status_code=404, detail='Project not found.')


@app.get("/project/number/{project_number}", status_code=status.HTTP_200_OK)
async def read_project_by_number(db: db_dependency, project_number: str = Path(min_length=14, max_length=17)):
    project_model = db.query(PIM).filter(
        PIM.project_number == project_number).first()
    if project_model is not None:
        return project_model
    raise HTTPException(status_code=404, detail='Project not found.')


@app.post("/create-project", status_code=status.HTTP_201_CREATED)
async def create_project(db: db_dependency, project_request: ProjectRequest):
    project_model = PIM(**project_request.model_dump())

    db.add(project_model)
    db.commit()


@app.put("/project/{project_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_progress(db: db_dependency, project_update: ProjectUpdate, project_number: str = Path(min_length=14, max_length=17)):
    project_model = db.query(PIM).filter(
        PIM.project_number == project_number).first()

    if project_model is None:
        raise HTTPException(status_code=404, detail='Project not found.')

    project_model.progress = project_update.progress

    db.add(project_model)
    db.commit()


@app.delete("/project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(db: db_dependency, project_id: int = Path(gt=0)):
    project_model = db.query(PIM).filter(PIM.id == project_id).first()

    if project_model is None:
        raise HTTPException(status_code=404, detail='Project not found.')

    db.delete(project_model)
    db.commit()

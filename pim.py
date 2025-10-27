from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette import status

app = FastAPI()


class Project:
    id: int
    project_number: str
    team: str
    engineer: str
    customer: str
    project_name: str
    progress: int

    def __init__(self, id, project_number, team, engineer, customer, project_name, progress):
        self.id = id
        self.project_number = project_number
        self.team = team
        self.engineer = engineer
        self.customer = customer
        self.project_name = project_name
        self.progress = progress


class ProjectRequest(BaseModel):
    id: Optional[int] = Field(
        description='ID is not needed on create.', default=None)
    project_number: str = Field(min_length=14, max_length=17)
    team: str = Field(min_length=2)
    engineer: str = Field(min_length=1)
    customer: str = Field(min_length=1)
    project_name: str = Field(min_length=1, max_length=100)
    progress: int = Field(ge=0, le=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "project_number": "QKPH-1234-5678",
                "team": "IOT",
                "engineer": "Louie Cleofas",
                "customer": "Customer Name",
                "project_name": "Project Name",
                "progress": 70
            }
        }
    }


PROJECTS: List[Project] = [
    Project(1, "QKPH-TEST-0001", "IOT", "Louie", "DNPH", "Traceability", 50),
    Project(2, "QKPH-TEST-0002", "INF", "Francis",
            "KDDI", "Test Project 1", 60),
    Project(3, "QKPH-TEST-0003", "SEP", "Arjay",
            "Daiho", "Test Project 2", 40),
    Project(4, "QKPH-TEST-0004", "NET", "Francis",
            "DNPH", "Test Project 3", 70),
    Project(5, "QKPH-TEST-0005", "IOT", "Louie", "PMM", "Test Project 4", 90),
]


@app.get('/', status_code=status.HTTP_200_OK)
async def list_projects():
    return PROJECTS


@app.get('/team/{team}', status_code=status.HTTP_200_OK)
async def read_projects_by_team(team: str = Path(min_length=1)):
    return [project for project in PROJECTS if project.get('team').casefold() == team.casefold()]


@app.get('/team/{team}/', status_code=status.HTTP_200_OK)
async def read_team_engineer_query(team: str = Path(min_length=1), engineer: str = Query(min_length=1)):
    return [project for project in PROJECTS if project.get('team').casefold() == team.casefold() and
            project.get('infra engineer').casefold() == engineer.casefold()]


@app.get("/id/{project_id}", status_code=status.HTTP_200_OK)
async def read_project_by_id(project_id: int = Path(gt=0)):
    for project in PROJECTS:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=404, detail='Item not found.')


@app.get("/number/{project_number}", status_code=status.HTTP_200_OK)
async def read_project_by_project_number(project_number: str = Path(min_length=14, max_length=17)):
    for project in PROJECTS:
        if project.project_number == project_number:
            return project
    raise HTTPException(status_code=404, detail='Item not found.')


@app.post('/create-project', status_code=status.HTTP_201_CREATED)
async def create_project(project_request: ProjectRequest):
    new_project = Project(**project_request.model_dump())
    PROJECTS.append(auto_project_id(new_project))
    return new_project


def auto_project_id(project: Project):
    project.id = 1 if len(PROJECTS) == 0 else PROJECTS[-1].id + 1

    return project


@app.put("/update-progress", status_code=status.HTTP_204_NO_CONTENT)
async def update_progress(updated_progress: ProjectRequest):
    progress_updated = False
    for i in range(len(PROJECTS)):
        if PROJECTS[i].get('project_number').casefold() == updated_progress.get('project_number').casefold():
            PROJECTS[i]['latest overall progress'] = updated_progress['latest overall progress']
            progress_updated = True
    if not progress_updated:
        raise HTTPException(status_code=404, detail='Item not found.')


@app.delete('/delete-project/{project_number}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_number: str = Path(min_length=14, max_length=17)):
    project_deleted = False
    for i in range(len(PROJECTS)):
        if PROJECTS[i].get('project_number').casefold() == project_number.casefold():
            PROJECTS.pop(i)
            project_deleted = True
            break
    if not project_deleted:
        raise HTTPException(status_code=404, detail='Item not found.')

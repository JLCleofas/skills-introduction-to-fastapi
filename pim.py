from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List

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
    id: Optional[int] = None
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


@app.get('/')
async def get_all_projects():
    return PROJECTS


@app.get('/team/{team}')
async def read_team_engineer_query(team: str):
    return [project for project in PROJECTS if project.get('team').casefold() == team.casefold()]


@app.get('/team/{team}/')
async def read_team_engineer_query(team: str, engineer: str):
    return [project for project in PROJECTS if project.get('team').casefold() == team.casefold() and
            project.get('infra engineer').casefold() == engineer.casefold()]


@app.post('/create_project')
async def create_project(project_request: ProjectRequest):
    new_project = Project(**project_request.model_dump())
    PROJECTS.append(auto_project_id(new_project))
    return new_project


@app.put("/update_progress")
async def update_progress(updated_progress=Body()):
    for i in range(len(PROJECTS)):
        if PROJECTS[i].get('project number').casefold() == updated_progress.get('project number').casefold():
            PROJECTS[i]['latest overall progress'] = updated_progress['latest overall progress']


@app.delete('/delete_project/{project_number}')
async def delete_project(project_number: str):
    for i in range(len(PROJECTS)):
        if PROJECTS[i].get('project number').casefold() == project_number.casefold():
            PROJECTS .pop(i)


def auto_project_id(project: Project):
    project.id = 1 if len(PROJECTS) == 0 else PROJECTS[-1].id + 1

    return project

from fastapi import Body, FastAPI

app = FastAPI()

projects = [
    {"project number": "QKPH-TEST-0001", "team": "IOT", "infra engineer": "Louie",
        "customer": "DNPH", "project name": "Traceability", "latest overall progress": "50"},
    {"project number": "QKPH-TEST-0002", "team": "INF", "infra engineer": "Francis",
        "customer": "KDDI", "project name": "Test Project 1", "latest overall progress": "60"},
    {"project number": "QKPH-TEST-0003", "team": "SEP", "infra engineer": "Arjay",
        "customer": "Daiho", "project name": "Test Project 2", "latest overall progress": "40"},
    {"project number": "QKPH-TEST-0004", "team": "NET", "infra engineer": "Francis",
        "customer": "DNPH", "project name": "Test Project 3", "latest overall progress": "70"},
    {"project number": "QKPH-TEST-0005", "team": "IOT", "infra engineer": "Louie",
        "customer": "PMM", "project name": "Test Project 4", "latest overall progress": "90"},
]


@app.get('/')
async def get_all_projects():
    return projects


@app.get('/team/{team}')
async def read_team_engineer_query(team: str):
    return [project for project in projects if project.get('team').casefold() == team.casefold()]


@app.get('/team/{team}/')
async def read_team_engineer_query(team: str, engineer: str):
    return [project for project in projects if project.get('team').casefold() == team.casefold() and
            project.get('infra engineer').casefold() == engineer.casefold()]


@app.post('/create_project')
async def create_project(new_project=Body()):
    projects.append(new_project)


@app.put("/update_progress")
async def update_progress(updated_progress=Body()):
    for i in range(len(projects)):
        if projects[i].get('project number').casefold() == updated_progress.get('project number').casefold():
            projects[i]['latest overall progress'] = updated_progress['latest overall progress']


@app.delete('/delete_project/{project_number}')
async def delete_project(project_number: str):
    for i in range(len(projects)):
        if projects[i].get('project number').casefold() == project_number.casefold():
            projects.pop(i)

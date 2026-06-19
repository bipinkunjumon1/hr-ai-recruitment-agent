from fastapi import FastAPI

from routers.jd_routes import router as jd_router

from routers.resume_routes import router as resume_router

from routers.workflow_routes import (
    router as workflow_router
)
from routers.ats_routes import (
    router as ats_router
)


from routers.interview_routes import (
    router as interview_router
)

from routers.auth_routes import (
    router as auth_router
)
from phase2.routers.reschedule_routes import router as reschedule_router


app = FastAPI(
    title="HR AI Recruitment Agent",
    version="1.0.0"
)

app.include_router(

    auth_router,

    prefix="/api/auth",

    tags=["Authentication"]
)

app.include_router(
    jd_router,
    prefix="/api/jd",
    tags=["Job Description"]
)

app.include_router(
    resume_router,
    prefix="/api/resume",
    tags=["Resume"]
)

app.include_router(
    workflow_router,
    prefix="/api/workflow",
    tags=["Recruitment Workflow"]
)
app.include_router(
    ats_router,
    prefix="/api/ats",
    tags=["ATS"]
)


app.include_router(reschedule_router, prefix="/api/reschedule",
                   tags=["Reschedule"])



@app.get("/")
def home():

    return {
        "message": "HR AI Recruitment Agent"
    }


app.include_router(

    interview_router,

    prefix="/api/interview",

    tags=["Interview"]
)
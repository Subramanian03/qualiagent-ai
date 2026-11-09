from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI

from backend.routers.ai import router as ai_router
from backend.routers.requirements import router as requirements_router
from backend.routers.test_cases import router as test_cases_router

from backend.db.database import Base
from backend.db.database import engine
from backend.db.project_model import ProjectDB
from backend.db.requirement_model import RequirementDB
from backend.db.test_case_model import TestCaseDB
from backend.routers.projects import router as projects_router


from fastapi.middleware.cors import CORSMiddleware
from backend.db.automation_model import AutomationScriptDB
from backend.routers.automation import router as automation_router
from backend.db.execution_model import ExecutionDB
from backend.db.test_cycle_model import (
    TestCycleDB,
)
from backend.db.cycle_test_item_model import (
    CycleTestItemDB,
)
from backend.routers.executions import (
    router as executions_router,
)
from backend.db.test_scenario_model import (
    TestScenarioDB,
)
from backend.db.execution_config_model import (
    ExecutionConfigDB,
)
from backend.routers.execution_config import (
    router as execution_config_router,
)
from backend.routers.reports import (
    router as reports_router,
)
from backend.routers.test_scenarios import (
    router as test_scenarios_router,
)
from backend.routers.ai_status import (
    router as ai_status_router,
)
from backend.routers import test_cycles

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="QualiAgent AI",
    description="AI-powered QA testing platform",
    version="0.12.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(requirements_router)
app.include_router(ai_router)
app.include_router(test_cases_router)
app.include_router(projects_router)
app.include_router(automation_router)
app.include_router(executions_router)
app.include_router(execution_config_router)
app.include_router(reports_router)
app.include_router(test_scenarios_router)
app.include_router(ai_status_router)
app.include_router(test_cycles.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to QualiAgent AI",
        "status": "running",
        "version": "0.12.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "QualiAgent AI Backend",
    }
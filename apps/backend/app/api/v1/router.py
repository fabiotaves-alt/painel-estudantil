from fastapi import APIRouter

from app.api.v1 import health

api_router = APIRouter()

# Incluir routers por domínio
api_router.include_router(health.router, tags=["Health"])

# TODO: Adicionar routers nas próximas fases
# api_router.include_router(semesters.router, prefix="/semesters", tags=["Semesters"])
# api_router.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
# api_router.include_router(class_meetings.router, prefix="/class-meetings", tags=["Class Meetings"])
# api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
# api_router.include_router(grades.router, prefix="/grades", tags=["Grades"])
# api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
# api_router.include_router(settings_router.router, prefix="/settings", tags=["Settings"])
# api_router.include_router(backups.router, prefix="/backups", tags=["Backups"])

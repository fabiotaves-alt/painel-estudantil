from datetime import UTC, datetime
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar("DataT")


class MetaInfo(BaseModel):
    """Metadados de resposta da API."""

    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class APIResponse[T](BaseModel):
    """Resposta padrão de sucesso da API."""

    data: T
    meta: MetaInfo

    model_config = ConfigDict(from_attributes=True)


class APIError(BaseModel):
    """Erro padrão da API."""

    code: str
    message: str
    details: dict | None = None


class APIErrorResponse(BaseModel):
    """Resposta de erro da API."""

    error: APIError
    meta: MetaInfo


# Health check
class HealthResponse(BaseModel):
    """Resposta do endpoint de health."""

    status: str = "ok"
    version: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


# Semester
class SemesterCreate(BaseModel):
    """Schema para criar semestre."""

    name: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=2000, le=2100)
    start_date: datetime
    end_date: datetime
    is_current: bool = False


class SemesterUpdate(BaseModel):
    """Schema para atualizar semestre."""

    name: str | None = Field(None, min_length=1, max_length=100)
    year: int | None = Field(None, ge=2000, le=2100)
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_current: bool | None = None


class SemesterRead(BaseModel):
    """Schema de leitura de semestre."""

    id: int
    name: str
    year: int
    start_date: datetime
    end_date: datetime
    is_current: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Subject
class SubjectCreate(BaseModel):
    """Schema para criar disciplina."""

    code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=200)
    professor: str | None = Field(None, max_length=200)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    workload_hours: int = Field(..., ge=1, le=1000)
    semester_id: int


class SubjectUpdate(BaseModel):
    """Schema para atualizar disciplina."""

    code: str | None = Field(None, min_length=1, max_length=20)
    name: str | None = Field(None, min_length=1, max_length=200)
    professor: str | None = Field(None, max_length=200)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    workload_hours: int | None = Field(None, ge=1, le=1000)
    semester_id: int | None = None


class SubjectRead(BaseModel):
    """Schema de leitura de disciplina."""

    id: int
    code: str
    name: str
    professor: str | None
    color: str | None
    workload_hours: int
    semester_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ClassMeeting
class ClassMeetingCreate(BaseModel):
    """Schema para criar aula."""

    subject_id: int
    weekday: int = Field(..., ge=0, le=6)
    start_time: datetime
    end_time: datetime
    location: str | None = Field(None, max_length=200)
    notes: str | None = None


class ClassMeetingUpdate(BaseModel):
    """Schema para atualizar aula."""

    weekday: int | None = Field(None, ge=0, le=6)
    start_time: datetime | None = None
    end_time: datetime | None = None
    location: str | None = Field(None, max_length=200)
    notes: str | None = None


class ClassMeetingRead(BaseModel):
    """Schema de leitura de aula."""

    id: int
    subject_id: int
    weekday: int
    start_time: datetime
    end_time: datetime
    location: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ImportJob
class ImportJobCreate(BaseModel):
    """Schema para criar job de importação."""

    filename: str
    file_hash: str


class ImportJobRead(BaseModel):
    """Schema de leitura de job de importação."""

    id: int
    filename: str
    file_hash: str
    status: str
    extracted_at: datetime | None
    error: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

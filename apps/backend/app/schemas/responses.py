from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

DataT = TypeVar("DataT")


class MetaInfo(BaseModel):
    """Metadados de resposta da API."""

    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class APIResponse(BaseModel, Generic[DataT]):
    """Resposta padrão de sucesso da API."""

    data: DataT
    meta: MetaInfo

    model_config = ConfigDict(from_attributes=True)


class APIError(BaseModel):
    """Erro padrão da API."""

    code: str
    message: str
    details: Optional[dict] = None


class APIErrorResponse(BaseModel):
    """Resposta de erro da API."""

    error: APIError
    meta: MetaInfo


# Health check
class HealthResponse(BaseModel):
    """Resposta do endpoint de health."""

    status: str = "ok"
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


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

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=2000, le=2100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None


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
    professor: Optional[str] = Field(None, max_length=200)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    workload_hours: int = Field(..., ge=1, le=1000)
    semester_id: int


class SubjectUpdate(BaseModel):
    """Schema para atualizar disciplina."""

    code: Optional[str] = Field(None, min_length=1, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    professor: Optional[str] = Field(None, max_length=200)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    workload_hours: Optional[int] = Field(None, ge=1, le=1000)
    semester_id: Optional[int] = None


class SubjectRead(BaseModel):
    """Schema de leitura de disciplina."""

    id: int
    code: str
    name: str
    professor: Optional[str]
    color: Optional[str]
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
    location: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None


class ClassMeetingUpdate(BaseModel):
    """Schema para atualizar aula."""

    weekday: Optional[int] = Field(None, ge=0, le=6)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None


class ClassMeetingRead(BaseModel):
    """Schema de leitura de aula."""

    id: int
    subject_id: int
    weekday: int
    start_time: datetime
    end_time: datetime
    location: Optional[str]
    notes: Optional[str]
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
    extracted_at: Optional[datetime]
    error: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """Mixin para campos de timestamp."""

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class SemesterBase(SQLModel):
    """Base para Semester."""

    name: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=2000, le=2100)
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    is_current: bool = Field(default=False)


class Semester(SemesterBase, TimestampMixin, table=True):
    """Modelo de semestre acadêmico."""

    __tablename__ = "semesters"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relacionamentos serão definidos após criar todos os modelos


class SubjectBase(SQLModel):
    """Base para Subject."""

    code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=200)
    professor: Optional[str] = Field(default=None, max_length=200)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color
    workload_hours: int = Field(..., ge=1, le=1000)


class Subject(SubjectBase, TimestampMixin, table=True):
    """Modelo de disciplina."""

    __tablename__ = "subjects"

    id: Optional[int] = Field(default=None, primary_key=True)
    semester_id: Optional[int] = Field(default=None, foreign_key="semesters.id", nullable=False)


class ClassMeetingBase(SQLModel):
    """Base para ClassMeeting."""

    weekday: int = Field(..., ge=0, le=6)  # 0=segunda, 6=domingo
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)
    location: Optional[str] = Field(default=None, max_length=200)
    notes: Optional[str] = Field(default=None)


class ClassMeeting(ClassMeetingBase, TimestampMixin, table=True):
    """Modelo de aula/encontro."""

    __tablename__ = "class_meetings"

    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: Optional[int] = Field(default=None, foreign_key="subjects.id", nullable=False)


class ImportJobBase(SQLModel):
    """Base para ImportJob."""

    filename: str = Field(..., min_length=1)
    file_hash: str = Field(..., min_length=64, max_length=64)  # SHA-256
    status: str = Field(default="pending")  # pending, processing, completed, failed
    extracted_at: Optional[datetime] = Field(default=None)
    error: Optional[str] = Field(default=None)


class ImportJob(ImportJobBase, TimestampMixin, table=True):
    """Modelo de job de importação."""

    __tablename__ = "import_jobs"

    id: Optional[int] = Field(default=None, primary_key=True)


# Modelos adicionais (fora do MVP inicial, mas definidos para contrato)
class StudentProfileBase(SQLModel):
    """Base para perfil do estudante."""

    name: str = Field(..., min_length=1, max_length=200)
    student_id: Optional[str] = Field(default=None, max_length=50)
    course: Optional[str] = Field(default=None, max_length=200)


class StudentProfile(StudentProfileBase, TimestampMixin, table=True):
    """Perfil do estudante."""

    __tablename__ = "student_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)


class GradeRecordBase(SQLModel):
    """Base para registro de notas."""

    subject_id: int = Field(..., foreign_key="subjects.id")
    grade_type: str = Field(..., max_length=50)  # prova, trabalho, etc.
    value: float = Field(..., ge=0, le=10)
    max_value: float = Field(default=10.0, gt=0)
    date: Optional[datetime] = Field(default=None)


class GradeRecord(GradeRecordBase, TimestampMixin, table=True):
    """Registro de nota."""

    __tablename__ = "grade_records"

    id: Optional[int] = Field(default=None, primary_key=True)


class AttendanceRecordBase(SQLModel):
    """Base para registro de frequência."""

    class_meeting_id: int = Field(..., foreign_key="class_meetings.id")
    present: bool = Field(default=True)
    date: datetime = Field(...)


class AttendanceRecord(AttendanceRecordBase, TimestampMixin, table=True):
    """Registro de frequência."""

    __tablename__ = "attendance_records"

    id: Optional[int] = Field(default=None, primary_key=True)


class AcademicDocumentBase(SQLModel):
    """Base para documento acadêmico."""

    document_type: str = Field(..., max_length=50)
    file_path: str = Field(..., max_length=500)
    file_hash: str = Field(..., max_length=64)
    processed: bool = Field(default=False)


class AcademicDocument(AcademicDocumentBase, TimestampMixin, table=True):
    """Documento acadêmico processado."""

    __tablename__ = "academic_documents"

    id: Optional[int] = Field(default=None, primary_key=True)

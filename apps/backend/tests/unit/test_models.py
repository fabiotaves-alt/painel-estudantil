import pytest

from app.domain.models import Semester, Subject


class TestSemesterModel:
    """Testes para o modelo Semester."""

    def test_semester_creation(self):
        """Deve criar um semestre com dados válidos."""
        from datetime import datetime
        
        semester = Semester(
            name="2024.1",
            year=2024,
            start_date=datetime(2024, 2, 1),
            end_date=datetime(2024, 7, 31),
            is_current=True,
        )
        
        assert semester.name == "2024.1"
        assert semester.year == 2024
        assert semester.is_current is True

    def test_semester_year_validation(self):
        """Deve validar ano dentro do intervalo permitido."""
        from datetime import datetime
        
        # Ano válido
        semester = Semester(
            name="Teste",
            year=2024,
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
        )
        assert semester.year == 2024
        
        # Ano muito antigo deve falhar na validação do Field
        with pytest.raises(Exception):
            Semester(
                name="Antigo",
                year=1900,
                start_date=datetime(1900, 1, 1),
                end_date=datetime(1900, 12, 31),
            )


class TestSubjectModel:
    """Testes para o modelo Subject."""

    def test_subject_creation(self):
        """Deve criar uma disciplina com dados válidos."""
        subject = Subject(
            code="MAT101",
            name="Matemática I",
            professor="Dr. Silva",
            color="#FF5733",
            workload_hours=60,
            semester_id=1,
        )
        
        assert subject.code == "MAT101"
        assert subject.name == "Matemática I"
        assert subject.workload_hours == 60

    def test_subject_color_validation(self):
        """Deve validar cor no formato hexadecimal."""
        # Cor válida
        subject = Subject(
            code="TESTE",
            name="Teste",
            color="#00FF00",
            workload_hours=30,
            semester_id=1,
        )
        assert subject.color == "#00FF00"
        
        # Cor inválida deve falhar
        with pytest.raises(Exception):
            Subject(
                code="TESTE2",
                name="Teste 2",
                color="invalido",
                workload_hours=30,
                semester_id=1,
            )

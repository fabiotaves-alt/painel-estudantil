# Dashboard Acadêmico Backend

API FastAPI para o Dashboard Acadêmico - aplicativo desktop offline-first para visualização de dados acadêmicos.

## Instalação

```bash
pip install -e ".[dev]"
```

## Desenvolvimento

```bash
# Rodar servidor em desenvolvimento
uvicorn app.main:app --reload

# Rodar testes
pytest

# Lint
ruff check .

# Typecheck
mypy app
```

## Estrutura

- `app/api/v1/` - Rotas da API
- `app/domain/` - Modelos e regras de domínio
- `app/application/` - Casos de uso e serviços
- `app/infrastructure/` - Persistência e infraestrutura
- `app/schemas/` - Schemas Pydantic para validação
- `tests/` - Testes unitários e de integração

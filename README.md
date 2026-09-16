# Dashboard Acadêmico

Aplicativo desktop offline-first para visualizar, importar, validar e consultar dados acadêmicos extraídos de PDFs.

## Stack Tecnológica

### Frontend (Desktop)
- **React 18** + TypeScript (strict mode)
- **Vite** para build e dev server
- **TanStack Query** para gerenciamento de estado do servidor
- **React Hook Form** + Zod para formulários e validação
- **TailwindCSS** para estilização
- **Lucide** para ícones
- **Vitest** + React Testing Library para testes
- **Tauri 2** para empacotamento desktop

### Backend (API Local)
- **Python 3.12** + FastAPI
- **Pydantic v2** para validação de dados
- **SQLModel** + SQLAlchemy 2 (async)
- **SQLite** com WAL mode
- **Alembic** para migrações
- **pytest** para testes

## Estrutura do Projeto

```
/workspace
├── apps/
│   ├── desktop/          # Aplicação Tauri + React
│   │   ├── src/
│   │   │   ├── app/      # Componente App e configuração
│   │   │   ├── components/
│   │   │   ├── features/
│   │   │   ├── hooks/
│   │   │   ├── lib/
│   │   │   ├── schemas/
│   │   │   ├── styles/
│   │   │   └── types/
│   │   └── src-tauri/    # Código Rust/Tauri
│   └── backend/          # API FastAPI
│       ├── app/
│       │   ├── api/v1/
│       │   ├── domain/
│       │   ├── application/
│       │   ├── infrastructure/
│       │   └── schemas/
│       └── tests/
├── docs/
│   └── decisions/        # ADRs
└── packages/
    └── contracts/        # OpenAPI specs
```

## Comandos

### Desenvolvimento

```bash
# Instalar dependências do frontend
cd apps/desktop && npm install

# Instalar dependências do backend
cd apps/backend && pip install -e ".[dev]"

# Rodar frontend em dev
npm run dev

# Rodar backend em dev
cd apps/backend && uvicorn app.main:app --reload

# Rodar testes frontend
npm run test

# Rodar testes backend
cd apps/backend && pytest
```

### Build

```bash
# Build frontend
npm run build

# Build backend para produção
cd apps/backend && pyinstaller --onefile app/main.py

# Build Tauri (produz instaladores)
npm run tauri build
```

### Qualidade

```bash
# Lint frontend
npm run lint

# Typecheck frontend
npm run typecheck

# Lint backend
cd apps/backend && ruff check .

# Typecheck backend
cd apps/backend && mypy app
```

## Arquitetura

### Princípios
- **KISS**: Solução mais simples possível
- **YAGNI**: Nada especulativo
- **SoC**: Separação clara entre UI, negócio e persistência
- **SOLID**: Aplicado com pragmatismo
- **Offline-first**: Todos os dados persistidos localmente
- **Privacidade**: Sem envio de dados para nuvem

### Comunicação
- Tauri inicia o backend como sidecar
- Backend escuta em `127.0.0.1:{porta}` com token por execução
- Frontend comunica via HTTP local ou IPC Tauri
- Health check antes de liberar UI

### Segurança
- CORS restrito apenas para origem Tauri
- Token por sessão para API
- SQLite com WAL mode
- Backup/restore criptografado (futuro)

## Fases de Desenvolvimento

- [x] **Fase 0**: Planejamento e arquitetura
- [x] **Fase 1**: Fundação (este marco)
- [ ] **Fase 2**: CRUD disciplinas/semestres
- [ ] **Fase 3**: Grade semanal
- [ ] **Fase 4**: Importação de PDF
- [ ] **Fase 5**: Notas e frequência
- [ ] **Fase 6**: Empacotamento final

## ADRs (Architecture Decision Records)

Consulte `docs/decisions/` para decisões arquiteturais documentadas.

## Licença

MIT

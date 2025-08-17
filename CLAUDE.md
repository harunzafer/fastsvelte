# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastSvelte is a fullstack SaaS starter kit designed for developers who want to rapidly build modern web applications using FastAPI (Python) and SvelteKit (TypeScript). It provides a secure, clean, and extensible foundation for B2B or B2C SaaS products.

Four main components:

- **Backend**: FastAPI with PostgreSQL, using dependency injection and repository pattern
- **Frontend**: SvelteKit SPA with session-based authentication
- **Database**: PostgreSQL with Sqitch migrations
- **Landing**: Public SvelteKit marketing site
- **Nexus-Svelte**: Premium TailwindCSS + DaisyUI admin dashboard theme with pre-built components

## Development Commands

### Frontend (SvelteKit)

```bash
cd frontend
npm run dev              # Start development server
npm run build            # Build for production
npm run preview          # Preview production build
npm run lint             # Run linting (prettier + eslint)
npm run check            # Type checking with svelte-check
npm run test             # Run unit tests (vitest) and e2e tests (playwright)
npm run test:unit        # Run only unit tests
npm run test:e2e         # Run only e2e tests
```

### Nexus-Svelte (Premium Theme)

```bash
cd nexus-svelte
npm install              # Install dependencies
npm run dev              # Start development server
npm run build            # Build for production
npm run preview          # Preview production build
```

**Important**: Use Nexus-Svelte theme components and patterns whenever possible. Avoid creating new components if the theme already has examples. Copy/adapt existing theme components rather than building from scratch.

### Backend (FastAPI)

```bash
cd backend
# Create virtual environment first
python3.12 -m venv .venv
source .venv/bin/activate
pip install pip-tools
pip-compile --no-strip-extras requirements.in  # Generate requirements.txt

# Development
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Testing
pytest                   # Run all tests
pytest test/unit/        # Run specific test directory
```

### Database (Sqitch)

```bash
cd db
./sqitch.sh dev deploy             # Deploy migrations to dev DB
./sqitch.sh dev revert --to <name> # Revert to specific migration
sqitch add <name> -n "<description>" # Create new migration
```

### Docker Development

```bash
# Option 1: Local FastAPI + Docker services
docker compose up db -d
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000

# Option 2: Everything in Docker
docker compose --env-file .env.docker up --build
```

## Architecture & Patterns

### Backend Architecture (FastAPI)

- **Dependency Injection**: Uses `dependency-injector` for IoC container
- **Repository Pattern**: All database access through repositories in `app/data/repo/`
- **Service Layer**: Business logic in `app/service/`
- **Absolute Imports**: Always use `from app.xxx` not relative imports
- **Configuration**: Environment variables with `pydantic_settings`, prefixed with `FASTSVELTE`

**Directory Structure**:

```
app/
├── main.py              # FastAPI app + DI container setup
├── api/route/           # HTTP endpoints
├── service/             # Business logic
├── data/repo/           # Database repositories
├── model/               # Request/response models
├── config/              # Settings & DI container
└── util/                # Utilities (auth, cookies, etc.)
```

### Frontend Architecture (SvelteKit)

- **Session-based Auth**: Uses HTTP-only cookies, checks via `/api/user/me`
- **API Generation**: Uses Orval to generate API client from OpenAPI spec
- **State Management**: Svelte 5 runes for local state, stores for global auth state
- **Styling**: TailwindCSS v4 + DaisyUI components

**Key Files**:

- `src/lib/auth/auth.svelte.ts` - Auth store and session management
- `src/lib/api/axios.js` - API client with 401 handling
- `src/lib/api/gen/` - Auto-generated API client (don't edit manually)

### Database Strategy

- **Migrations**: Sqitch for schema versioning
- **Naming**: Repositories named after primary domain entity (e.g., `UserRepo` even if it joins multiple tables)
- **Development**: Use `./sqitch.sh dev` commands to avoid manual SQL execution

## Common Workflows

### Adding New API Endpoints

1. Create route in `backend/app/api/route/`
2. Add service method in `backend/app/service/`
3. Add repository method in `backend/app/data/repo/` if needed
4. Update models in `backend/app/model/`
5. Run `cd frontend && npm run generate` to update API client

### Authentication Flow

- Frontend checks session via `/api/user/me` on load
- All API requests use shared client that handles 401 redirects
- Cross-tab session validation with localStorage debouncing
- No JWT tokens - pure session cookies

### Database Changes

1. `cd db && sqitch add feature_name -n "Description"`
2. Edit generated SQL files in `deploy/`, `revert/`, `verify/`
3. `./sqitch.sh dev deploy` to apply changes
4. Update repository methods to use new schema

## Testing Strategy

### Backend

- Unit tests with pytest
- Repository tests use test database
- Service tests mock repository dependencies

### Frontend

- Unit tests with Vitest
- E2E tests with Playwright
- Component tests with Vitest browser mode

## Environment & Configuration

### Backend

- Environment variables prefixed with `FASTSVELTE_`
- Use `pydantic_settings` for configuration management
- Required variables will cause startup failure if missing

### Frontend

- Uses Vite environment variables
- API base URL configured in `src/lib/api/axios.js`

### Database

- Connection strings in `.env` files
- Separate configs for dev/beta/prod environments
- Use `sqitch.sh` wrapper script for environment-specific commands

## Code Style

### Backend

- Absolute imports: `from app.service.user_service import UserService`
- Repository naming: `user_repo` for variables, `UserRepo` for classes
- Service methods return domain models, not database records
- Use dependency injection for all cross-cutting concerns

### Frontend

- TypeScript strict mode enabled
- Prettier + ESLint for formatting
- Svelte 5 runes syntax preferred over legacy stores
- Component files use PascalCase, other files use kebab-case
- **Use Nexus-Svelte theme**: Always check `nexus-svelte/` for existing components before creating new ones
- Copy/adapt theme patterns for consistent UI/UX across the application

### Instructions for Claude Code

Always follow the following rules when helping me:

1. Ask clarifying questions to understand the problem entirely.
2. Go step by step. Do not try to code right away. First suggest your approach and after my confirmation you can give me the code.
3. Keep your answers as short as possible.
4. Always provide the file path for the code you suggest.
5. Always use datetime.now(timezone.utc) instead of datetime.utcnow(),
6. Always use TIMESTAMPTZ instead of TIMESTAMPT
7. Always use `list` instead of `List` from typing. Same for other types.
8. Always use IF NOT EXISTS and IF EXISTS where appropriate for our SQL migration scripts.
9. Our repositories should always return pydantic models or primitive types but we never return dictionaries.
10. Never mention Claude or Claude Code in commit messages - keep them professional and focused on the changes made.
11. Always run `npm run format` in the frontend directory before committing to ensure code passes Prettier formatting checks in CI/CD pipeline.

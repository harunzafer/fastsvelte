# Project Structure Overview

The project structure shown here reflects the current layout of FastSvelte. As the project evolves, minor adjustments may be made for clarity, extensibility, or performance. Always refer to the latest codebase for the most accurate structure.

fastsvelte/
├── README.md                    # Root-level readme for the entire repo
├── docker-compose.yml           # Orchestrates backend, frontend, and Postgres
├── create.py                    # CLI to scaffold a new project: `fastsvelte create my_app`

├── backend/                     # FastAPI backend (auth, users, notes, OpenAI integration)
│   └── ...                      # See detailed backend structure above

├── frontend/                    # Authenticated SvelteKit SPA (dashboard, notes, profile)
│   └── ...                      # See detailed frontend structure above

├── landing/                     # Public marketing site (SvelteKit)
│   └── ...                      # Simple +page.svelte for the landing page

├── db/                          # Sqitch-based PostgreSQL migrations
│   ├── deploy/                  # Migration "up" scripts
│   ├── revert/                  # Migration "down" scripts
│   ├── verify/                  # Test the correctness of each migration
│   ├── sqitch.plan              # Migration plan (order of scripts)
│   ├── sqitch.conf              # Sqitch config (DB target etc.)
│   └── sqitch.sh                # Script to run migrations via Docker

├── .github/
│   └── workflows/               # GitHub Actions CI (backend, frontend, landing linting/tests)
│       ├── backend.yml
│       ├── frontend.yml
│       └── landing.yml


## Backend Folder Breakdown

backend/
├── Dockerfile                  # Backend container image definition
├── requirements.txt            # Production dependencies
├── requirements.dev.txt        # Dev/test/lint dependencies
├── README.md                   # Backend usage and setup instructions

├── app/                        # Main application code
│
│   ├── main.py                 # FastAPI app initialization + DI container setup
│
│   ├── api/                    # HTTP interface layer
│   │   ├── middleware/         # Global request/response hooks
│   │   │   ├── auth.py         # Inject user session from cookie, enforce auth
│   │   │   └── error_handlers.py # Custom exception formatting
│   │   ├── route/              # API route handlers (entry points)
│   │   │   ├── auth.py         # /login, /signup, /logout endpoints
│   │   │   ├── note.py         # /notes CRUD endpoints
│   │   │   └── user.py         # /me, update profile, change password
│   │   └── router.py           # Master router that includes all route modules
│
│   ├── config/                 # App configuration & DI setup
│   │   ├── settings.py         # Load env variables and runtime config
│   │   └── container.py        # Dependency Injector container (services, repos, config)
│
│   ├── data/                   # Database interaction
│   │   ├── db_config.py        # Create asyncpg connection pool
│   │   └── repo/               # Raw SQL repositories
│   │       ├── base_repo.py    # Common query helpers + connection management
│   │       ├── note_repo.py    # DB access for note records
│   │       ├── session_repo.py # Session storage and lookup
│   │       └── user_repo.py    # User creation, lookup, and update
│
│   ├── model/                  # Data classes and schema definitions
│   │   ├── auth.py             # LoginRequest, SignupRequest, AuthResult
│   │   ├── note.py             # NoteEntity, CreateNoteRequest, NoteResponse
│   │   ├── session.py          # Session object (DB + cookie-related)
│   │   └── user.py             # UserEntity, CreateUserRequest, UserResponse
│
│   ├── service/                # Business logic layer
│   │   ├── auth_service.py     # Login, signup, session management
│   │   ├── note_service.py     # Create, update, delete, list notes
│   │   ├── openai_service.py   # AI functionality (e.g. summarize notes)
│   │   └── user_service.py     # Profile management and password update
│
│   ├── util/                   # Utility helpers
│   │   ├── cookie.py           # Set/delete secure session cookies
│   │   └── session.py          # Session validation helpers


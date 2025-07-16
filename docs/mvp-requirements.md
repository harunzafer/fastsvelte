# FastSvelte MVP Requirements

## 1. User Authentication

- Email/password signup & login
- Password hashing using passlib (bcrypt)
- Session-based authentication using secure, HTTP-only, SameSite cookies
- Authenticated endpoints protected in backend
- Frontend supports login/signup/logout
- No token-based auth (SPA can't access cookie)

## 2. User Management

- View/update profile (name, email)
- Change password (requires current password)
- Profile page on frontend

## 3. AI-Enhanced CRUD Example

- Note model: id, title, content, created_at, updated_at
- Integration with OpenAI API (e.g., summarization or categorization of note)
- User can: Create, view, update, delete notes; Trigger AI-based processing on a note
- Notes are scoped per user
- Frontend has basic UI for CRUD and AI actions

## 4. Frontend Features

- Built with SvelteKit (SPA mode)
- Tailwind CSS + DaisyUI for styling
- Shared layout: topbar, sidebar
- Responsive design
- Dark mode toggle
- API abstraction (api.ts)
- Protected routes via session check

## 5. Backend Architecture

- Built with FastAPI
- No ORM — uses asyncpg with base_repo
- Code structure: routers/, services/, schemas/, repos/

## 6. Local Dev & Deployment

- Dockerfile for backend & frontend
- docker-compose.yml with PostgreSQL
- .env support for config
- Dev scripts (e.g., make dev, make test)

## 7. CI & Linting

- GitHub Actions: Lint backend (black, ruff), Lint frontend (prettier), Run backend unit tests
- Prettier for Svelte files

## 8. Project Scaffolding Tool

- CLI command: fastsvelte create my_app
- Generates a new folder with code customized for my_app
- Includes backend/frontend, env setup, Makefile, etc.

## 9. Monetization & Access

- Landing page for marketing
- Documentation page (hosted on GitHub)
- One-time payment grants repo access (via GitHub)
- Scaffold script and docs included in private repo

## 10. B2B and B2C Mode Support

- Each user belongs to an organization
- B2B mode: multiple users per organization
- B2C mode: one user per organization
- Front-end may not expose organization management in MVP

## 11. Subscription Plans & Pricing Tiers

- Users (or their organizations) can be assigned to a subscription plan
- Each plan defines usage limits (e.g., notes per month, API calls) and feature access
- Plans can be free or paid (one-time or recurring)
- The system should support associating users or organizations with a current active plan
- Frontend may not expose plan management in MVP, but backend must support it
## Project Structure

More or less, we follow this structure:

```bash
app/
├── main.py
├── config.py
├── api/
│   ├── __init__.py
│   ├── route/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│   │   └── auth.py  # <-- /login and /logout go here
│   ├── model/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── auth.py  # <-- Auth-related request/response models
│   └── guard/
├── core/
│   ├── __init__.py
│   ├── user.py
│   └── auth.py      # <-- Auth service with login/logout logic
├── error/
├── data/
│   ├── repo/
│   │   ├── user.py
│   │   └── token.py # <-- If you store tokens/sessions
├── util/
│   └── auth.py      # <-- Auth utilities (JWT, hashing, etc.)
└── test/
```

We always user absolute imports and not relative imports. 

When a repo reads and writes to the user table we call it user_repo.  When your repository needs to join multiple tables, I'd recommend naming the repo based on its primary domain entity or the main purpose it serves, not all the tables it joins.

Example:

```py
# user.py
class UserRepo:
    def get_users_with_items(self):
        # JOIN users and items tables
```

## Configuration Management

We use `pydantic_settings` for configuration — it's simple, elegant, and powerful.

- All configuration is read from environment variables.
- Variables are prefixed with `FASTSVELTE` to prevent naming conflicts.
- Both `.env` and system environment variables are supported.
- If a required variable is missing (i.e., no default and not defined), the app will fail to start with a clear error.
- In code, we don’t use the prefix. For example, the environment variable `FASTSVELTEDB_URL` is accessed via `settings.db_url`.
- `pydantic_settings` is much simpler than `dependency_injector.providers.Configuration`, so we prefer it for global settings.


# Dependency Management

Create a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install `pip-compile`. With `pip-compile`, we'll be able to separate direct dependencies from transitive dependencies. 

```bash
pip install pip-tools
```

Create an empty requirements.in file

```bash
touch requirements.in
```

Run `pip-compile` to generate the requirements.txt file

```bash
pip-compile --no-strip-extras requirements.in
```

Notice that, pip-compile doesn't addd itself or `pip-tools` to the requirements.txt file, since it is only required for development.

Now we can add new dependencies to the requirements.in file and run `pip-compile` again to generate the requirements.txt file.


## Running Locally

### Option 1: Local FastAPI + Docker services

This uses `.env` file

```bash
docker compose up db azurite
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Option 2: Run everything in Docker (for testing before deploy)

```bash
docker compose --env-file .env.docker up --build
```

In both cases, you should be able to ping the service with:

```bash
curl http://localhost:8000/ping
```


## Deployment

To Deploy Azure Container Apps assuming Azure CLI setup is complete:

```bash
az containerapp up \
  --resource-group fastsvelte-rg \
  --name fastsvelte-api \
  --ingress external \
  --target-port 3100 \
  --source .
```

See the [Azure Container Apps documentation](https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app?tabs=web-app-fastapi) for more information.


## Environment Strategy

We have three resource groups on Azure as `dev`, `beta` and `prod`. All the components (db, api, blobstore etc.) are available for both `beta` and `prod`. To avoid costs, we don't have most components for the `dev` as the application is mostly testable locally. 
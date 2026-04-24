# Project Setup

## Set up Repo
In Github:
Create new repo called cs_631_project and make sure it is public

In WSL/VS Code Terminal:
```bash
mkdir cs_631_project
cd cs_631_project/
git init
git branch -m main
git remote add origin git@github.com:mbel12345/cs_631_project.git
vim README.md
git add . -v
git commit -m "Initial commit"
git push -u origin main
```

## Set up virtual environment
In WSL/VS Code Terminal:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Build image and start container
Note: This must be already running for all local testing
In WSL/VS Code Terminal:
```bash
docker compose down -v
docker compose up --build
```

## Import sample data
In WSL/VS Code Terminal:
```bash
python3 -m app.populate_tables
```

## Run FastAPI app locally
In WSL/VS Code Terminal:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

## Using the App
Pgadmin: http://localhost:5050/
Swagger UI locally: http://localhost:8001/docs
Swagger UI in container: http://localhost:8000/docs

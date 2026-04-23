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

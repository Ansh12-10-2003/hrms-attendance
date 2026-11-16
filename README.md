# HRMS Attendance

A punch in/out attendance system built with FastAPI and SQLite.
Built end to end as a DevOps learning project.

## Features
- Create employees
- Punch in / punch out with business rules (no double punch-in)
- Attendance history per employee

## Run locally
1. `python -m venv venv` and activate it
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload`
4. Open http://127.0.0.1:8000/docs

## Roadmap
- [x] Backend API
- [ ] Web frontend
- [ ] Docker
- [ ] CI/CD with GitHub Actions
- [ ] Kubernetes (minikube)
- [ ] Monitoring

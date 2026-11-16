from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas
from database import engine, SessionLocal
from models import utc_now

# Creates the tables in hrms.db if they don't exist yet
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/employees", response_model=schemas.EmployeeOut, status_code=201)
def create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    employee = models.Employee(name=data.name, email=data.email)
    db.add(employee)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(employee)
    return employee


@app.get("/employees", response_model=list[schemas.EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()


@app.post("/punch-in/{employee_id}", response_model=schemas.AttendanceOut, status_code=201)
def punch_in(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(models.Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    open_record = (
        db.query(models.Attendance)
        .filter(models.Attendance.employee_id == employee_id,
                models.Attendance.punch_out.is_(None))
        .first()
    )
    if open_record:
        raise HTTPException(status_code=400, detail="Already punched in")

    record = models.Attendance(employee_id=employee_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.post("/punch-out/{employee_id}", response_model=schemas.AttendanceOut)
def punch_out(employee_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(models.Attendance)
        .filter(models.Attendance.employee_id == employee_id,
                models.Attendance.punch_out.is_(None))
        .first()
    )
    if not record:
        raise HTTPException(status_code=400, detail="Not punched in")

    record.punch_out = utc_now()
    db.commit()
    db.refresh(record)
    return record


@app.get("/attendance/{employee_id}", response_model=list[schemas.AttendanceOut])
def attendance_history(employee_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Attendance)
        .filter(models.Attendance.employee_id == employee_id)
        .order_by(models.Attendance.punch_in.desc())
        .all()
    )
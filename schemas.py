from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class EmployeeCreate(BaseModel):
    name: str
    email: str

class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str

class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    punch_in: datetime
    punch_out: Optional[datetime] = None
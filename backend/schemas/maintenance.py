from pydantic import BaseModel


class MaintenanceRecord(BaseModel):
    asset: str = ""
    issue: str = ""
    priority: str = ""
    operator: str = ""
    recommendation: str = ""
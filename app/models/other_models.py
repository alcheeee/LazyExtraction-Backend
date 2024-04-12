from sqlmodel import SQLModel, Field


class Jobs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    job_name: str
    job_type: str
    income: int
    energy_required: int
    description: str
    required_stats: str  # Json
    stat_changes: str



from pydantic import BaseModel
import datetime


class gateway(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class refrigerator(BaseModel):
    id: int
    name: str | None = None
    temp_min: float | None = None
    temp_max: float | None = None

    class Config:
        orm_mode = True


class monitor(BaseModel):
    id: int
    name: str | None = None

    class Config:
        orm_mode = True


class monitor_detail(monitor):
    moved: bool | None = None
    moved_datetime: datetime.datetime | None = None
    temp: float | None = None
    last_data: datetime.datetime | None = None
    refrigerator: refrigerator
    id_refrigerator: int | None = None

    class Config:
        orm_mode = True


class data(BaseModel):
    rssi: int
    temp: int
    openings: int

    class Config:
        orm_mode = True


class data_monitor(data):
    id: int

    class Config:
        orm_mode = True

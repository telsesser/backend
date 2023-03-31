from pydantic import BaseModel


class gateway(BaseModel):
    id: int
    gateway: str

    class Config:
        orm_mode = True


class monitor(BaseModel):
    id: int
    monitor: str

    class Config:
        orm_mode = True


class data(BaseModel):
    rssi: int
    temperatura: int
    aperturas: int

    class Config:
        orm_mode = True

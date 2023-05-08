from pydantic import BaseModel


class gateway(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class monitor(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class data(BaseModel):
    rssi: int
    temperatura: int
    openings: int

    class Config:
        orm_mode = True

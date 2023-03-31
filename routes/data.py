from fastapi import APIRouter, Depends
from typing import List, Annotated

from auth.users import get_current_user
from schemas.data import gateway, monitor, data
from schemas.users import User
from crud import data as crud


router = APIRouter()


@router.get(
    "/gateways",
    response_model=List[gateway],
    dependencies=[Depends(get_current_user)],
)
def get_gateways(current_user: Annotated[User, Depends(get_current_user)]):
    return crud.get_gateways_user(current_user.id)


@router.get(
    "/monitors/{id_gateway}",
    response_model=List[monitor],
    dependencies=[Depends(get_current_user)],
)
def get_monitors(id_gateway: int):
    return crud.get_monitors_gateway(id_gateway)


@router.get(
    "/data/{id_monitor}",
    response_model=List[data],
    dependencies=[Depends(get_current_user)],
)
def get_data(id_monitor: int):
    return crud.get_data_monitor(id_monitor)

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated

from auth.users import get_current_user
from schemas.data import gateway, monitor, data
from schemas.users import User
from crud import data as crud
import random

router = APIRouter()


@router.get("/monitors_online")
def get_monitors_online(current_user: Annotated[User, Depends(get_current_user)]):
    res = {"disponible": 30, "total": 35}
    return res


@router.get("/ubicacion")
def get_ubicacion(current_user: Annotated[User, Depends(get_current_user)]):
    res = {"disponible": 34, "total": 35}
    return res


@router.get("/temperatura")
def get_teperatura(current_user: Annotated[User, Depends(get_current_user)]):
    res = {"disponible": 24, "total": 35}
    return res


@router.get("/openings")
def get_teperatura(current_user: Annotated[User, Depends(get_current_user)]):
    res = {
        "1/5/2023": 1120,
        "2/5/2023": 176,
        "3/5/2023": 822,
        "4/5/2023": 1023,
        "5/5/2023": 983,
        "6/5/2023": 1345,
        "7/5/2023": 1264,
    }
    return res


@router.get("/personas")
def get_teperatura(current_user: Annotated[User, Depends(get_current_user)]):
    res = {"cantidad": 10254}
    return res


@router.get("/tasas")
def get_teperatura(current_user: Annotated[User, Depends(get_current_user)]):
    res = {"cantidad": "12%"}
    return res


@router.get(
    "/refrigerators",
)
def get_refrigerators():
    res = [
        {
            "id": x,
            "name": f"heladera {x}",
            "temp": random.randint(-9, 0),
            "temp_min": -8,
            "temp_max": -2,
        }
        for x in range(10)
    ]
    return res


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
def get_monitors(
    id_gateway: int, current_user: Annotated[User, Depends(get_current_user)]
):
    return crud.get_monitors_gateway(id_gateway, current_user.id)


@router.get(
    "/data/{id_monitor}",
    response_model=List[data],
    dependencies=[Depends(get_current_user)],
)
def get_data(id_monitor: int, current_user: Annotated[User, Depends(get_current_user)]):
    res = crud.get_data_monitor(id_monitor, current_user.id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado"
        )
    return res

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Annotated, Optional
import datetime
from auth.users import get_current_user
import schemas.data  # import gateway, data_monitor, data, monitor
from schemas.users import User

# from crud import data as crud
import crud.data, crud.users
import random

router = APIRouter()


@router.get(
    "/monitors_user",
    response_model=List[schemas.data.monitor],
    dependencies=[Depends(get_current_user)],
)
def get_monitors_online(current_user: Annotated[User, Depends(get_current_user)]):
    res = crud.data.get_data_for_monitors(id_user=current_user.id)
    return res


@router.get(
    "/monitors/detail",
    response_model=List[schemas.data.monitor_detail],
    dependencies=[Depends(get_current_user)],
)
def get_monitors_detail(user: Annotated[User, Depends(get_current_user)]):
    data_monitors = crud.data.get_data_from_monitors(id_company=user.id_company)
    return data_monitors


@router.get("/monitors/info")
def get_monitors_info(user: Annotated[User, Depends(get_current_user)]):
    data_monitors = crud.data.get_data_from_monitors(id_company=user.id_company)
    res = {
        "monitors": {
            "moved": 0,
            "offline": 0,
            "temp_out_range": 0,
            "total": len(data_monitors),
        }
    }
    current_time = datetime.datetime.now()
    for d in data_monitors:
        time_difference = current_time - d.last_data
        if time_difference > datetime.timedelta(hours=24):
            res["monitors"]["offline"] += 1
        if not d.moved:
            res["monitors"]["moved"] += 1
        if d.refrigerator.temp_min < d.temp < d.refrigerator.temp_max:
            res["monitors"]["temp_out_range"] += 1
    res["openings"] = crud.data.get_openings_last_day(id_company=user.id_company)
    return res


@router.get("/ubicacion")
def get_ubicacion(current_user: Annotated[User, Depends(get_current_user)]):
    data_monitors = crud.data.get_data_for_monitors(id_user=current_user.id)
    res = {"disponible": 0, "total": len(data_monitors)}
    for d in data_monitors:
        if not d.moved:
            res["disponible"] += 1
    return res


@router.get("/aperturas")
def get_aperturas(user: Annotated[User, Depends(get_current_user)]):
    # res = crud.data.get_openings_by_day_last_week(id_user=current_user.id)
    res = crud.data.get_openings_last_day(id_company=user.id_company)
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
    "/temperatura",
    # response_model=List[data_monitor],
    dependencies=[Depends(get_current_user)],
)
def get_temperatura(current_user: Annotated[User, Depends(get_current_user)]):
    data_monitors = crud.data.get_data_for_monitors(id_user=current_user.id)
    res = {"disponible": 0, "total": len(data_monitors)}
    for d in data_monitors:
        if d.refrigerator.temp_min < d.temp < d.refrigerator.temp_max:
            res["disponible"] += 1
    return res


@router.get(
    "/gateways",
    response_model=List[schemas.data.gateway],
    dependencies=[Depends(get_current_user)],
)
def get_gateways(current_user: Annotated[User, Depends(get_current_user)]):
    return crud.data.get_gateways_user(current_user.id)


@router.get(
    "/monitors/{id_gateway}",
    response_model=List[schemas.data.monitor],
    dependencies=[Depends(get_current_user)],
)
def get_monitors(
    id_gateway: int, current_user: Annotated[User, Depends(get_current_user)]
):
    return crud.data.get_monitors_gateway(id_gateway, current_user.id)


@router.get(
    "/data/{id_monitor}",
    response_model=List[schemas.data.data],
    dependencies=[Depends(get_current_user)],
)
def get_data(id_monitor: int, current_user: Annotated[User, Depends(get_current_user)]):
    res = crud.data.get_data_monitor(id_monitor, current_user.id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado"
        )
    return res

    ### historicos


@router.get("/historical/openings", dependencies=[Depends(get_current_user)])
def get_historical_openings(
    start_date: str,
    end_date: str,
    id_monitors: Annotated[list[int], Query()] = None,
    current_user: User = Depends(get_current_user),
):
    if id_monitors is None:
        monitors = crud.data.get_data_for_monitors(id_user=current_user.id)
        id_monitors = [monitor.id for monitor in monitors]
    data = crud.data.get_openings_by_date_range(
        id_monitors=id_monitors, start_date=start_date, end_date=end_date
    )

    return data

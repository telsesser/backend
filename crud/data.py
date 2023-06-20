from database.config import session_db as db
from database import models
from datetime import datetime, timedelta
from sqlalchemy import func
from typing import List


def get_gateways_user(id_user: int, skip: int = 0, limit: int = 100):
    try:
        user = db.query(models.users).filter(models.users.id == id_user).first()
        qr = (
            db.query(models.monitors.id_gateway)
            .filter(models.monitors.id_company == user.id_company)
            .offset(skip)
            .distinct()
            .all()
        )
        id_gateways = [x.id_gateway for x in qr]
        gateways = (
            db.query(models.gateways).filter(models.gateways.id.in_(id_gateways)).all()
        )
    except Exception as e:
        print(e)
        gateways = {"error": "error"}
        db.rollback()
    return gateways


def get_monitors_gateway(
    id_gateway: int, id_user: int, skip: int = 0, limit: int = 100
):
    try:
        user = db.query(models.users).filter(models.users.id == id_user).first()
        res = (
            db.query(models.monitors)
            .filter(
                models.monitors.id_gateway == id_gateway,
                models.monitors.id_company == user.id_company,
            )
            .offset(skip)
            .all()
        )
    except Exception as e:
        print(e)
        res = {"error": "error"}
        db.rollback()
    return res


def get_data_monitor(id_monitor: int, id_user: int, skip: int = 0, limit: int = 100):
    try:
        user = db.query(models.users).filter(models.users.id == id_user).first()
        qr = (
            db.query(models.monitors.id)
            .filter(models.monitors.id_company == user.id_company)
            .offset(skip)
            .all()
        )
        if id_monitor in [x.id for x in qr]:
            res = (
                db.query(models.data)
                .filter(models.data.id_monitor == id_monitor)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            res = False
    except Exception as e:
        print(e)
        res = {"error": "error"}
        db.rollback()
    return res


def get_data_from_monitors(id_company: int, skip: int = 0, limit: int = 100):
    try:
        # user = db.query(models.users).filter(models.users.id == id_user).first()
        monitors = (
            db.query(models.monitors)
            .filter(models.monitors.id_company == id_company)
            .offset(skip)
            .limit(limit)
            .all()
        )

    except Exception as e:
        print(e)
        monitors = []
        db.rollback()

    return monitors


def get_refrigerator_attributes(id_user: int):
    try:
        user = db.query(models.users).filter(models.users.id == id_user).first()
        monitors = (
            db.query(models.monitors.id, models.monitors.id_refrigerator)
            .filter(models.monitors.id_company == user.id_company)
            .all()
        )
        refrigerator_attributes = []
        for monitor in monitors:
            refrigerator = (
                db.query(models.refrigerators)
                .filter(models.refrigerators.id == monitor.id_refrigerator)
                .first()
            )
            if refrigerator:
                print(refrigerator.__dict__)
                refrigerator_attributes.append(refrigerator)
        res = refrigerator_attributes

    except Exception as e:
        print(e)
        res = {"error": "error"}
        db.rollback()
    return res


import datetime


def get_openings_by_day_last_week(id_user: int):
    res = {}
    # Obtener la fecha actual
    current_date = datetime.datetime.now().date()
    # Obtener la fecha de hace una semana
    last_week = current_date - timedelta(days=7)

    try:
        user = db.query(models.users).filter(models.users.id == id_user).first()
        monitors = (
            db.query(models.monitors.id)
            .filter(models.monitors.id_company == user.id_company)
            .all()
        )
        # Realizar la consulta para obtener la suma de aperturas por día
        result = (
            db.query(func.date(models.data.timestmp), func.sum(models.data.openings))
            .filter(models.data.timestmp >= last_week)
            .filter(models.data.id_monitor.in_([m.id for m in monitors]))
            .group_by(func.date(models.data.timestmp))
            .all()
        )

        # Formatear el resultado en el diccionario de respuesta
        for date, sum_openings in result:
            res[date.strftime("%d/%m/%Y")] = sum_openings

    except Exception as e:
        print(e)
        db.rollback()

    return res


def get_openings_last_day(id_company: int):
    # Obtener la fecha actual
    current_date = datetime.datetime.now().date() - timedelta(days=5)
    # Obtener la fecha de hace una semana
    res = -1
    try:
        # user = db.query(models.users).filter(models.users.id == id_user).first()
        monitors = (
            db.query(models.monitors.id)
            .filter(models.monitors.id_company == id_company)
            .all()
        )
        # Realizar la consulta para obtener la suma de aperturas por día
        result = (
            db.query(func.sum(models.data.openings).label("total_openings"))
            .filter(models.data.timestmp >= current_date)
            .filter(models.data.id_monitor.in_([m.id for m in monitors]))
            .group_by(func.date(models.data.timestmp))
            .first()
        )
        res = result.total_openings
        # Formatear el resultado en el diccionario de respuesta

    except Exception as e:
        print(e)
        db.rollback()

    return res


def get_openings_by_date_range(id_user: int, start_date: str, end_date: str):
    res = {}
    try:
        user = db.query(models.users).filter(models.users.id == id_user).first()
        monitors = (
            db.query(models.monitors.id)
            .filter(models.monitors.id_company == user.id_company)
            .all()
        )
        # Convertir las fechas de inicio y fin al formato adecuado
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        print([m.id for m in monitors])
        # Realizar la consulta para obtener la suma de aperturas por día
        result = (
            db.query(func.date(models.data.timestmp), func.sum(models.data.openings))
            .filter(models.data.timestmp >= start_date)
            .filter(models.data.timestmp <= end_date)
            .filter(models.data.id_monitor.in_([m.id for m in monitors]))
            .group_by(func.date(models.data.timestmp))
            .all()
        )
        print(result)
        # Formatear el resultado en el diccionario de respuesta
        for date, sum_openings in result:
            print(date)
            res[date.strftime("%Y-%m-%d")] = sum_openings

    except Exception as e:
        print(e)
        db.rollback()

    return res

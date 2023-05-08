from database.config import session_db as db
from database import models


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
    db.commit()
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
    db.commit()
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
    db.commit()
    return res

from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.schemas.schema_water_sprinkler import WaterSprinklerCreate, WaterSprinklerDelete, WaterSprinklerPut, \
    WaterSprinklerAddSettings, WaterSprinklerPatch
from app.models.water_sprinkler import WaterSprinkler, Setting
from app.db.dependency import get_db


water_sprinkler_router = APIRouter(
    prefix="/water-sprinkler"
)


@water_sprinkler_router.get("/get/", status_code=status.HTTP_200_OK)
async def water_sprinkler_list(db: Session = Depends(get_db)):
    try:
        water_sprinklers = db.query(WaterSprinkler).all()

        for water_sprinkler in water_sprinklers:
            settings = water_sprinkler.settings

        response = jsonable_encoder(water_sprinklers)

        return JSONResponse(content=response)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@water_sprinkler_router.get("/get/{id}/", status_code=status.HTTP_200_OK)
async def water_sprinkler_retrieve(id: int, db: Session = Depends(get_db)):
    try:
        water_sprinkler = db.query(WaterSprinkler).filter(WaterSprinkler.id == id).first()
        if water_sprinkler is not None:
            water_sprinkler.settings
            water_sprinkler.plants
            response = jsonable_encoder(water_sprinkler)

        return JSONResponse(content=response)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@water_sprinkler_router.post("/create/", status_code=status.HTTP_201_CREATED)
async def water_sprinkler_create(water_sprinkler: WaterSprinklerCreate, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(water_sprinkler)

        settings_data = data.pop("settings")

        water_sprinkler_data = WaterSprinkler(**data)
        db.add(water_sprinkler_data)
        db.commit()
        db.flush(water_sprinkler_data)

        for setting in settings_data:
            setting["water_sprinklers_id"] = water_sprinkler_data.id

            is_active = setting.pop("is_active")
            setting["is_active"] = True if is_active in ["True", "true"] else False

            date_start = setting.pop("date_start")
            setting["date_start"] = datetime.strptime(date_start, '%Y-%m-%d').date()

            new_setting = Setting(**setting)
            db.add(new_setting)
            db.commit()

        data["settings"] = settings_data
        new_data = jsonable_encoder(data)

        return JSONResponse(content=new_data)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@water_sprinkler_router.post("/add-settings/")
async def water_sprinkler_add_settings(water_sprinkler: WaterSprinklerAddSettings, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(water_sprinkler)

        id = data.pop("id")
        settings_data = data.pop("settings")

        for setting in settings_data:
            setting["water_sprinklers_id"] = id

            is_active = setting.pop("is_active")
            setting["is_active"] = True if is_active in ["True", "true"] else False

            date_start = setting.pop("date_start")
            setting["date_start"] = datetime.strptime(date_start, '%Y-%m-%d').date()

            new_setting = Setting(**setting)
            db.add(new_setting)

        db.commit()
        print("Sucess")

        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@water_sprinkler_router.put("/update/")
async def water_sprinkler_update(water_sprinkler: WaterSprinklerPut, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(water_sprinkler)

        id = data.pop("id")

        settings_data = data.pop("settings")

        for setting in settings_data:
            setting_id = setting.pop("id")
            db.execute(update(Setting).where(Setting.id == setting_id).values(setting))

        db.execute(update(WaterSprinkler).where(WaterSprinkler.id == id).values(data))

        db.commit()

        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@water_sprinkler_router.patch("/update-data/", status_code=status.HTTP_204_NO_CONTENT)
async def water_sprinkler_patch(water_sprinkler: WaterSprinklerPatch, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(water_sprinkler)

        id = data.pop("id")

        settings_data = data.pop("settings")

        if settings_data:
            for setting in settings_data:
                setting_id = setting.pop("id")
                db.execute(update(Setting).where(Setting.id == setting_id).values(setting))

        new_data = {}
        for k, v in data.items():
            if v is not None:
                new_data[k] = v

        if new_data:
            db.execute(update(WaterSprinkler, return_defaults=True).where(WaterSprinkler.id == id).values(new_data))

        db.commit()

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@water_sprinkler_router.delete("/delete/{id}/", status_code=status.HTTP_200_OK)
async def water_sprinkler_delete(id: int, db: Session = Depends(get_db)):
    try:
        water_sprinkler = db.query(WaterSprinkler).filter(WaterSprinkler.id == id).first()

        water_sprinkler_settings_list = water_sprinkler.settings
        for water_sprinkler_setting in water_sprinkler_settings_list:
            setting_id = water_sprinkler_setting.id
            setting = db.query(Setting).filter(Setting.id == setting_id).first()
            db.delete(setting)

        db.delete(water_sprinkler)
        db.commit()

        return {"message": "Planta excluida com sucesso"}

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@water_sprinkler_router.delete("/settings-delete/{id}/", status_code=status.HTTP_200_OK)
async def water_sprinkler_settings_delete(id: int, db: Session = Depends(get_db)):
    try:
        setting = db.query(Setting).filter(Setting.id == id).first()
        db.delete(setting)

        db.commit()

        return {"message": "Configuração excluida com sucesso"}

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


from app.models import water_sprinkler # noqa
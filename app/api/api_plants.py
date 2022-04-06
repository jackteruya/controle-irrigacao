from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from app.api.schemas.schema_plants import PlantCreate, PlantPut, PlantPatch
from app.models.plants import Plants
from app.db.dependency import get_db


plants_router = APIRouter(
    prefix="/plants"
)


@plants_router.get("/get/", status_code=status.HTTP_200_OK)
async def plants_list(db: Session = Depends(get_db)):
    try:
        plants_ = db.query(Plants).all()

        response = jsonable_encoder(plants_)

        return JSONResponse(content=response)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@plants_router.get("/get/{id}/", status_code=status.HTTP_200_OK)
async def plants_retrieve(id: int, db: Session = Depends(get_db)):
    try:
        plant = db.query(Plants).filter(Plants.id == id).first()
        if plant is not None:
            response = jsonable_encoder(plant)

        return JSONResponse(content=response)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@plants_router.post("/create/", status_code=status.HTTP_201_CREATED)
async def plants_create(plant: PlantCreate, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(plant)

        new_plant = Plants(**data)
        db.add(new_plant)
        db.commit()

        return JSONResponse(content=data)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@plants_router.put("/update/")
async def plants_update(plant: PlantPut, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(plant)

        id = data.pop("id")

        db.execute(update(Plants).where(Plants.id == id).values(data))
        db.commit()

        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@plants_router.delete("/delete/{id}/", status_code=status.HTTP_200_OK)
async def plants_delete(id: int, db: Session = Depends(get_db)):
    try:
        plant = db.query(Plants).filter(Plants.id == id).first()
        db.delete(plant)
        db.commit()

        return {"message": "Planta excluida com sucesso"}

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@plants_router.patch("/update-data/", status_code=status.HTTP_204_NO_CONTENT)
async def plants_patch(plant: PlantPatch, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(plant)

        id = data.pop("id")

        new_data = {}
        for k, v in data.items():
            if v is not None:
                new_data[k] = v

        db.execute(update(Plants, return_defaults=True).where(Plants.id == id).values(new_data))
        db.commit()

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


from app.models import plants # noqa

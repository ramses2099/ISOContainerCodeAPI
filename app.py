from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from services import (
    get_iso_container_type_by_id,
    get_iso_container_type_by_code,
    create_iso_container_type as create_iso_container_type_service,
)
from models import Base 
from schemas import ISOContainerTypeBase, ISOContainerTypeCreate
from db import get_db, engine
from auth import get_current_user, router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)


@app.get("/isocontainertypesbygkey/{gkey}", response_model=ISOContainerTypeBase,
         dependencies=[Depends(get_current_user)])
def read_iso_container_type_by_id(gkey: int, db: Session = Depends(get_db)):
    db_iso_container_type = get_iso_container_type_by_id(db, gkey=gkey)
    if db_iso_container_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_iso_container_type

@app.get("/isocontainertypesbycode/{code}", response_model=ISOContainerTypeBase,
         dependencies=[Depends(get_current_user)])
def read_iso_container_type_by_code(code: str, db: Session = Depends(get_db)):
    db_iso_container_type = get_iso_container_type_by_code(db, code=code)
    if db_iso_container_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ISO container type not found")
    return db_iso_container_type


@app.post("/isocontainertypes", response_model=ISOContainerTypeBase,
          status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(get_current_user)])
def create_iso_container_type(isocontainertype: ISOContainerTypeCreate,
                             db: Session = Depends(get_db)):
    existing = get_iso_container_type_by_code(db, code=isocontainertype.code)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ISO container type code already exists")
    return create_iso_container_type_service(db, isocontainertype=isocontainertype)


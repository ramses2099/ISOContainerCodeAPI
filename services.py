from sqlalchemy.orm import Session

from models import ISOContainerType
from schemas import ISOContainerTypeCreate,ISOContainerTypeUpdate


def get_iso_container_type_by_id(db: Session, gkey: int):
    return db.query(ISOContainerType).filter(ISOContainerType.gkey == gkey).first()


def get_iso_container_type_by_code(db: Session, code: str):
    return db.query(ISOContainerType).filter(ISOContainerType.code == code).first()

def get_iso_container_type(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ISOContainerType).offset(skip).limit(limit).all()

def create_iso_container_type(db: Session, isocontainertype: ISOContainerTypeCreate):
    db_isocontainertype = ISOContainerType(code=isocontainertype.code,description=isocontainertype.description,
                                        length =isocontainertype.length,
                                          height = isocontainertype.height,
                                          group = isocontainertype.group                                      
                                      )
    db.add(db_isocontainertype)
    db.commit()
    db.refresh(db_isocontainertype)
    return db_isocontainertype

def update_iso_container_type(db: Session, isocontainertype: ISOContainerTypeUpdate):
    isoconttype = db.query(ISOContainerType).filter(ISOContainerType.gkey == isocontainertype.gkey).first()

    if isoconttype:
        isoconttype.code = isocontainertype.code
        isoconttype.description = isocontainertype.description
        isoconttype.length = isocontainertype.length
        isoconttype.height = isocontainertype.height
        isoconttype.group = isocontainertype.group

        db.commit()
        db.refresh(isoconttype)
    return isoconttype
        

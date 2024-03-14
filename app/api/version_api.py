from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from crud.version_crud import get_version, get_all_versions, store_version_difference, delete_versions, rollback_versions, update_versions
from schemas.version_schema import VersionSchema, VersionResponseSchema, VersionChangeSchema
from core.database import get_db

router = APIRouter()

@router.get("/{document_type}/{document_id}", response_model=List[VersionResponseSchema])
def read_versions(document_type, document_id, db: Session = Depends(get_db)):
    versions = get_all_versions(document_type, document_id, db)
    if versions == None:
        raise HTTPException(status_code=404, detail="Versions not found")
    return versions

@router.get("/{document_type}/{document_id}/{version}", response_model=VersionResponseSchema)
def read_version(document_type, document_id, version, db: Session = Depends(get_db)):
    version = get_version(document_type, document_id, version, db)
    if version == None:
        raise HTTPException(status_code=404, detail="Version not found")
    return version

@router.post("/new_version", status_code=status.HTTP_201_CREATED)
def create_new_version(new_version: VersionSchema, db: Session = Depends(get_db)):
    new_version = store_version_difference(new_version, db)
    if new_version == None:
        raise HTTPException(status_code=500, detail="Error creating new version")
    return new_version

@router.delete("/{document_type}/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_version(document_type, document_id, db: Session = Depends(get_db)):
    versions_to_delete = delete_versions(document_type, document_id, db)
    if versions_to_delete == None:
        raise HTTPException(status_code=404, detail="Versions not found")
    return versions_to_delete

@router.post("/rollback", status_code=status.HTTP_200_OK)
def rollback_version(version_to_change: VersionChangeSchema, db: Session = Depends(get_db)):
    version_to_change = rollback_versions(version_to_change, db)
    if version_to_change == None:
        raise HTTPException(status_code=404, detail="Error rolling back version")
    return version_to_change

@router.post("/update", status_code=status.HTTP_200_OK)
def update_version(version_to_change: VersionChangeSchema, db: Session = Depends(get_db)):
    version_to_change = update_versions(version_to_change, db)
    if version_to_change == None:
        raise HTTPException(status_code=404, detail="Error updating version")
    return version_to_change
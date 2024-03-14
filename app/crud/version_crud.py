from sqlalchemy.orm import Session
import models.version_model as version_model
import schemas.version_schema as version_schema
from core.utils import get_diff, rollback_to_version, update_to_version
from datetime import datetime


def get_all_versions(document_type, document_id, db: Session):
    return db.query(version_model.Versions).filter_by(document_type=document_type, document_id=document_id).all()

def get_version(document_type, document_id, version, db: Session):
    return db.query(version_model.Versions).filter_by(document_type=document_type, document_id=document_id, version=version).first()

def store_version_difference(new_version: version_schema.VersionSchema, db: Session):
    diff = get_diff(new_version.old_json, new_version.new_json)
    if "error" in diff:
        return None
    if len(diff) == 0:
        return None
    try:
        latest_version = db.query(version_model.Versions).filter_by(document_type=new_version.document_type, document_id=new_version.document_id).order_by(version_model.Versions.version.desc()).first()
        if latest_version:
            new_version_number = latest_version.version + 1
        else:
            new_version_number = 1
        new_version_result = version_model.Versions(document_type=new_version.document_type, document_id=new_version.document_id, version=new_version_number, json_data_changes=str(diff), created_at=datetime.now(), created_by=new_version.created_by)
        db.add(new_version_result)
        db.commit()
        db.refresh(new_version_result)
        return 201
    except Exception as e:
        db.rollback()
        print(f"An error occurred while storing the version difference: {e}")
        return None
    
def delete_versions(document_type, document_id, db: Session):
    versions = db.query(version_model.Versions).filter_by(document_type=document_type, document_id=document_id).all()
    if len(versions) == 0:
        return None
    try:
        for version in versions:
            db.delete(version)
        db.commit()
        return 204
    except Exception as e:
        db.rollback()
        print(f"An error occurred while deleting the versions: {e}")
        return None
    
def rollback_versions(version_to_change: version_schema.VersionChangeSchema, db: Session):
    changes = db.query(version_model.Versions).filter_by(document_type=version_to_change.document_type, document_id=version_to_change.document_id).all()
    changes_dicts = [version.to_dict() for version in changes]
    if len(changes_dicts) == 0:
        return None
    try:
        new_json = rollback_to_version(version_to_change.current_json, changes_dicts, int(version_to_change.current_version), int(version_to_change.target_version))
        return new_json
    except Exception as e:
        print(f"An error occurred while rolling back the version: {e}")
        return None
    
def update_versions(version_to_change: version_schema.VersionChangeSchema, db: Session):
    changes = db.query(version_model.Versions).filter_by(document_type=version_to_change.document_type, document_id=version_to_change.document_id).all()
    changes_dicts = [version.to_dict() for version in changes]
    if len(changes_dicts) == 0:
        return None
    try:
        new_json = update_to_version(version_to_change.current_json, changes_dicts, int(version_to_change.current_version), int(version_to_change.target_version))
        return new_json
    except Exception as e:
        print(f"An error occurred while updating to the version: {e}")
        return None
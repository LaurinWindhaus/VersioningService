from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Versions(Base):
    __tablename__ = 'T003_Versioning'
    __table_args__ = {'schema': 'dsd'} 

    id = Column(Integer, primary_key=True, nullable=False)
    document_type = Column(String, nullable=False)
    document_id = Column(String, nullable=False)
    version = Column(String, nullable=False)
    json_data_changes = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(String, nullable=False)

    def __repr__(self):
        return '{"id":%d, "document_type":"%s", "document_id":"%s", "version":"%s", "json_data_changes":"%s", "created_at":"%s", "created_by:":"%s"}' % (self.id, self.document_type, self.document_id, self.version, self.json_data_changes, self.created_at, self.created_by)
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_type': self.document_type,
            'document_id': self.document_id,
            'version': self.version,
            'json_data_changes': self.json_data_changes,
            'created_at': self.created_at,
            'created_by': self.created_by
        }
from sqlalchemy import Column, Integer, String, Boolean, column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base



class Posts(Base):
    __tablename__ = "posts"

    iid = Column(Integer, primary_key = True, nullable=False)
    title = Column(String, nullable = False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

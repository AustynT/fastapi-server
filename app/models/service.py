from sqlalchemy import Column, Integer, String, Float

from app.models.base_model import BaseModel

class Service(BaseModel):
   __tablename__ = "services" 

   serive_id = Column(Integer, primary_key = True, index = True)
   service_name = Column(String, unique = True, nullable = False)
   total_amount = Column(Float, nullable = False)


   
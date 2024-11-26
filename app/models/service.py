from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Service(BaseModel):
   __tablename__ = "services" 

   serive_id = Column(Integer, primary_key = True, index = True)
   user_id = Column(Integer, ForeignKey("users.id", nullable= False, index= True))
   service_name = Column(String, unique = True, nullable = False)
   total_amount = Column(Float, nullable = False)

   user = relationship("Users", back_populates="services")
   
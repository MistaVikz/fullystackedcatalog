from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
   
    category_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.category_id,
       }
 
class CatalogItem(Base):
    __tablename__ = 'catalog_items'

    item_id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(250))
    price = Column(String(10))
    category_id = Column(Integer,ForeignKey('category.category_id'))
    category = relationship(Category)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'  : self.description,
           'price'        : self.price,
           'id'           : self.item_id,
       }



engine = create_engine('sqlite:///CATalog.db')
 

Base.metadata.create_all(engine)

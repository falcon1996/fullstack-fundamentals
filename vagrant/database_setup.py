############################################################################
import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base    # to use in config and class code
from sqlalchemy.orm import relationship #to create foreign key
from sqlalchemy import create_engine #to use in config code in end

Base = declarative_base() #to let sqlalchemy know our classes are special sqlalchemy classes that correspond to tables in database
############################################################################################


###################################################################################
class Restaurant(Base):
	__tablename__ = 'restaurant'

	name = Column(String(80), nullable = False)# nullable means three must be a value
	ids = Column(Integer, primary_key = True)

class MenuItem(Base):
	__tablename__ = 'menu_item'

	name = Column(String(80), nullable = False)
	ids = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.ids'))#retrieve id number from restaurant table
	restaurant = relationship(Restaurant)
###########################################################################################

##########################################################################################
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)# goes to database and add classes as tables in our databases.
##################################################################################

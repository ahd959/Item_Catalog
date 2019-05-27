from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Car, MenuItem, User

engine = create_engine('sqlite:///carmenuuser.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Items for user
user1 = User(name='Ahmed ALHAWSAWI', email='ahd959@gmail.com',
picture='https://lh3.googleusercontent.com/-y7mp_LYnSkQ/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rdwPT3d49ubku6oKxN7Pb_rOKDVsg/s128-c-mo/photo.jpg')  # noqa

session.add(user1)
session.commit()

# Items for car companies
car1 = Car(name='TOYOTA', user_id=1)

session.add(car1)
session.commit()

# Items for Toyota
item1 = MenuItem(name='CAMRY', price='$10.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car1, user_id=1)  # noqa

session.add(item1)
session.commit()

item2 = MenuItem(name='HILUX', price='$20.000', item_type='COMMERCIAL', description='A commercial vehicle is any type of motor vehicle used for transporting goods or paying passengers', car=car1, user_id=1)  # noqa

session.add(item2)
session.commit()

item3 = MenuItem(name='INNOVA', price='$30.000', item_type='SUVS', description='A van is a type of road vehicle used for transporting goods or people.', car=car1, user_id=1)  # noqa

session.add(item3)
session.commit()

item4 = MenuItem(name='LAND CRUISER', price='$50.000', item_type='SUVS', description='A powerful vehicle with four-wheel drive that can be driven over rough ground.', car=car1, user_id=1)  # noqa
session.add(item4)
session.commit()

item5 = MenuItem(name='86 GT', price='$70.000', item_type='SPORT', description='A low-built car designed for performance at high speeds', car=car1, user_id=1)  # noqa

session.add(item5)
session.commit()

# Items for car companies
car2 = Car(name='NISSAN', user_id=1)

session.add(car2)
session.commit()

# menu for Nissan
item1 = MenuItem(name='ALTIMA', price='$30.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car2, user_id=1)  # noqa

session.add(item1)
session.commit()

item2 = MenuItem(name='MAXIMA', price='$50.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car2, user=user1)  # noqa

session.add(item2)
session.commit()

item3 = MenuItem(name='TITAN', price='$70.000', item_type='COMMERCIAL', description='A commercial vehicle is any type of motor vehicle used for transporting goods or paying passengers', car=car2, user=user1)  # noqa

session.add(item3)
session.commit()

item4 = MenuItem(name='MARANO', price='$80.000', item_type='SUVS', description='A powerful vehicle with four-wheel drive that can be driven over rough ground.', car=car2, user=user1)  # noqa

session.add(item4)
session.commit()

item5 = MenuItem(name='GT-R', price='$100.000', item_type='SPORT', description='A low-built car designed for performance at high speeds', car=car2, user=user1)  # noqa

session.add(item5)
session.commit()

# Items for car companies
car3 = Car(name='HONDA', user=user1)

session.add(car3)
session.commit()

# menu for Honda
item1 = MenuItem(name='ACCORD', price='30.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car3, user=user1)  # noqa

session.add(item1)
session.commit()

item2 = MenuItem(name='CIVIC', price='$50.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car3, user=user1)  # noqa

session.add(item2)
session.commit()

item3 = MenuItem(name='PILOT', price='$70.000', item_type='SUVS', description='A powerful vehicle with four-wheel drive that can be driven over rough ground.', car=car3, user=user1)  # noqa

session.add(item3)
session.commit()

item4 = MenuItem(name='ODYSSEY', price='$80.000', item_type='SUVS', description='A van is a type of road vehicle used for transporting goods or people.', car=car3, user=user1)  # noqa

session.add(item4)
session.commit()

item5 = MenuItem(name='NSX', price='$90.000', item_type='SPORT', description='A low-built car designed for performance at high speeds', car=car3, user=user1)  # noqa

session.add(item5)
session.commit()

# Items for car companies
car4 = Car(name='HUNDAI', user=user1)

session.add(car4)
session.commit()

# menu for Hundai
item1 = MenuItem(name='ACCENT', price='$20.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car4, user=user1)  # noqa

session.add(item1)
session.commit()

item2 = MenuItem(name='ELANTRA', price='30.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car4, user=user1)  # noqa

session.add(item2)
session.commit()

item3 = MenuItem(name='SANT FE', price='$50.000', item_type='SUVS', description='A powerful vehicle with four-wheel drive that can be driven over rough ground.', car=car4, user=user1)  # noqa

session.add(item3)
session.commit()

item4 = MenuItem(name='H-1', price='$70.000', item_type='COMMERCIAL', description='A commercial vehicle is any type of motor vehicle used for transporting goods or paying passengers', car=car4, user=user1)  # noqa

session.add(item4)
session.commit()

item5 = MenuItem(name='i30 N', price='$90.000', item_type='SPORT', description='A low-built car designed for performance at high speeds', car=car4, user=user1)  # noqa

session.add(item5)
session.commit()

# Items for car companies
car5 = Car(name='CHEVROLET', user=user1)

session.add(car5)
session.commit()

# menu for Chevrolet
item1 = MenuItem(name='MALIBU', price='30.000', item_type='PASSENGER', description='A passenger car is a road motor vehicle', car=car5, user=user1)  # noqa

session.add(item1)
session.commit()

item2 = MenuItem(name='TRAX', price='$50.000', item_type='SUVS', description='A powerful vehicle with four-wheel drive that can be driven over rough ground.', car=car5, user=user1)  # noqa

session.add(item2)
session.commit()

item3 = MenuItem(name='EXPRESS', price='$70.000', item_type='COMMERCIAL', description='A commercial vehicle is any type of motor vehicle used for transporting goods or paying passengers', car=car5, user=user1)  # noqa

session.add(item3)
session.commit()

item4 = MenuItem(name='CORVETTE GRAND SPORT', price='$80.000', item_type='SPORT', description='A low-built car designed for performance at high speeds', car=car5, user=user1)  # noqa

session.add(item4)
session.commit()

item5 = MenuItem(name='CAMARO', price='$90.000', item_type='SPORT', description='An electric car is an automobile that is propelled by one or more electric motors, using energy stored in rechargeable batteries', car=car5, user=user1)  # noqa

session.add(item5)
session.commit()


print ('items have been added successfully')

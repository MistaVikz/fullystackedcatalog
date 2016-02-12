from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CatalogItem, User

engine = create_engine('sqlite:///CATalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#Create fake user
User1 = User(name="Emma the Cat", email = "meow@meowmix.ca")
session.add(User1)
session.commit()

# Wet Food
category1 = Category(name="Wet Food")

session.add(category1)
session.commit()

catalogItem1 = CatalogItem(user_id=1, name="Almo Nature", description="Seafood chunks with no added preservatives", 
					price = "$1.25", category=category1)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(user_id=1, name="Science Diet", description="Chick beaks with ash and lots of science.", 
					price= "$1.05", category=category1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Lamburgini", description="Juicy lamb with lots of puns.", 
					price="$1.50", category=category1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Discount Cat Chum", description="You don't want to know.", 
					price="$0.25", category=category1)

session.add(catalogItem4)
session.commit()


# Dry Food
category2 = Category(name="Dry Food")

session.add(category2)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Almo Nature Kibble", description="Dry chicken kibble.", 
					price="$20.99", category=category2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Science Diet", description="Sodium Hypothalimide in a crunchy pellet form", 
					price="$15.00", category=category2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Discount Cat Kibble", description="Don't ask.", 
					price="$5.00", category=category2)

session.add(catalogItem3)
session.commit()


# Toys
category3 = Category(name="Cat Toys")

session.add(category3)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Mr. Mouse", description="A fluffy mouse with catnip inside.", 
					price="$0.50", category=category3)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Super Elaborate Cat Entertainment System", description="A complicated, expensive ball track that will take hours to assemble. Your cat will break it within 30 seconds.", 
					price="$85.99", category=category3)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Screeching Bird", description="A plush bird that makes an irritating noise every time your cat plays with it.", 
					price="$9.95", category=category3)

session.add(catalogItem3)
session.commit()


# Scratching Posts
category4 = Category(name="Scratching Posts")

session.add(category4)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Scratching Pylon", description="A 2 foot high python that your cat will scratch", 
					price="$23.95", category=category4)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Meowing Mansion", description="A three story cat enclosure with 2 bedrooms and 1.5 baths.", 
					price="$654.95", category=category4)

session.add(catalogItem2)
session.commit()


# Litter Boxes
category5 = Category(name="Litter Boxes")

session.add(category5)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Plastic One-Cat Box", description="A box that you put litter in.", 
					price="$9.95", category=category5)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Multi-Cat Litter Tub", description="You have too many cats.", 
					price="$27.95", category=category5)

session.add(catalogItem2)
session.commit()


# Kitty Litter
category6 = Category(name="Kitty Litter")

session.add(category6)
session.commit()

catalogItem1 = CatalogItem(user_id=1, name="Clumping Natural Litter", description="Put it in your litter box.", 
					price="$25.99", category=category6)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(user_id=1, name="Mountain Meadow Scented Litter.", description="Will remind you of the Swiss Alps.", 
					price="$42.99", category=category6)

session.add(catalogItem2)
session.commit()

print "added cat related items!"

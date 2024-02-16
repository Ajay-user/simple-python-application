'''SQLlite Model '''
from flask_login import UserMixin

from market import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    '''reload the user object from the user ID stored in the session.'''
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Database table for USERS""" 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship("Item", backref='owned_user', lazy=True)

    # @property
    # def password(self):
    #     '''password getter'''
    #     return self.password

    # @password.setter
    # def password(self, password_):
    #     '''password setter'''
    #     print('>>>>>>>>>>>>>>>>>>>>>>>>>',password_)
    #     self.password = (
    #         bcrypt
    #         .generate_password_hash(password=password_)
    #         .decode('UTF-8')
    #     )

    def __repr__(self) -> str:
        return f"USER [ {self.username} ]"


class Item(db.Model):
    """Database table for ITEMS"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    barcode = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"ITEM < {self.name} | ${self.price} >"


# set up database, table .. 

with app.app_context():
    # # drop the database tables
    db.drop_all()
    # # create database and table
    db.create_all()

    # # Add an item into the ITEM table
    # item= Item(name='Phone', barcode='893212299897', price=500, description='Coolest phone ever')
    # db.session.add(item)
    # db.session.commit()

    # # Add some items into the ITEM table
    item_1 = Item(name='Phone', barcode='893212299897', price=500, description='Coolest phone ever')
    item_2 = Item(name='Laptop', barcode='993212299897', price=1500, description='Coolest Laptop ever')
    item_3 = Item(name='Apple Laptop', barcode='993212299999', price=2500, description='Coolest Apple Laptop ever')
    item_4 = Item(name='Gameboy', barcode='993212299897', price=150, description='Coolest Gameboy ever')
    db.session.add_all([item_1, item_2, item_3, item_4])
    db.session.commit()

    # # Add an user into the USER table
    user_1 = User(username='ajay', password='123456', email='ajay@gmail.com')
    db.session.add(user_1)
    db.session.commit()



    # # print all the items in the table ITEM
    # print(Item.query.all())

    # # Filter the query results 
    for item in Item.query.filter_by(price=500):
        print(">> ", item)
    
    for user in User.query.all():
        print("--> ", user)


    # # db.session.rollback --> rollback previous changes and commits 
        

    # # Assign product to a user
    item_1 = Item.query.filter_by(price=500).first()
    # # user you want -- get the id
    user_1_id = User.query.filter_by(username='ajay').first().id
    # # update product info
    item_1.owner = user_1_id
    db.session.add(item_1)
    db.session.commit()

    print("USER ID", user_1_id)
    # # Filter the query results 
    for item in Item.query.filter_by(owner=user_1_id):
        print(">> ", item, " << ", item.owner)
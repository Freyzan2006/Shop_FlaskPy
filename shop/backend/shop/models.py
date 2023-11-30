from flask_login import UserMixin



from shop import db, manager

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    isActive = db.Column(db.Boolean, default = True)
    image = db.Column(db.String, nullable = True)
    price_type = db.Column(db.String(3), nullable = False)

    def __repr__(self):
        return self.title


class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    isAdmin = db.Column(db.Boolean, default = False)


@manager.user_loader
def login_user(user_id):
    return User.query.get(user_id)











from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash


login = LoginManager()
db = SQLAlchemy()


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


class PageModel(UserMixin, db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


class NavbarItemModel(UserMixin, db.Model):
    __tablename__ = 'navbar_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    custom_url = db.Column(db.String(100))
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    page = db.relationship("PageModel", backref=backref("pages", uselist=False))
    custom_url_enabled = db.Column(db.Boolean, default=False)
    position_index = db.Column(db.Integer)
    parent_item_id = db.Column(db.Integer, db.ForeignKey('navbar_items.id'))


class SettingsModel(UserMixin, db.Model):
    __tablename__ = 'settings'

    key = db.Column(db.String, primary_key=True)
    value = db.Column(db.String)

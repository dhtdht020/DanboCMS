from flask import Flask, redirect, url_for
from models import db, login, PageModel, SettingsModel
import config

from setup.routes import setup
from admin.routes import admin
from website.routes import website

app = Flask(__name__)

# Register blueprints
app.register_blueprint(setup)
app.register_blueprint(admin)
app.register_blueprint(website)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = config.secret_key
db.init_app(app)
login.init_app(app)
login.login_view = 'admin.login'


@app.before_first_request
def create_table():
    db.create_all()

    # add an home page entry to pages table
    if PageModel.query.filter_by(name='Home Page').first() is None:
        page = PageModel(name='Home Page', url='',
                         content='<h1 class="title">Welcome to the website!</h1>'
                                 '<p>This is the home page.</p>'
                                 '<a href="/admin/pages">Manage pages</a>')
        db.session.add(page)
        db.session.commit()

    # add default settings if they don't exist
    if SettingsModel.query.filter_by(key='website_name').first() is None:
        settings = SettingsModel(key='website_name', value='My Website')
        db.session.add(settings)
        db.session.commit()
    if SettingsModel.query.filter_by(key='home_page').first() is None:
        settings = SettingsModel(key='home_page', value='1')
        db.session.add(settings)
        db.session.commit()
    if SettingsModel.query.filter_by(key='blog_page').first() is None:
        settings = SettingsModel(key='blog_page', value='1')
        db.session.add(settings)
        db.session.commit()
    if SettingsModel.query.filter_by(key='display_navigation_bar').first() is None:
        settings = SettingsModel(key='display_navigation_bar', value='true')
        db.session.add(settings)
        db.session.commit()


if __name__ == '__main__':
    app.run()

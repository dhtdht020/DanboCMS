from flask import Blueprint, render_template, abort

from models import PageModel, NavbarItemModel, SettingsModel
import helpers

website = Blueprint('website', __name__, template_folder='templates')


@website.route('/<url>')
@website.route('/<url>/')
def page(url):
    page = PageModel.query.filter_by(url=url).first()
    if page is None:
        abort(404)
    navbar_items = NavbarItemModel.query.order_by(NavbarItemModel.position_index.asc())
    return render_template('website/base.html', content=page.content, navbar_items=navbar_items,
                           settings=helpers.get_settings())


@website.route('/')
def home():
    return page('')

from models import SettingsModel, db


def get_settings():
    settings = {}
    for setting in SettingsModel.query.all():
        settings[setting.key] = setting.value
    return settings


def update_setting(key: str, value: str):
    # create if doesn't exist
    if SettingsModel.query.filter_by(key=key).first() is None:
        settings = SettingsModel(key=key, value=value)
        db.session.add(settings)
    else:
        settings = SettingsModel.query.filter_by(key=key).first()
        settings.value = value
    db.session.commit()

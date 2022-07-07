from models import SettingsModel


def get_settings():
    settings = {}
    for setting in SettingsModel.query.all():
        settings[setting.key] = setting.value
    return settings

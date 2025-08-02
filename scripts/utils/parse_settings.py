from configparser import ConfigParser


def config_to_settings(path):
    """Load an INI style configuration into a flat dictionary."""

    parser = ConfigParser()
    parser.read(path)

    settings = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            settings[f"{section}.{key}"] = value
    return settings

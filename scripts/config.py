from configparser import ConfigParser, NoOptionError, NoSectionError

_PATH = "./config.ini"


def getstr(parser: ConfigParser, section: str, key: str) -> str | None:
    try:
        return parser.get(section, key)
    except (NoSectionError, NoOptionError):
        return None


def getint(parser: ConfigParser, section: str, key: str) -> int | None:
    """Get an integer from the configuration file

    Args:
        parser (ConfigParser): The configparser object to query
        section (str): The section to look in
        key (str): The key to look for

    Returns:
        int | None: An int, or None as default
    """
    try:
        return parser.getint(section, key)
    except (NoSectionError, NoOptionError):
        return None


def getparser() -> ConfigParser:
    parser = ConfigParser()
    parser.read(_PATH)
    return parser

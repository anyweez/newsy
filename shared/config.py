import configparser

"""
Load the configuration file from the specified location on disk. Uses Python3's ConfigParser.

https://docs.python.org/3/library/configparser.html
"""
def load(path):
    config = configparser.ConfigParser()
    config.read(path)

    return config
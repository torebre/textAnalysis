import configparser

def getPaths():
    config = configparser.RawConfigParser()
    config.read('../app.properties')
    paths_dict = dict(config.items('PATHS'))
    return paths_dict

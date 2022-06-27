
import os
import sys
from configparser import ConfigParser

sys.path.append(os.path.abspath(os.path.curdir))

# Read the config file
config_file      = 'database.conf' # TODO: Read it from yaml
basedir          = os.path.abspath(os.path.dirname(__file__))
config_file_path = os.path.join(basedir, config_file)

config = ConfigParser()
if os.path.exists(config_file):
    config.read(config_file)
else:
    message = f'No `{config_file}` in the location {basedir}'
    raise Exception(message)

def get_config_value(key: str) -> any:
    """
    Function to get the environment variable

    Inputs: 
        :key: Entity key from the `conf` file
        :type key: str
    Outputs:
        :: Value for the config key  
    """
    try:
        return config['postgres-conf'][key]
    except KeyError:
        message = f'Expected config variable `{key}` not set.'
        raise Exception(message)

# Set the variables
POSTGRES_HOST = get_config_value("POSTGRES_HOST")
POSTGRES_PORT = get_config_value("POSTGRES_PORT")
POSTGRES_USER = get_config_value("POSTGRES_USER")
POSTGRES_PWD  = get_config_value("POSTGRES_PWD")
POSTGRES_DB   = get_config_value("POSTGRES_DB")

# Set DB URL
DB_URL = 'postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}'.format(
    user=POSTGRES_USER, pwd=POSTGRES_PWD, host=POSTGRES_HOST, port=POSTGRES_PORT, db=POSTGRES_DB
)

class Config(object):
    """"
    Creates the config object for the Database by reading the configuration `database.conf`
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_DATABASE_URI = DB_URL or \
            'psql:///' + os.path.join(basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

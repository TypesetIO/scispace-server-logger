"""
    Constants related to scispace logger service
"""

import os

TRUE_VALUES = ['1', 'true']

def return_bool(string):
    """
        Util Function to return env variable bool
    """
    if string and string.lower() in TRUE_VALUES:
        return True
    return False

# LOG LEVEL RELATED CONSTANTS
ERROR = 'ERROR'
INFO = 'INFO'
WARNING = 'WARNING'
DEBUG = 'DEBUG'

# TRACE LEVELS
RETURN = 'return'
EXCEPTION = 'exception'
CALL = 'call'

# KINESIS RELATED CONSTANTS
DELIVERY_STREAM_NAME = os.getenv(
    'SCISPACE_LOGGER_DELIVERY_STREAM_NAME', 'scispace-server-logs')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-west-2')

# Client Related CONSTANTS
ENV = os.getenv('SCISPACE_LOGGER_ENV')
APP_NAME = os.getenv('SCISPACE_LOGGER_APP_NAME')
ENABLE_SCISPACE_LOGGER = return_bool(os.getenv('ENABLE_SCISPACE_LOGGER'))
ENABLE_SCISPACE_EVENT_HANDLERS = return_bool(os.getenv('ENABLE_SCISPACE_EVENT_HANDLERS'))

# EVENT ANALYTICS CONSTANTS
DEFAULT_LOGGER = os.getenv('DEFAULT_LOGGER', 'apps.log')
VENV_LOCATION = os.getenv('VENV_LOCATION', 'env3')
DEFAULT_IGNORED_FILES = [VENV_LOCATION] if VENV_LOCATION else []
DEFAULT_IGNORED_CLASSES = ['AxiomHandler', 'HostnameFilter']
IGNORED_FILES = os.getenv('IGNORED_FILES')
IGNORED_FILES = IGNORED_FILES.split(',') if IGNORED_FILES else []
IGNORED_FILES += DEFAULT_IGNORED_FILES
IGNORED_FILES = [file.strip() for file in IGNORED_FILES]
IGNORED_CLASSES = os.getenv('IGNORED_CLASSES')
IGNORED_CLASSES = IGNORED_CLASSES.split(',') if IGNORED_CLASSES else []
IGNORED_CLASSES += DEFAULT_IGNORED_CLASSES
IGNORED_CLASSES = [cls.strip() for cls in IGNORED_CLASSES]
IGNORED_FUNCTIONS = ['__str__', '__repr__']

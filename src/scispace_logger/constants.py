"""
    Constants related to scispace logger service
"""

import os

# LOG LEVEL RELATED CONSTANTS
ERROR = 'ERROR'
INFO = 'INFO'
WARNING = 'WARNING'
DEBUG = 'DEBUG'

# KINESIS RELATED CONSTANTS
DELIVERY_STREAM_NAME = os.getenv(
    'SCISPACE_LOGGER_DELIVERY_STREAM_NAME', 'scispace-server-logs')

# Client Related CONSTANTS
ENV = os.getenv('SCISPACE_LOGGER_ENV')
APP_NAME = os.getenv('SCISPACE_LOGGER_APP_NAME')
ENABLE_SCISPACE_LOGGER = os.getenv('ENABLE_SCISPACE_LOGGER')

"""
    Constants related to scispace logger service
"""

import os

# LOG LEVEL RELATED CONSTANTS
ERROR = 'ERROR'
INFO = 'INFO'
WARNING = 'WARNING'
DEBUG = 'DEBUG'

# Service Related CONSTANTS
DEFAULT_APP_NAME = 'scispace'

# KINESIS RELATED CONSTANTS
DELIVERY_STREAM_NAME = os.getenv('DELIVERY_STREAM_NAME')

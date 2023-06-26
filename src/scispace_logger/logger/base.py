"""
    Base Classes for the server logger
"""

from ..s3_client.kinesis_firehose_cli import KinesisFirehoseClient
from ..constants import ERROR, INFO, WARNING, DEBUG, \
    DELIVERY_STREAM_NAME, ENV, APP_NAME, ENABLE_SCISPACE_LOGGER


class BaseServerLogger(object):
    """
        Base Class for construction of logs and pushing to log service
    """

    def __init__(self, **kwargs) -> None:
        self.delivery_stream_name = kwargs.get(
            'delivery_stream_name', DELIVERY_STREAM_NAME)
        self.service_name = kwargs.get('service_name')
        if ENABLE_SCISPACE_LOGGER and self.delivery_stream_name:
            self.logger_cli = KinesisFirehoseClient()
        else:
            print('Scispace Logger is not enabled.')
            self.logger_cli = None

    def _log(self, **kwargs):
        log_info = kwargs.get('log_info', {})
        logger_kwargs = dict(
            delivery_stream_name=self.delivery_stream_name,
            data=log_info
        )
        if self.logger_cli:
            self.logger_cli.push_record(**logger_kwargs)

    def _get_log_info(self, message, **kwargs):
        exc_info = kwargs.get('exc_info')
        extra = kwargs.get('extra')
        service_name = kwargs.get('service_name', self.service_name)
        user_id = kwargs.get('user_id')
        log_info = dict(
            user_id=user_id,
            message=message,
            traceback=exc_info,
            env=ENV,
            app_name=APP_NAME,
            service_name=service_name,
            **extra
        )
        return log_info

    def error(self, message, **kwargs):
        """
            To log messages with the level ERROR
        """
        log_info = dict(
            level=ERROR,
            **self._get_log_info(message, **kwargs)
        )
        self._log(log_info=log_info)

    def info(self, message, **kwargs):
        """
            To log messages with the level INFO
        """
        log_info = dict(
            level=INFO,
            **self._get_log_info(message, **kwargs)
        )
        self._log(log_info=log_info)

    def warn(self, message, **kwargs):
        """
            To log messages with the level WARNING
        """
        log_info = dict(
            level=WARNING,
            **self._get_log_info(message, **kwargs)
        )
        self._log(log_info=log_info)

    def debug(self, message, **kwargs):
        """
            To log messages with the level DEBUG
        """
        log_info = dict(
            level=DEBUG,
            **self._get_log_info(message, **kwargs)
        )
        self._log(log_info=log_info)

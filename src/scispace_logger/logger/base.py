"""
    Base Classes for the server logger
"""

from ..s3_client.kinesis_firehose_cli import KinesisFirehoseClient
from ..constants import ERROR, INFO, WARNING, DEBUG, \
    DELIVERY_STREAM_NAME


class BaseServerLogger(object):
    """
        Base Class for construction of logs and pushing to log service

        __init__ requires service_name as one of the arguments
    """

    def __init__(self, service_name, **kwargs) -> None:
        delivery_stream_name = kwargs.get(
            'delivery_stream_name', DELIVERY_STREAM_NAME)
        self.logger_cli = KinesisFirehoseClient()
        self.app_name = None
        self.service = service_name
        self.delivery_stream_name = delivery_stream_name

    def _log(self, **kwargs):
        log_info = kwargs.get('log_info', {})
        logger_kwargs = dict(
            delivery_stream_name=self.delivery_stream_name,
            data=log_info
        )
        self.logger_cli.push_record(**logger_kwargs)

    def _get_log_info(self, message, **kwargs):
        exc_info = kwargs.get('exc_info')
        extra = kwargs.get('extra')
        user_id = kwargs.get('user_id')
        env = kwargs.get('env')
        log_info = dict(
            user_id=user_id,
            message=message,
            app=self.app_name,
            service=self.service,
            traceback=exc_info,
            info=extra,
            env=env
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

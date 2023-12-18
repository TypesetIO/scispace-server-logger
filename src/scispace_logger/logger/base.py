"""
    Base Classes for the server logger
"""
from copy import deepcopy

from ..s3_client.kinesis_firehose_cli import KinesisFirehoseClient
from ..constants import ERROR, INFO, WARNING, DEBUG, \
    DELIVERY_STREAM_NAME, ENV, APP_NAME, ENABLE_SCISPACE_LOGGER, \
    ENABLE_SCISPACE_EVENT_HANDLERS


class BaseServerLogger(object):
    """
        Base Class for construction of logs and pushing to log service
    """

    def __init__(self, **kwargs) -> None:
        self.delivery_stream_name = kwargs.get(
            'delivery_stream_name', DELIVERY_STREAM_NAME)
        self.service_name = kwargs.get('service_name')
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.region_name = None

    def _get_logger_cli(self, **kwargs):
        if (ENABLE_SCISPACE_LOGGER or ENABLE_SCISPACE_EVENT_HANDLERS) and self.delivery_stream_name:
            kwargs_for_firehose = dict()
            if self.aws_access_key_id:
                kwargs_for_firehose['aws_access_key_id'] = self.aws_access_key_id
            if self.aws_secret_access_key:
                kwargs_for_firehose['aws_secret_access_key'] = self.aws_secret_access_key
            if self.region_name:
                kwargs_for_firehose['region_name'] = self.region_name
            return KinesisFirehoseClient(**kwargs_for_firehose)
        else:
            return None

    def _override_keys(self, data, prefix=''):
        result = dict()
        if not data:
            return result
        for key, value in data.items():
            result[prefix + key] = value
        return result

    def _log(self, **kwargs):
        log_info = kwargs.get('log_info', {})
        logger_kwargs = dict(
            delivery_stream_name=self.delivery_stream_name,
            data=log_info
        )
        logger_cli = self._get_logger_cli()
        if logger_cli:
            logger_cli.push_record(**logger_kwargs)

    def _get_log_info(self, message, **kwargs):
        kwargs_for_logs = deepcopy(kwargs)
        extra = kwargs_for_logs.pop('extra', {})
        log_info = dict(
            message=message,
            env=ENV,
            app_name=APP_NAME,
            **kwargs_for_logs,
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

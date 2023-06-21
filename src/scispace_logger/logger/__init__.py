"""
    Logger Service related class for scispace app
"""
from .base import BaseServerLogger


class ScispaceLogger(BaseServerLogger):
    """
        Logger Service to be used while logging for all scispace related apps
    """

    def __init__(self, service_name, **kwargs) -> None:
        super().__init__(service_name, **kwargs)
        self.app_name = 'scispace'


class NLPLogger(BaseServerLogger):
    """
        Logger Service to be used while logging for all NLP related apps
    """

    def __init__(self, service_name, **kwargs) -> None:
        super().__init__(service_name, **kwargs)
        self.app_name = 'nlp'

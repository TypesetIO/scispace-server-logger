
from copy import deepcopy
import logging

from ..events.trace_events import TraceEvents
from ..logger.base import BaseServerLogger
from ..constants import DEFAULT_LOGGER

logger = logging.getLogger(DEFAULT_LOGGER)
scispace_logger = BaseServerLogger()

def handle_event_analytics(analytics_service):
    """
    Decorator to handle analytics on specific features / functionalities
    """
    def trace_func(func):
        def wrapper(self, *args, **kwargs):
            if not analytics_service:
                return func(self, *args, **kwargs)

            # Main Class handling the tracing of all args, kwargs
            # to be consumed by logger service
            trace_events = TraceEvents()
            with trace_events:
                # function call
                return_value = func(self, *args, **kwargs)

                # logging events to kibana for analytics
                try:
                    # Get the necessary data for logging from logger service
                    kwargs_for_event_analytics_service = dict()
                    kwargs_for_event_analytics_service['events_data'] = trace_events.get_event_data()
                    log_data = analytics_service.get(**kwargs_for_event_analytics_service)

                    # Log the events and other info to kibana
                    log_info = deepcopy(log_data)
                    message = log_info.pop('message', 'Event captured for analytics')
                    scispace_logger.info(message, **log_info)
                except Exception as exc:
                    logger.error(str(exc))
            return return_value
        return wrapper
    return trace_func

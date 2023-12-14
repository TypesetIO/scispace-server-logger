
import sys
import logging
import traceback
from ..constants import IGNORED_FILES, IGNORED_CLASSES, IGNORED_FUNCTIONS, DEFAULT_LOGGER, \
    RETURN, EXCEPTION, ENABLE_SCISPACE_EVENT_HANDLERS

logger = logging.getLogger(DEFAULT_LOGGER)

class TraceEvents(object):
    """
        Generic class to handle the python function tracing
    """
    def __init__(self) -> None:
        self.__events_data = dict()
    
    def validate_trace(self, frame, event, arg):
        """
            Validate whether to trace the event or not
            To trace only events which are not related to packages
        """
        f_code = frame.f_code
        file_name = f_code.co_filename
        func_name = f_code.co_name

        if not file_name.startswith('/usr/share'):
            return False

        if func_name in IGNORED_FUNCTIONS:
            return False

        for ignored_file in IGNORED_FILES:
            if ignored_file in file_name:
                return False
        return True
   
    def __enter__(self):
        if ENABLE_SCISPACE_EVENT_HANDLERS:
            sys.settrace(self.trace_lines)

    def __exit__(self, *args, **kwargs):
        # Stop tracing all events
        sys.settrace(None)

    def trace_lines(self, frame, event, arg):
        """
            Logic to construct the args, kwargs based on functions
            and return values
        """
        try:
            # Trace only events while end of the function
            if event not in [RETURN, EXCEPTION]:
                return self.trace_lines

            if not self.validate_trace(frame, event, arg):
                return
            
            # Construct data about local var, func name etc
            f_code = frame.f_code
            local_vars = frame.f_locals
            func_name = f_code.co_name
            caller_fn = frame.f_back.f_code.co_name

            # While tracing, we might encounter function calls
            # to different classes. So tracking the events
            # based on functions of different classes
            instance_obj = local_vars.get('self', None)
            if instance_obj:
                class_name = instance_obj.__class__.__name__
            else:
                class_name = 'self'

            if class_name in IGNORED_CLASSES:
                return

            # Construct the event data
            if class_name not in self.__events_data:
                self.__events_data[class_name] = dict()

            if func_name not in self.__events_data[class_name]:
                self.__events_data[class_name][func_name] = list()

            # Custom Event Record
            event_record = dict(is_exception=(event == EXCEPTION))
            for var, value in local_vars.items():
                if var in ['self']:
                    continue
                else:
                    event_record[var] = value

            # wrapper is the decorator function which enables the tracing
            if caller_fn != 'wrapper':
                if caller_fn in self.__events_data[class_name]:
                    caller_fun_idx = len(self.__events_data[class_name][caller_fn])
                else:
                    caller_fun_idx = 1
                event_record['caller_fn'] = f'{class_name}_{caller_fn}'
                event_record['caller_fn_id'] = caller_fun_idx - 1 if caller_fun_idx else 0
            
            # Push the event record
            self.__events_data[class_name][func_name].append(event_record)
        except Exception as exc:
            logger.error(str(exc))
            logger.error(traceback.format_exc())
        return self.trace_lines

    def get_event_data(self, **kwargs):
        """
            Getter method to access events data
        """
        return self.__events_data

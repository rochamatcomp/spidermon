import inspect
from unittest import TestLoader
from functools import cmp_to_key as _cmp_to_key

from .monitors import Monitor
from .suites import MonitorSuite
from .exceptions import InvalidMonitor


class MonitorLoader(TestLoader):
    def load_suite_from_monitor(self, monitor_class, name=None):
        if not (inspect.isclass(monitor_class) and issubclass(monitor_class, Monitor)):
            raise InvalidMonitor('monitor must be a class subclassing Monitor')
        test_function_names = self.get_testcase_names(monitor_class)
        if not test_function_names and hasattr(monitor_class, 'runTest'):
            test_function_names = ['runTest']
        #monitors = [monitor_class(function_name, name=name) for function_name in test_function_names]
        loaded_suite = MonitorSuite(
            monitors=map(monitor_class, test_function_names),
            name=name
        )
        return loaded_suite

    def get_testcase_names(self, monitor_class):
        def is_test_method(attrname, class_name=monitor_class, prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and \
                hasattr(getattr(class_name, attrname), '__call__')
        test_function_names = filter(is_test_method, dir(monitor_class))
        if self.sortTestMethodsUsing:
            test_function_names.sort(key=_cmp_to_key(self.sortTestMethodsUsing))
        return test_function_names


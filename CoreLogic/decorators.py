'''Allows for easy troubleshooting by providing the returns etc'''
import time
import logging
import json
from CoreLogic.args import argsmain
argsmain()

with open('json/config.json', 'r', encoding="utf-8") as file:
    config = json.loads(file.read())
    debug = config['debug']


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(funcName)s:%(message)s')



def classlogger(cls):
    '''DEBUG mode for troubleshooting'''

    if not debug:
        return cls

    class WrappedClass(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            logging.debug(f"\nClass: {cls.__name__}")
            logging.debug(self.__str__())

    return WrappedClass


def logger(func):
    '''DEBUG mode for troubleshooting'''
    if func.__name__ == 'main':
        func()

    if (not debug):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper

    elif (debug):
        def wrapper(*args, **kwargs):
            try:
                start = time.perf_counter()
                result = func(*args, **kwargs)
                end = time.perf_counter()
                parameters = ', '.join(f'{keyword} = {value}' for keyword, value in kwargs.items())
                arg_values = [arg if arg != args[0] else "self" for arg in args]
                arguments = ', '.join(str(arg) for arg in arg_values)
                logging.debug(f"\nRun function: {func.__name__}()\n\tTook {end - start:.5f}s\n\tReturned {result}\n\tParams used:\n\t   *args: {arguments}\n\t   **kwargs: {parameters if any(parameters) else 'None'}")
                return result
            except Exception as exp:
                logging.error(f'Error running Function {func.__name__}() with the error\n{exp}')
                return 101
    
        return wrapper
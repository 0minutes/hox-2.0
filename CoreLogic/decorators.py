'''
Using time to calculate the time a function took to run
Using json to extract either DEBUG mode is on
'''
import time
import json

with open('json/config.json', 'r', encoding="utf-8") as file:
    config = json.loads(file.read())
    debug = config['debug']

def classlogger(cls):
    '''DEBUG mode for troubleshooting'''
    if (not debug):
        return cls
    
    classparams = cls.__init__.__code__.co_varnames[1:]

    print(f'Class: {cls.__name__}\n\tParameters: {", ".join(classparams)}\n\tFunctions: {len([func for func in dir(cls) if callable(getattr(cls, func)) and not func.startswith("__")])}')

    return cls


def logger(function):
    '''DEBUG mode for troubleshooting'''
    if (not debug):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        
        return wrapper

    elif (debug):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            parameters = ', '.join(f'{keyword} = {value}' for keyword, value in kwargs.items())
            arg_values = [arg if arg != args[0] else "self" for arg in args]
            arguments = ', '.join(str(arg) for arg in arg_values)
            print(f"Run function: {function.__name__}()\n\tTook {end - start:.5f}s\n\tReturned {result}\n\tParams used:\n\t   *args: {arguments}\n\t   **kwargs: {parameters if any(parameters) else 'None'}")
            return result
    
        return wrapper
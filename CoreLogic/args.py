'''Allows the user to use arguments prerun of hox.py for example -d for debugging'''
import argparse
import json

with open('json/config.json', 'r', encoding='utf-8') as f:
    current = json.loads(f.read())

def setdebug(value: bool):
    global current
    configuration = {
    'prefix': current['prefix'],
    'logs': current['logs'],
    'debug': value
    }

    with open('json/config.json', 'w', encoding='utf-8') as configfile:
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()


def setprefix(value: str):
    global current
    configuration = {
    'prefix': value,
    'logs': current['logs'],
    'debug': current['debug'],
    }

    with open('json/config.json', 'w', encoding='utf-8') as configfile:
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()

def setlogs(value: bool):
    global current
    configuration = {
    'prefix': current['prefix'],
    'logs': value,
    'debug': current['debug'],
    }

    with open('json/config.json', 'w', encoding='utf-8') as configfile:
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()

def argsmain() -> None:  
    global current  
    parser = argparse.ArgumentParser(description='Arguments for prerun hox.py')
    parser.add_argument('-d', help='1/0 (1=True 0=False) enable debug for hox.py', default=False, type=int)
    parser.add_argument('-p', help='allows the user to enter any prefix for hox.py prerun', default=current['prefix'], type=str)
    parser.add_argument('-l', help='Allows the user to change logs to either 1/0 (1=True 0=False) prerun', default=current['logs'], type=int)
    arguments = parser.parse_args()

    if arguments.d != current['debug']:
        match arguments.d:
            case 1: setdebug(True)
            case 0: setdebug(False)
            case _: raise Exception(f"error: argument -d: invalid value: {arguments.l}")
            
    if arguments.l != current['logs']:
        match arguments.l:
            case 1: setlogs(True)
            case 0: setlogs(False)
            case _: raise Exception(f"error: argument -l: invalid value: {arguments.l}")
    
    if arguments.p != current['prefix']: setprefix(arguments.p)

'''Allows the user to use arguments prerun of hox.py for example -d for debugging'''
import argparse
import json



def setdebug(value: bool):
    with open('json/config.json', 'r', encoding='utf-8') as f:
        current = json.loads(f.read())

    configuration = {
    'prefix': current['prefix'],
    'logs': current['logs'],
    'debug': value,
    'cwd': current['cwd'],
    }

    with open('json/config.json', 'w', encoding='utf-8') as configfile:
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()
    return

def setprefix(value: str):
    with open('json/config.json', 'r', encoding='utf-8') as f:
        current = json.loads(f.read())

    configuration = {
    'prefix': value,
    'logs': current['logs'],
    'debug': current['debug'],
    'cwd': current['cwd'],
    }

    with open('json/config.json', 'w', encoding='utf-8') as configfile:
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()

    return

def setlogs(value: bool):
    with open('json/config.json', 'r', encoding='utf-8') as f:
        current = json.loads(f.read())

    configuration = {
    'prefix': current['prefix'],
    'logs': value,
    'debug': current['debug'],
    'cwd': current['cwd'],
    }

    with open('json/config.json', 'w', encoding='utf-8') as configfile:
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()
    return

def setcwd(value: bool):
    with open('json/config.json', 'r', encoding='utf-8') as f:
        current = json.loads(f.read())

    configuration = {
    'prefix': current['prefix'],
    'logs': current['logs'],
    'debug': current['debug'],
    'cwd': value,
    }

    with open('json/config.json', 'w', encoding='utf-8') as configfile:
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()
    return

def argsmain() -> None:  
    with open('json/config.json', 'r', encoding='utf-8') as f:
        current = json.loads(f.read())
        
    parser = argparse.ArgumentParser(description='Arguments for prerun hox.py')
    parser.add_argument('-d', '--debug', help='1/0 (1=True 0=False) enable debug for hox.py', default=False, type=int)
    parser.add_argument('-l', '--logs', help='1/0 (1=True 0=False) enable logs for hox.py', default=int(current['logs']), type=int)
    parser.add_argument('-dir','--dir',help='1/0 (1=True 0=False) enable view dir for hox.py', default=int(current['cwd']), type=int)
    parser.add_argument('-p', '--prefix', help='Enter any prefix for hox.py prerun', default=str(current['prefix']), type=str)
    arguments = parser.parse_args()

    if arguments.prefix != current['prefix']:
        setprefix(arguments.prefix)

    if arguments.debug == 0:
        setdebug(False)
    elif arguments.debug == 1:
        setdebug(True)
    else:
        print(f'Invalid {arguments.debug} option for -d[D] argument')
        quit()

    if arguments.logs == 0:
        setlogs(False)
    elif arguments.logs == 1:
        setlogs(True)
    else:
        print(f'Invalid {arguments.logs} option for -l[L] argument')
        quit()

    if arguments.dir == 0:
        setcwd(False)
    elif arguments.dir == 1:
        setcwd(True)
    else:
        print(f'Invalid {arguments.dir} option for -dir[L] argument')
        quit()

    return
'''Main loop runs here'''
import os
import json
from CoreLogic.handler import Handler
from CoreLogic.logs import Logs
from CoreLogic.decorators import logger
from CoreLogic.variables import Variables


@logger
def main() -> int: 
    '''Main Function'''
    with open('json/config.json', 'r', encoding="utf-8") as file:
        config = json.loads(file.read())
        file.close()

    logs = config['logs']
    debug = config['debug']
    cwd = config['cwd']
    log = Logs()
    
    if cwd:
        print(os.getcwd())
    
    prompt = f'{">" if (debug is False) else "D>"} '

    while True:
        user = input(prompt)
        if (logs): log.writefile(user)
        responce = Handler().result(user)

        if (responce == Variables.logson): logs = True
        elif (responce == Variables.logsoff): logs = False
        elif (responce == 200): quit(0)

if __name__ == '__main__':
    main()
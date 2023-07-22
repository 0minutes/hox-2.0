'''Main loop runs here'''
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

    prefix = config['prefix']
    logs = config['logs']
    debug = config['debug']
    log = Logs()

    while True:
        prompt = input(f'{prefix if (debug is False) else "D"} ')
        if (logs): log.writefile(prompt=prompt)

        responce = Handler().result(prompt=prompt)

        if responce == Variables.logson: logs = True
        if responce == Variables.logsoff: logs = False
        if responce == 200: return 0

        # match Handler().result(prompt):
        #     case 300: logs = False
        #     case 301: logs = True
        #     case 200: return 0

main()
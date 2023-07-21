'''Main loop runs here'''
import json
from CoreLogic.handler import Handler
from CoreLogic.logs import Logs
from CoreLogic.decorators import logger


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
        handler = Handler(prefix=prefix, prompt=prompt)

        match handler.match():
            case 300: logs = False
            case 301: logs = True
            case 200: return 0

main()
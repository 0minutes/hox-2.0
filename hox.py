'''Using json to extract prefix and logs variables'''
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
    logs=config['logs']
    log = Logs()

    while True:

        prompt = input(f'<{prefix}>')

        if (logs):
            log.writefile(prompt=prompt)

        handler = Handler(prefix=prefix, prompt=prompt)

        match handler.match():
            case 200:
                return 0

            case 300:
                logs = False
            
            case 301:
                logs = True

main()

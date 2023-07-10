'''Using json to extract prefix and logs variables'''
import json
from CoreLogic.const import Variables
from CoreLogic.handler import Handler


def main() -> int:
    '''Main Function'''
    with open('CoreLogic/config.json', 'r', encoding="utf-8") as file:
        config = json.loads(file.read())
        file.close()

    prefix = config['prefix']

    # logs=config['logs']

    while True:
        if (
            Handler
            (
                prompt=input(f'<{prefix}>'),
                prefix=prefix
            ).match() == Variables.quit):
            return 0


main()

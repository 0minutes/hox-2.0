from CoreLogic.const import Variables
from CoreLogic.Handler import Handler


def main() -> int:
    while (True):
        if (Handler(prompt=input(f'<{Variables.prefix}>')).match() == Variables.Quit):
            return 0

if __name__ == '__main__':
    main()
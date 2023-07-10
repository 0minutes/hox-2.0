"""Using OS to perform shell commands"""
import os
from CoreLogic.const import Variables
from CoreLogic.file import FileManageClass
from CoreLogic.config import Config
from CoreLogic.logs import Logs

class Handler:
    """Handles all the input coming from the user and provides an output depending on the input"""
    
    def __init__(self, prompt: str = None, prefix: str = None) -> None:
        self.prompt: str = prompt
        self.prefix: str = prefix
        self.promptslice: list = prompt.split()
        self.promptlower: str = prompt.lower()
        self.promptlowerslice: list = prompt.lower().split()

    def match(self) -> int:
        """Matches the input to the right command or executed the command"""
        if (self.prompt.startswith(self.prefix)):
            
            if (self.promptlowerslice[0] == f'{self.prefix}q' or self.promptlowerslice[0] == f'{self.prefix}quit'):
                return Variables.quit
            
            elif (self.promptlowerslice[0] == f'{self.prefix}cfg' or self.promptlowerslice[0] == f'{self.prefix}config'):
                return Config(prefix='$', logs=True).promptcheck(self.prompt)
            
            elif (self.promptlowerslice[0] == f'{self.prefix}f' or self.promptlowerslice[0] == f'{self.prefix}file'):
                return FileManageClass(prefix=self.prefix).promptcheck(userprompt=self.prompt)
            
            elif (self.promptlowerslice[0] == f'{self.prefix}l' or self.promptlowerslice[0] == f'{self.prefix}logs'):
                return Logs().promptcheck(prompt=self.prompt)

            elif (self.promptlowerslice[0] == f'{self.prefix}h' or self.promptlowerslice[0] == f'{self.prefix}help'):
                return self.help()

            print(f'Unknown command: {self.prompt}')
            return Variables.error

        os.system(self.prompt)
        return Variables.success

    def help(self) -> int:
        """The help function matches the command name to show it's help message"""
        match len(self.promptslice):
            case 1:
                print(f'''COMMANDS LIST:
        {self.prefix}h(help)     <command> -> shows the current messages or displays help of a provided command
        {self.prefix}f(file)     <command> -> shows help for all the file commands or executes a given command
        {self.prefix}l(logs)     <command> -> shows help for all the logs commands or executes a given command
        {self.prefix}cfg(config) <command> -> shows help for all the config commands or executes a given command''')
                return Variables.success

            case 2:
                match self.promptlowerslice[1]:
                    case 'f' | 'file':
                        FileManageClass(prefix = self.prefix).filehelp()
                        return Variables.success

                    case 'l' | 'logs':
                        Logs().logshelp()
                        return Variables.success

                    case default:
                        print(f'{default} is an unknown command')
                        return Variables.error

            case default:
                print(
                f'Unknown command ({self.promptslice[-2]}) subcommand ({self.promptlowerslice[-1]})')
                return Variables.error

"""Handles all input coming in from the main function"""
import os
from CoreLogic.variables import Variables
from CoreLogic.file import FileManageClass
from CoreLogic.config import Config
from CoreLogic.logs import Logs
from CoreLogic.customcommands import Customcommands
from CoreLogic.decorators import logger, classlogger

@classlogger
class Handler:
    """Handles all the input coming from the user and provides an output depending on the input"""
    
    def __init__(self, prompt: str = None, prefix: str = None) -> None:
        self.prompt: str = prompt
        self.prefix: str = prefix
        self.promptslice: list = prompt.split()
        self.promptlower: str = prompt.lower()
        self.promptlowerslice: list = prompt.lower().split()

    @logger
    def match(self) -> int:
        """Matches the input to the right command or executed the command"""
        if (self.prompt.startswith(self.prefix)):
            
            if (self.promptlowerslice[0] == f'{self.prefix}q' or self.promptlowerslice[0] == f'{self.prefix}quit'):
                return Variables.quit
            
            elif (self.promptlowerslice[0] == f'{self.prefix}cfg' or self.promptlowerslice[0] == f'{self.prefix}config'):
                return Config(prefix='$', logs=True).promptcheck(self.prompt)
            
            elif (self.promptlowerslice[0] == f'{self.prefix}cc' or self.promptlowerslice[0] == f'{self.prefix}customcommands'):
                return Customcommands().promptcheck(self.prompt)
            
            elif (self.promptlowerslice[0] == f'{self.prefix}f' or self.promptlowerslice[0] == f'{self.prefix}file'):
                return FileManageClass(prefix=self.prefix).promptcheck(userprompt=self.prompt)
            
            elif (self.promptlowerslice[0] == f'{self.prefix}l' or self.promptlowerslice[0] == f'{self.prefix}logs'):
                return Logs().promptcheck(prompt=self.prompt)

            elif (self.promptlowerslice[0] == f'{self.prefix}h' or self.promptlowerslice[0] == f'{self.prefix}help'):
                return self.help()
            
            elif (self.promptlowerslice[0] == f'{self.prefix}e'or self.promptlowerslice[0] == f'{self.prefix}eval'):
                return self.manualeval()
            

            print(f'Unknown command: {self.prompt}')
            return Variables.error
        
        os.system(self.prompt)
        return Variables.success
    
    @logger
    def manualeval(self):
        match self.promptlowerslice[0]:
            case 'e': os.system(self.prompt.removeprefix(f'{self.prefix}e '))
            case 'eval': os.system(self.prompt.removeprefix(f'{self.prefix}eval '))
        return Variables.success

    @logger
    def help(self) -> int:
        """The help function matches the command name to show it's help message"""
        match len(self.promptslice):
            case 1:
                print(f'''COMMANDS LIST:
        {self.prefix}h(help)     <command> -> shows the current messages or displays help of a provided command
        {self.prefix}f(file)     <command> -> shows help for all the file commands or executes a given command
        {self.prefix}l(logs)     <command> -> shows help for all the logs commands or executes a given command
        {self.prefix}cfg(config) <command> -> shows help for all the config commands or executes a given command
        {self.prefix}cc(customcommands) <command> -> shows help for all the cc functions or executes a given command''')
                return Variables.success

            case 2:
                match self.promptlowerslice[1]:
                    case 'f' | 'file': return FileManageClass(prefix = self.prefix).filehelp()
                    case 'l' | 'logs': return Logs().logshelp()
                    case 'c' | 'customcommands': return Customcommands().cchelp()

                    case default:
                        print(f'{default} is an unknown command')
                        return Variables.error

            case default:
                print(
                f'Unknown command ({self.promptslice[-2]}) subcommand ({self.promptlowerslice[-1]})')
                return Variables.error

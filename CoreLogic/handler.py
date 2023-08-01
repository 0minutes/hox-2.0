"""Handles all input coming in from the main function"""
import os
import json
from CoreLogic.variables import Variables
from CoreLogic.file import FileManageClass
from CoreLogic.config import Config
from CoreLogic.logs import Logs
from CoreLogic.customcommands import Customcommands
from CoreLogic.decorators import logger, classlogger

@classlogger
class Handler:
    """Handles all the input coming from the user and provides an output depending on the input"""
    
    def __init__(self) -> None:
        with open('json/config.json', 'r', encoding='utf-8') as file:
            self.configuration = json.loads(file.read())
            file.close()

        self.prefix: str = self.configuration['prefix']

    def __str__(self) -> str:
        return f'''
    Params: 
        {self.prefix = }
    Method Count: {len([func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("__")])}
        '''

    @logger
    def result(self, userinput) -> int:
        """Matches the input to the right command or executed the command"""
        
        promptlowerslice: list = userinput.lower().split()
        if (userinput.startswith(self.prefix)):
            
            if (promptlowerslice[0] == f'{self.prefix}q' or promptlowerslice[0] == f'{self.prefix}quit'):return Variables.quit
            elif (promptlowerslice[0] == f'{self.prefix}cfg' or promptlowerslice[0] == f'{self.prefix}config'): return Config().promptcheck(userinput)
            elif (promptlowerslice[0] == f'{self.prefix}cc' or promptlowerslice[0] == f'{self.prefix}customcommands'): return Customcommands().promptcheck(userinput)
            elif (promptlowerslice[0] == f'{self.prefix}f' or promptlowerslice[0] == f'{self.prefix}file'): return FileManageClass().promptcheck(userinput)
            elif (promptlowerslice[0] == f'{self.prefix}l' or promptlowerslice[0] == f'{self.prefix}logs'): return Logs().promptcheck(userinput)
            elif (promptlowerslice[0] == f'{self.prefix}h' or promptlowerslice[0] == f'{self.prefix}help'): return self.help(userinput)

            print(f'Unknown command: {userinput}')
            return Variables.error
        
        os.system(userinput)
        return Variables.success


    @logger
    def help(self, prompt) -> int:
        """The help function matches the command name to show it's help message"""

        promptslice: list = prompt.split()
        promptlowerslice: list = prompt.lower().split()

        match len(promptslice):
            case 1:
                print(f'''COMMANDS LIST:
        {self.prefix}h(help)     <command> -> shows the current messages or displays help of a provided command
        {self.prefix}f(file)     <command> -> shows help for all the file commands or executes a given command
        {self.prefix}l(logs)     <command> -> shows help for all the logs commands or executes a given command
        {self.prefix}cfg(config) <command> -> shows help for all the config commands or executes a given command
        {self.prefix}cc(customcommands) <command> -> shows help for all the cc functions or executes a given command''')
                return Variables.success

            case 2:
                match promptlowerslice[1]:
                    case 'f' | 'file': return FileManageClass(prefix = self.prefix).filehelp()
                    case 'l' | 'logs': return Logs().logshelp()
                    case 'c' | 'customcommands': return Customcommands().cchelp()

                    case default:
                        print(f'{default} is an unknown command')
                        return Variables.error

            case default:
                print(
                f'Unknown command ({promptslice[-2]}) subcommand ({promptlowerslice[-1]})')
                return Variables.error

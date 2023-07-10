'''Using json to extract logs variables and datetime to make an appropritate name for the log file'''
import json
import datetime
import os
from typing import Union
from CoreLogic.const import Variables

class Logs:
    """Handles all the logs and whats happening"""
    def __init__(self) -> None:
        with open('CoreLogic/config.json', 'r', encoding='utf-8') as file:
            configuration = json.loads(file.read())
            file.close()

        self.logfile = None
        self.prefix = configuration['prefix']
        self.logs = configuration['logs']
        self.folderpath = 'logs/'

    def promptcheck(self, prompt:str) -> int:
        """Checks the input of the user to match the subcommand to the right function"""
        splitprompt: list = prompt.split()

        if ((splitprompt[0].lower() == f'{self.prefix};' and len(splitprompt) == 1) or (splitprompt[0].lower() == f'{self.prefix}logs' and len(splitprompt) == 1)):
            self.logshelp()
            return Variables.success
        
        match splitprompt[1].lower():
            case 'c' | 'clear':
                return self.clearlogs()
            
            case 'on' | 'off':
                return self.update(prompt=prompt)

            case 'help' | 'h':
                return self.logshelp()

            case default:
                print(
                    f'Unknown subcommand \'{default}\' for the logs branch')
                return Variables.exerror

    def update(self, prompt: str) -> int:
        '''Updates the logs by turning them off or on'''
        splitprompt: list = prompt.split()

        match splitprompt[1].lower():
            case 'on':
                if (self.logs):
                    print('Logs already on')
                    return Variables.exerror
                
                configuration = {
                'prefix': self.prefix,
                'logs': True,
                }

                with open('CoreLogic/config.json', 'w', encoding="utf-8") as configfile:
                    configfile.write(json.dumps(configuration, indent=4))
                    configfile.close()


                print('Logs turned on')
                return Variables.logson
            
            case 'off':
                if (not self.logs):
                    print('Logs already off')
                    return Variables.exerror
                
                configuration = {
                'prefix': self.prefix,
                'logs': False,
                }

                with open('CoreLogic/config.json', 'w', encoding="utf-8") as configfile:
                    configfile.write(json.dumps(configuration, indent=4))
                    configfile.close()


                print('Logs turned off')
                return Variables.logsoff

    def logshelp(self) -> int:
        """Shows the commands for the logs class"""
        print(f'''LOGS:
    {self.prefix}l(logs) c(clear) -> Allows you to clear all the files in the logs folder
    {self.prefix}l(logs) on/off   -> Allows you change logs live''')

        return Variables.success

    def createfile(self) -> Union[str, None]:
        '''Creates the log file if one doesnt already exist'''
        if (self.logfile is not None):
            return self.logfile

        if (self.logs):

            os.makedirs(self.folderpath, exist_ok=True)

            time = datetime.datetime.now().strftime('%H-%M-%S')

            logfile = os.path.join(self.folderpath, f'logs-{time}.txt')
            with open(logfile, 'a', encoding='utf-8'):
                pass

            self.logfile = logfile
            return self.logfile

    def writefile(self, prompt: str) -> None:
        '''Writes inside the logfile if Logs are on otherwise not'''
        if (self.logfile is None):
            self.createfile()

        if (self.logs):
            with open(self.logfile, 'a', encoding='utf-8') as file:
                time = datetime.datetime.now().strftime('%H-%M-%S')
                file.write(f'[{time}]: {prompt}\n')

    def clearlogs(self) -> int:
        '''Clears all the files in the logs folder'''

        if (input('Are you sure you want to clear the logs folder? (y/n)').lower() == 'y'):
            if (not os.path.exists(self.folderpath)):
                print('The "logs" folder does not exist.')
                return Variables.error

            files = os.listdir(self.folderpath)

            for file in files:
                filepath = os.path.join(self.folderpath, file)
                try:
                    os.remove(filepath)
                    print(f'Removed: {os.path.basename(filepath)}')
                except OSError as exp:
                    print(f'Error deleting {os.path.basename(filepath)}:\n{exp}')

            return Variables.success

        print('Cancelled clearing logs...')
        return Variables.success

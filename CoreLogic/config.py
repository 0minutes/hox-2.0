'''Handles all input for configuration and allows user to change default settings'''
import json
from CoreLogic.variables import Variables
from CoreLogic.decorators import logger, classlogger

@classlogger
class Config:
    """All the commands used for configuration."""
    def __init__(self) -> None:
        with open('json/config.json', 'r', encoding='utf-8') as f:
            self.current = json.loads(f.read())

        self.currentprefix = self.current['prefix']
        self.currentlog = self.current['logs']
        self.defaults = {
            'prefix': '$',
            'logs': False,
            'debug': False,
            'cwd': False
        }
        self.dir = 'json/config.json'
    
    def __str__(self) -> str:
        return f'''
    Params:
        {self.defaults = }
        {self.dir = }
        {self.currentprefix = }
        {self.currentlog = }
        {self.current = }
    Method Count: {len([func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("__")])}
        '''

    @logger
    def promptcheck(self, userprompt) -> int:
        """Matches the user input to the right function"""
        splitprompt = userprompt.split()
        if ((splitprompt[0].lower() == f'{self.currentprefix}cfg' and len(splitprompt) == 1) or (splitprompt[0].lower() == f'{self.currentprefix}config' and len(splitprompt) == 1)):
            self.confighelp()
            return Variables.success

        match splitprompt[1].lower():
            case 'e' | 'edit':
                return self.editconfig()

            case 'v' | 'view':
                return self.viewconfig()

            case 'd' | 'default':
                return self.defaultconfig()

            case 'h' | 'help':
                return self.confighelp()

            case default:
                print(f'Unknown subcommand \'{default}\' for the config management branch')
                return Variables.exerror

    @logger
    def confighelp(self) -> int:
        """Shows all the functions in the config branch"""
        print(f'''CONFIG HELP:
        {self.currentprefix}cfg(config) e(edit)    -> allows you to edit the current configuration
        {self.currentprefix}cfg(config) v(view)    -> allows you to view the current configuration
        {self.currentprefix}cfg(config) d(default) -> allows you to load the default configuration: Logs off, prefix \'$\'''')

        return Variables.success

    @logger
    def defaultconfig(self) -> int:
        """Sets the config to default settings"""
        with open(self.dir, 'w', encoding="utf-8") as configfile:
            configfile.write(json.dumps(self.defaults, indent=4))
            configfile.close()
        
        print('Successfully loaded the default settings:\nLogs: off\nprefix: \'$\'')
        return Variables.logsoff
    
    @logger
    def editconfig(self) -> int:
        """Allows the user to edit the config"""
        prefix = input('Enter a prefix or leave blank for default ($): ')

        if (prefix == '' or prefix == ' '):
            prefix = '$'

        while (True):
            logs = input('Turn on logs? (y/n): ').lower()
            if (logs == 'y'):
                logs = True
                break

            elif (logs == 'n'):
                logs = False
                break
            
            else:
                print('Invalid input try again...')
        
        while (True):
            cwd = input('Turn on cwd? (y/n): ').lower()
            if (cwd == 'y'):
                cwd = True
                break

            elif (cwd == 'n'):
                cwd = False
                break
            
            else:
                print('Invalid input try again...')


        while (True):
            if (input('Save changes? (y/n): ').lower() == 'y'):
                configuration = {
                'prefix': prefix,
                'logs': logs,
                'debug': False,
                'cwd': cwd
                }

                with open(self.dir, 'w', encoding="utf-8") as configfile:
                    configfile.write(json.dumps(configuration, indent=4))
                    configfile.close()

                print('Changes saved')
                if (not logs):
                    return Variables.logsoff
                if (logs):
                    return Variables.logson

            if (input('Save changes? (y/n)').lower() == 'n'):
                print('Changes Cancelled.')
                return Variables.success

            print("Invalid input try again...")
    @logger
    def viewconfig(self) -> int:
        """Allows the user to view the current config"""
        print(f'''CURRENT CONFIG SETTINGS:
        LOGS: {self.currentlog}
        PREFIX: {self.currentprefix}''')
        return Variables.success

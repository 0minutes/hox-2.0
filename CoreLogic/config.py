'''Using json to extract prefix and logs variables'''
import json
from CoreLogic.variables import Variables
from CoreLogic.decorators import logger

class Config:
    """All the commands used for configuration."""
    def __init__(self, prefix: str, logs: bool) -> None:
        with open('json/config.json', 'r', encoding='utf-8') as f:
            current = json.loads(f.read())

        self.currentprefix = current['prefix']
        self.currentlog = current['logs']
        self.prefix = prefix
        self.logs = logs
        self.defaults = {
            'prefix': '$',
            'logs': False,
            'debug': False
        }
        self.dir = 'json/config.json'

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
        print(f'''FILE MANAGEMENT:
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
            if (input('Save changes? (y/n): ').lower() == 'y'):
                configuration = {
                'prefix': prefix,
                'logs': logs,
                'debug': False
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

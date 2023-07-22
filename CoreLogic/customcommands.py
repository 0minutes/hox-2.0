'''Handles all input and allows for custom commands which run different scripts'''
import json
import os
import datetime
from CoreLogic.variables import Variables
from CoreLogic.decorators import logger, classlogger

@classlogger
class Customcommands:
    '''Allows the user to add their own custom python scripts'''

    def __init__(self) -> None:
        with open('json/config.json', 'r', encoding='utf-8') as file:
            configuration = json.loads(file.read())
            file.close()

        self.prefix = configuration['prefix']
        self.logs = configuration['logs']

    def __str__(self) -> str:
        return f'''
    Params: 
        {self.logs = }
        {self.prefix = }
    Method Count: {len([func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("__")])}
        '''

    @logger
    def promptcheck(self, prompt: str) -> int:
        """Matches the user input to the right function"""
        splitprompt = prompt.split()
        if ((splitprompt[0].lower() == f'{self.prefix}cc' and len(splitprompt) == 1) or (splitprompt[0].lower() == f'{self.prefix}customcommands' and len(splitprompt) == 1)):
            return self.cchelp()

        match splitprompt[1].lower():
            case 'add':
                if len(splitprompt) == 4:
                    return self.jsonize(prompt=prompt)

                if len(splitprompt) < 4:
                    print(
                    f'Not enough arguments to satisfy the function -> {self.prefix}cc(customcommand) add <path> <name>')
                    return Variables.error

                if len(splitprompt) > 4:
                    print(
                    f'Unknown argument {splitprompt[-1]} for the directory in the cc add function')
                    return Variables.error
            
            case 'r' | 'remove':
                if len(splitprompt) == 3:
                    return self.remove(prompt=prompt)

                if len(splitprompt) < 3:
                    print(
                    f'Not enough arguments to satisfy the function -> {self.prefix}cc(customcommand) r <name>')
                    return Variables.error

                if len(splitprompt) > 3:
                    print(
                    f'Unknown argument {splitprompt[-1]} for the directory in the cc add function')
                    return Variables.error

            case 'e' | 'eval':
                if len(splitprompt) == 3:
                    return self.evaluate(prompt=prompt)

                if len(splitprompt) < 3:
                    print(
                    f'Not enough arguments to satisfy the function -> {self.prefix}cc(customcommand) eval <name>')
                    return Variables.error

                if len(splitprompt) > 3:
                    print(
                    f'Unknown argument {splitprompt[-1]} for the directory in the cc eval function')
                    return Variables.error

            case 'l' | 'list':
                return self.listcom()

            case default:
                print(
                f'Unknown subcommand \'{default}\' for the Custom Commands branch')
                return Variables.exerror

    @logger
    def cchelp(self) -> int:
        """Shows the commands for the customcommands class"""
        print(f'''CUSTOM COMMANDS:
        {self.prefix}cc(customcommands) add <path> <name> -> Allows you to add a file script to the list 
        {self.prefix}cc(customcommands) r(remove)  <name> -> Allows you to remove a file script to the list
        {self.prefix}cc(customcommands) e(eval)    <name> -> allows you to run the script 
        {self.prefix}cc(customcommands) l(list) -> shows all added script
        {self.prefix}cc(customcommands) h(help) -> shows this message''')

        return Variables.success

    @logger
    def filedata(self, path: str) -> str:
        '''Opens and reads data from a file and returns it to the '''

        try:
            with open(path, 'r', encoding="utf-8") as file:
                contents: str = file.read()
                return contents

        except FileNotFoundError:
            print(
                f"The file '{path}' doesn't exist! Double-check the file path.")
            return Variables.error

        except PermissionError:
            print(
                f"Permission denied. Unable to return data from file '{path}'.")
            return Variables.error

        except IsADirectoryError:
            print(f"'{path}' is a directory, not a file.")
            return Variables.error

        except Exception as exp:
            print(f"An unexpected error occurred: {exp}")
            return Variables.error

    @logger
    def remove(self, prompt: str) -> int:
        '''Removes a given script
        $cc r hox'''
        promptsplit: list = prompt.split()
        jsondata: list = json.load(open('json/customcommands.json', 'r', encoding='utf-8'))

        for index, script in enumerate(jsondata, start=0): #Retrieve script data
            if promptsplit[2] in script:
                scriptindex: int = index
                break
        
        jsondata.pop(scriptindex)
        
        with open('json/customcommands.json', 'w', encoding='utf-8') as customcommandfile:
            customcommandfile.write(json.dumps(jsondata, indent=4))
            customcommandfile.write('\n')
        print(f'Successfuly removed {promptsplit[2]} from custom commands!')
        return Variables.success

    @logger
    def jsonize(self, prompt: str) -> int:
        '''Convert the script into json in this format:
        
        {
            "hox": {
                "location": 'path/to/file',
                "AdditionDate": 'xxxx'
            }
        }\n
        prompt example "$cc add hox.py hox"
        - Retrieves data from the prompt
        - Gets creates a dict with the given name and script source
        - Converts it into json
        - Writes the json into a file.
        '''
        #0   1   2       3
        #$cc add path.py scriptname
        promptsplit: list = prompt.split()
        location = os.path.join(os.getcwd(), promptsplit[2])
        jsonform = {
            promptsplit[3]:{
                'location': location,
                'AdditionDate': f'{datetime.date.today()}'
            }
        }

        with open('json/customcommands.json', 'r', encoding="utf-8") as file:
            jsondata: list = json.loads(file.read())

        jsondata.append(jsonform)

        with open('json/customcommands.json', 'w', encoding="utf-8") as customcommandfile:
            customcommandfile.write(json.dumps(jsondata, indent=4))
            customcommandfile.write('\n')
        print(f'Successfuly added {promptsplit[3]} to custom commands!')
        return Variables.success
    
    @logger
    def listcom(self) -> int:
        '''Lists all the script names that exist in the jsonfile\n
        prompt example "$cc l/list"
        - Retrieves data by script name from json file
        - Gets all the script names
        - Prints all the names in order'''
        scriptnum = 0
        
        with open('json/customcommands.json', 'r', encoding='utf-8') as file:
            scriptdata: list = json.load(file)

        for script in scriptdata:
            scriptnum += 1
            for scriptkey, scriptvalue in script.items():
                print(f'{scriptnum}: {scriptkey} Added on: {scriptvalue["AdditionDate"]}')

        return Variables.success

    @logger
    def evaluate(self, prompt: str) -> int:
        '''evaluates the custom script\n
        prompt example "$cc e/eval scriptname"
        - Retrieves data by script name from json file
        - Gets the script
        - Executes its with the built in eval()'''
        
        splitprompt: list = prompt.split()

        with open('json/customcommands.json', 'r', encoding='utf-8') as file: #Retrieve all the script data from the json
            jsondata: list = json.load(file)
        
        for script in jsondata: #Check if the script name is in the json
            if (not splitprompt[2] in script):
                print(f'{splitprompt[2]} doesn\'t exist, try checking the spelling and try again!')
                return Variables.error
        
        for script in jsondata: #Retrieve script data
            if splitprompt[2] in script:
                scriptsource = script[splitprompt[2]]['location']
                break

        try:
            os.system(f'python {scriptsource}')
            return Variables.success
        
        except Exception as exp:
            print(f'An error occured while running:\n{exp}')
            return Variables.exerror

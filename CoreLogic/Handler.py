from CoreLogic.const import Variables
from CoreLogic.File import FileManageClass
import os

class Handler:
    def __init__(self, prompt: str) -> None:
        self.prompt: str = prompt
        self.prefix: str = Variables.prefix
        self.promptSlice: list = prompt.split()
        self.promptLower: str = prompt.lower()
        self.promptLowerSlice: list = prompt.lower().split()


    def match(self) -> int:

        if (self.prompt.startswith(self.prefix)):
            
            if (self.promptLowerSlice[0] == f'{self.prefix}q' or self.promptLowerSlice[0] == f'{self.prefix}quit'):
                return Variables.Quit
            
            elif (self.promptLowerSlice[0] == f'{self.prefix}f' or self.promptLowerSlice[0] == f'{self.prefix}file'):
                FileManageClass(prefix=self.prefix).PromptCheck(userprompt=self.prompt)

            elif (self.promptLowerSlice[0] == f'{self.prefix}h' or self.promptLowerSlice[0] == f'{self.prefix}help'):
                self.help()

            else:
                print(f'Unknown command: {self.prompt}')
                return Variables.Error

        else:
            os.system(self.prompt)
            return Variables.Success
        

    def help(self) -> int:

        match len(self.promptSlice):
            case 1:
                print(f'''COMMANDS LIST:
        {self.prefix}h(help) <command> -> shows the current messages or displays help of a provided command
        {self.prefix}f(file) <command> -> shows help for all the file commands or executes a given command''')
                return Variables.Success

            case 2:
                match self.promptLowerSlice[1]:
                    case 'f' | 'file':
                        from CoreLogic.File import FileManageClass
                        FileManageClass(prefix = Variables.prefix).fileHelp()
                        return Variables.Success

                    case default:
                        print(f'unknown command {self.promptSlice[1]}')
                        return Variables.Error

            case default:
                print(f'Unknown command ({self.promptSlice[-2]}) subcommand ({self.promptLowerSlice[-1]})')
                return Variables.Error
            
          
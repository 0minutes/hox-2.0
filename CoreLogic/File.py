import os
import shutil
from CoreLogic.const import Variables


class FileManageClass:
    def __init__(self, prefix) -> None:
        self.prefix: str = prefix
    
    def PromptCheck(self, userprompt) -> int:
        splitPrompt = userprompt.split()
        ifHelp = (splitPrompt[0] == f'{self.prefix}f' and len(splitPrompt) == 1 or splitPrompt[0] == f'{self.prefix}file' and len(splitPrompt) == 1)
        if ifHelp:
            self.fileHelp()
            return Variables.Success

        match splitPrompt[1].lower():
            case 'move' | 'mv':
                if len(splitPrompt) == 4:
                    return self.moveFile(userprompt)

                elif len(splitPrompt) > 3:
                    print(f'Unknown argument {splitPrompt[-1]} for the directory in the file move branch')
                    return Variables.Error

                elif len(splitPrompt) < 4:
                    print(f'Not enough arguments to satisfy the function -> {self.prefix}f(file) mv(move) <file dir> '
                          f'<to dir>')
                    return Variables.Error

            case 'view' | 'v':
                if len(splitPrompt) == 3:
                    return self.viewFile(userprompt)

                elif len(splitPrompt) < 3:
                    print(f'Not enough arguments to satisfy the function -> {self.prefix}f(file) v(view) <file dir>')
                    return Variables.Error

                elif len(splitPrompt) > 3:
                    print(f'Unknown argument {splitPrompt[-1]} for the directory in the file view branch')
                    return Variables.Error

            case 'copy' | 'c':
                if len(splitPrompt) < 4:
                    print(
                        f'Not enough arguments to satisfy the function -> {self.prefix}f(file) c(copy) <from file '
                        f'dir>'
                        f' <to file dir>')
                    return Variables.Error

                elif len(splitPrompt) == 4:
                    return self.fileToFile(userprompt)

            case 'del' | 'dl':
                if len(splitPrompt) < 3:
                    print(f'Not enough arguments to satisfy the function -> {self.prefix}f(file) dl(del) <file dir>')
                    return Variables.Error

                elif len(splitPrompt) == 3:
                    return self.delFile(userprompt)

                elif len(splitPrompt) > 3:
                    print(f'Unknown arguments \'{splitPrompt[-1]}\' for the directory in the file del '
                          f'branch')
                    return Variables.Error

            case 'help' | 'h':
                return self.fileHelp()

            case default:
                print(f'Unknown subcommand \'{userprompt.split()[1]}\' for the file management branch')
                return Variables.ExError

        return 0

    def fileHelp(self) -> int:
        print(f'''FILE MANAGEMENT:
        {self.prefix}f(file) c(copy) <from file dir> <to file dir> -> copies a file to another
        {self.prefix}f(file) v(view) <file dir> -> allows you to view a file
        {self.prefix}f(file) mv(move) <from file dir> <to file dir> -> allows you to move a file
        {self.prefix}f(file) dl(del) <file dir> -> allows you to delete a file''')

        return Variables.Success

    @staticmethod
    def moveFile(args: str) -> int:
        args: list = args.split()
        src: str = args[2]
        dst: str = args[3]

        if not os.path.isabs(src):
            src = os.path.join(os.getcwd(), src)

        if not os.path.isabs(dst):
            dst = os.path.join(os.getcwd(), dst)

        try:
            dst_folder = os.path.dirname(dst)
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)

            shutil.move(src, dst)
            print('Successfully moved the file!')
            return Variables.Success

        except FileNotFoundError:
            print(f"File not found: {src}")
            return Variables.Error

        except PermissionError:
            print(f"Permission denied: {src} or {dst}")
            return Variables.Error

        except IsADirectoryError:
            print(f"Source is a directory: {src}")
            return Variables.Error

        except shutil.Error as e:
            print(f"Error occurred while moving the file: {e}")
            return Variables.Error

        except Exception as e:
            print(f"An unknown error occurred: {e}")
            return Variables.ExError

    @staticmethod
    def fileToFile(args: str) -> int:
        args = args.split()

        try:
            with open(args[2], 'r') as initFile, open(args[3], 'w') as endFile:
                contents: str = initFile.read()
                endFile.write(contents)

            print('Successfully copied the file')
            return Variables.Success

        except FileNotFoundError:
            print(f"The file '{args[2]}' doesn't exist! Double-check the file path.")
            return Variables.Error

        except PermissionError:
            print(f"Permission denied. Unable to copy file '{args[2]}'.")
            return Variables.Error

        except IsADirectoryError:
            print(f"Cannot copy directory. Expected a file, but got '{args[2]}'.")
            return Variables.Error

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return Variables.ExError

    @staticmethod
    def viewFile(filepath: str) -> int:
        FilePathSplit = filepath.split()

        try:
            with open(FilePathSplit[2], 'r') as file:
                contents: str = file.read()
                print(contents)
                return Variables.Error

        except FileNotFoundError:
            print(f"The file '{FilePathSplit[2]}' doesn't exist! Double-check the file path.")
            return Variables.Error

        except PermissionError:
            print(f"Permission denied. Unable to view file '{FilePathSplit[2]}'.")

        except IsADirectoryError:
            print(f"'{FilePathSplit[2]}' is a directory, not a file.")
            return Variables.Error
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return Variables.Error

    @staticmethod
    def delFile(filepath: str) -> int:
        FilePath = filepath.split()

        try:
            os.remove(FilePath[2])
            print(f"File '{FilePath[2]}' deleted successfully.")
            return Variables.Success

        except FileNotFoundError:
            print(f"File '{FilePath[2]}' does not exist.")
            return Variables.Error

        except PermissionError:
            print(f"Permission denied. Unable to delete file '{FilePath[2]}'.")
            return Variables.Error
        
        except IsADirectoryError:
            print(f"'{FilePath[2]}' is a directory, not a file.")
            return Variables.Error
        
        except Exception as e:
            print(f"An error occurred while deleting the file '{FilePath[2]}': {str(e)}")
            return Variables.Error
        
        
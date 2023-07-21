"""Handles all the file commands"""
import os
import shutil
from CoreLogic.variables import Variables
from CoreLogic.decorators import logger, classlogger

@classlogger
class FileManageClass:
    """All the commands used for file management."""

    def __init__(self, prefix) -> None:
        self.prefix: str = prefix

    @logger
    def promptcheck(self, userprompt) -> int:
        """Checks the input of the user to match the subcommand to the right function"""
        splitprompt = userprompt.split()
        if ((splitprompt[0].lower() == f'{self.prefix}f' and len(splitprompt) == 1) or (splitprompt[0].lower() == f'{self.prefix}file' and len(splitprompt) == 1)):
            self.filehelp()
            return Variables.success

        match splitprompt[1].lower():
            case 'move' | 'mv':
                if len(splitprompt) == 4: return self.movefile(userprompt)

                if len(splitprompt) > 3:
                    print(
                    f'Unknown argument {splitprompt[-1]} for the directory in the file move branch')
                    return Variables.error

                if len(splitprompt) < 4:
                    print(
                    f'Not enough arguments to satisfy the function -> {self.prefix}f(file) mv(move) <file dir> <to dir>')
                    return Variables.error

            case 'view' | 'v':
                if len(splitprompt) == 3: return self.viewfile(userprompt)

                if len(splitprompt) < 3:
                    print(
                    f'Not enough arguments to satisfy the function -> {self.prefix}f(file) v(view) <file dir>')
                    return Variables.error

                if len(splitprompt) > 3:
                    print(
                    f'Unknown argument {splitprompt[-1]} for the directory in the file view branch')
                    return Variables.error

            case 'copy' | 'c':
                if len(splitprompt) < 4:
                    print(
                    f'Not enough arguments to satisfy the function -> {self.prefix}f(file) c(copy) <from file '
                    f'dir>'
                    f' <to file dir>')
                    return Variables.error

                if len(splitprompt) == 4: return self.filetofile(userprompt)

            case 'del' | 'dl':
                if len(splitprompt) < 3:
                    print(
                        f'Not enough arguments to satisfy the function -> {self.prefix}f(file) dl(del) <file dir>')
                    return Variables.error

                if len(splitprompt) == 3: return self.delfile(userprompt)

                if len(splitprompt) > 3:
                    print(f'Unknown arguments \'{splitprompt[-1]}\' for the directory in the file del '
                          f'branch')
                    return Variables.error

            case 'help' | 'h': return self.filehelp()

            case default:
                print(
                    f'Unknown subcommand \'{default}\' for the file management branch')
                return Variables.exerror

        return 0

    @logger
    def filehelp(self) -> int:
        """Shows the commands for the file management class"""
        print(f'''FILE MANAGEMENT:
        {self.prefix}f(file) c(copy) <from file dir> <to file dir> -> copies a file to another
        {self.prefix}f(file) v(view) <file dir> -> allows you to view a file
        {self.prefix}f(file) mv(move) <from file dir> <to file dir> -> allows you to move a file
        {self.prefix}f(file) dl(del) <file dir> -> allows you to delete a file''')

        return Variables.success

    @staticmethod
    @logger
    def movefile(args: str) -> int:
        """Allows you to move a file by providing the dir of the file and where for it to end up"""
        args: list = args.split()
        src: str = args[2]
        dst: str = args[3]

        if not os.path.isabs(src): src = os.path.join(os.getcwd(), src)

        if not os.path.isabs(dst): dst = os.path.join(os.getcwd(), dst)

        try:
            dst_folder = os.path.dirname(dst)
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)

            shutil.move(src, dst)
            print('Successfully moved the file!')
            return Variables.success

        except FileNotFoundError:
            print(f"File not found: {src}")
            return Variables.error

        except PermissionError:
            print(f"Permission denied: {src} or {dst}")
            return Variables.error

        except IsADirectoryError:
            print(f"Source is a directory: {src}")
            return Variables.error

        except shutil.Error as exp:
            print(f"Error occurred while moving the file: {exp}")
            return Variables.error

        except Exception as exp:
            print(f"An unknown error occurred: {exp}")
            return Variables.exerror

    @staticmethod
    @logger
    def filetofile(args: str) -> int:
        """Allows you to copy file to a different directory with a different name."""
        args = args.split()

        try:
            with open(args[2], 'r', encoding="utf-8") as initfile, open(args[3], 'w', encoding="utf-8") as endfile:
                contents: str = initfile.read()
                endfile.write(contents)

            print('Successfully copied the file')
            return Variables.success

        except FileNotFoundError:
            print(
                f"The file '{args[2]}' doesn't exist! Double-check the file path.")
            return Variables.error

        except PermissionError:
            print(f"Permission denied. Unable to copy file '{args[2]}'.")
            return Variables.error

        except IsADirectoryError:
            print(
                f"Cannot copy directory. Expected a file, but got '{args[2]}'.")
            return Variables.error

        except Exception as exp:
            print(f"An unexpected error occurred: {exp}")
            return Variables.exerror

    @staticmethod
    @logger
    def viewfile(filepath: str) -> int:
        """Outputs the contents of a file"""
        filepathsplit = filepath.split()

        try:
            with open(filepathsplit[2], 'r', encoding="utf-8") as file:
                contents: str = file.read()
                print(contents)
                return Variables.success

        except FileNotFoundError:
            print(
                f"The file '{filepathsplit[2]}' doesn't exist! Double-check the file path.")
            return Variables.error

        except PermissionError:
            print(
                f"Permission denied. Unable to view file '{filepathsplit[2]}'.")
            return Variables.error

        except IsADirectoryError:
            print(f"'{filepathsplit[2]}' is a directory, not a file.")
            return Variables.error

        except Exception as exp:
            print(f"An unexpected error occurred: {exp}")
            return Variables.error

    @staticmethod
    @logger
    def delfile(filepath: str) -> int:
        """Allows you to delete a file from a curtain directory."""
        filepathsplit = filepath.split()

        try:
            os.remove(filepathsplit[2])
            print(f"File '{filepathsplit[2]}' deleted successfully.")
            return Variables.success

        except FileNotFoundError:
            print(f"File '{filepathsplit[2]}' does not exist.")
            return Variables.error

        except PermissionError:
            print(f"Permission denied. Unable to delete file '{filepathsplit[2]}'.")
            return Variables.error

        except IsADirectoryError:
            print(f"'{filepathsplit[2]}' is a directory, not a file.")
            return Variables.error

        except Exception as exp:
            print(
            f"An error occurred while deleting the file '{filepathsplit[2]}': {str(exp)}")
            return Variables.error

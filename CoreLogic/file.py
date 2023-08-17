"""Handles all the file commands"""
import os
import shutil
import json
from CoreLogic.variables import Variables
from CoreLogic.decorators import logger, classlogger

@classlogger
class FileManageClass:
    """All the commands used for file management."""

    def __init__(self) -> None:
        with open('json/config.json', 'r', encoding='utf-8') as file:
            configuration = json.loads(file.read())
            file.close()
            
        self.prefix: str = configuration['prefix']
    
    def __str__(self) -> str:
        return f'''
    Params:
        {self.prefix = }
    Method Count: {len([func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("__")])}
        '''

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
            
            case 'sort' | 's':
                #$f s src
                if len(splitprompt) < 3:
                    print(
                        f'Not enough arguments to satisfy the function -> {self.prefix}f(file) s(sort) <folder dir>')
                    return Variables.error

                if len(splitprompt) == 3: return self.sortfiles(splitprompt[-1])

                if len(splitprompt) > 3:
                    print(f'Unknown arguments \'{splitprompt[-1]}\' for the directory in the file sort '
                          f'branch')
                    return Variables.error


            case 'help' | 'h': return self.filehelp()

            case default:
                print(
                    f'Unknown subcommand \'{default}\' for the file management branch')
                return Variables.exerror

        return 0

    @staticmethod
    @logger
    def sortfiles(src: str):
        try:
            dirlist = os.listdir(src)
            filteredlist = []

            for filename in dirlist:
                for char in list(filename):
                    if char == '.':
                        filteredlist.append(filename)

            musicsFolder = src + r'\music'
            picturesFolder = src + r'\pictures'
            videosFolder = src + r'\videos'
            projectsFolder = src + r'\projects'
            othersFolder = src + r'\others'
            executeableFolder = src + r'\exe'
            compressedFolder = src + r'\compressed'

            os.makedirs(musicsFolder, exist_ok=True)
            os.makedirs(picturesFolder, exist_ok=True)
            os.makedirs(videosFolder, exist_ok=True)
            os.makedirs(projectsFolder, exist_ok=True)
            os.makedirs(othersFolder, exist_ok=True)
            os.makedirs(executeableFolder, exist_ok=True)
            os.makedirs(compressedFolder, exist_ok=True)
            
            filesSorted = 0
            for file in filteredlist:
                extension = file.split('.')[-1]
                print(file)
                try:
                    match extension:
                        case 'webm' | 'mp4' | 'gif':
                            shutil.move(os.path.join(src, file), videosFolder)
                            print(f'Moved {file} to {videosFolder}')
                            filesSorted += 1

                        case 'png' | 'jpg' | 'ico' | 'pdn':
                            shutil.move(os.path.join(src, file), picturesFolder)
                            print(f'Moved {file} to {picturesFolder}')
                            filesSorted += 1
                            
                        case 'mp4' | 'wav' | 'mov':
                            shutil.move(os.path.join(src, file), musicsFolder)
                            print(f'Moved {file} to {musicsFolder}')
                            filesSorted += 1

                        case 'py' | 'js' | 'cpp' | 'c' | 'java' | 'HC' | 'C':
                            shutil.move(os.path.join(src, file), projectsFolder)
                            print(f'Moved {file} to {projectsFolder}')
                            filesSorted += 1

                        case 'exe':
                            shutil.move(os.path.join(src, file), executeableFolder)
                            print(f'Moved {file} to {executeableFolder}')
                            filesSorted += 1
                        
                        case 'zip' | '7z' | 'rar' | 'gz':
                            shutil.move(os.path.join(src, file), compressedFolder)
                            print(f'Moved {file} to {compressedFolder}')
                            filesSorted += 1

                        case default:
                            shutil.move(os.path.join(src, file), othersFolder)
                            print(f'Moved {file} to {othersFolder}')
                            filesSorted += 1
                            
                except (FileNotFoundError, shutil.Error, OSError) as e:
                    print(f"Error while moving {file}: {e}")
                    continue

                except Exception as e:
                    print(f"Unexpected error occurred while moving {file}: {e}")
                    continue

        except FileNotFoundError as e:
            print(f"Error: {e}")
            return Variables.error

        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            return Variables.error

        else:
            print(f'Successfully sorted {filesSorted} files')
            return Variables.success


    @logger
    def filehelp(self) -> int:
        """Shows the commands for the file management class"""
        print(f'''FILE MANAGEMENT:
        {self.prefix}f(file) c(copy)  <from file dir> <to file dir> -> copies a file to another
        {self.prefix}f(file) v(view)  <file dir> -> allows you to view a file
        {self.prefix}f(file) mv(move) <from file dir> <to file dir> -> allows you to move a file
        {self.prefix}f(file) s(sort)  <folder dir> -> Sorts all files into different folders
        {self.prefix}f(file) dl(del)  <file dir> -> allows you to delete a file''')

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

        if '/' in filepath:
            filename = filepath.split('/')[-1]
        elif '\\' in filepath:
            filename = filepath.split('\\')[-1]
        else:
            filename = filepath.split()[-1]

        try:
            with open(filepathsplit[2], 'r', encoding="utf-8") as file:
                contents: str = file.read()
                lines = contents.split('\n')
                print(f' ~                               {filename}')
                for line in lines:
                    print(f' ~ {line}')
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

import os
import colorama
import shlex
import pickle
import sys

argv = sys.argv
argc = len(sys.argv)

class FileNode:
    def __init__(self, name, is_directory=True, contents=None):
        self.name = name
        self.is_directory = is_directory
        if is_directory:
            self.contents = []
        else:
            self.contents = contents
    
    def __repr__(self):
        return f"Type: {'DIRECTORY' if self.is_directory else 'FILE'}\nName: {self.name}"

    def __str__(self):
        return f"Type: {'DIRECTORY' if self.is_directory else 'FILE'}\nName: {self.name}"
    
    def get_contents(self):
        return self.contents
    
class VirtualDisk:
    def __init__(self):
        self.root = FileNode('/')

    def check_if_exists(self, directory, name):
        for entry in directory.contents:
            if name == entry.name:
                return True
        return False
    
    def check_if_dir_exists(self, directory, name):
        for entry in directory.contents:
            if name == entry.name and entry.is_directory:
                return True
        return False
    
    def traverse_path(self, path):
        current_directory = self.root
        paths = [p for p in path.split('/') if p != '']
        for i in range(0, len(paths)):
            found = False
            for dir in current_directory.contents:
                if dir.is_directory and dir.name == paths[i]:
                    current_directory = dir
                    found = True
                    break
            if not found:
                print("Error: Invalid Path given.")
                return None
        return current_directory
    
    def get_traverse_string(self, path):
        current_directory = self.root
        traverse_string = '/'
        paths = [p for p in path.split('/') if p != '']
        for i in range(0, len(paths)):
            found = False
            for dir in current_directory.contents:
                if dir.is_directory and dir.name == paths[i]:
                    current_directory = dir
                    found = True
                    traverse_string += f'{dir.name}/'
                    break
            if not found:
                print("Error: Invalid Path given.")
                return '/'
        return traverse_string
    
    def create_directory(self, pathname):
        paths = [p for p in pathname.split('/') if p != '']
        dir_to_create = paths[-1]
        path_previous = '/'.join(paths[:-1])
        current_directory = self.traverse_path(path_previous)
        if current_directory is None:
            return
        
        if self.check_if_exists(current_directory, dir_to_create):
            print(f"Error: Cannot create {pathname}, path already exists.")
            return
        
        current_directory.contents.append(FileNode(dir_to_create))
    
    def create_file(self, pathname, contents):
        paths = [p for p in pathname.split('/') if p != '']
        file_to_create = paths[-1]
        path_previous = '/'.join(paths[:-1])
        current_directory = self.traverse_path(path_previous)
        if current_directory is None:
            return
        
        if self.check_if_exists(current_directory, file_to_create):
            print(f"Error: Cannot create {pathname}, path already exists.")
            return
        
        current_directory.contents.append(FileNode(file_to_create, False, contents))

    def remove_entry(self, pathname):
        paths = [p for p in pathname.split('/') if p != '']
        entry_to_remove = paths[-1]
        path_previous = '/'.join(paths[:-1])
        current_directory = self.traverse_path(path_previous)
        if current_directory is None:
            return
        current_directory.contents = [entry for entry in current_directory.contents if entry.name != entry_to_remove]
    
    def copy_entry(self, pathname_src, pathname_dest, remove=False):
        paths = [p for p in pathname_src.split('/') if p != '']
        entry_to_copy = paths[-1]
        path_previous = '/'.join(paths[:-1])
        source_directory = self.traverse_path(path_previous)

        paths = [p for p in pathname_dest.split('/') if p != '']
        entry_to_paste = paths[-1]
        path_previous = '/'.join(paths[:-1])
        destination_directory = self.traverse_path(path_previous)

        if source_directory is None or destination_directory is None:
            print("Error: One of source or destination paths is invalid during this copy-paste operation.")
            return
        
        src_file_entry = None
        for file in source_directory.contents:
            if file.name == entry_to_copy:
                src_file_entry = file
                break

        if src_file_entry is None:
            print("Entry to copy does not exist.")

        if src_file_entry.is_directory:
            new_dir = FileNode(entry_to_paste)
            new_dir.contents = src_file_entry.contents
            destination_directory.contents.append(new_dir)
        else:
            destination_directory.contents.append(FileNode(entry_to_paste, False, src_file_entry.contents))
        
        if remove:
            source_directory.contents = [entry for entry in source_directory.contents if entry.name != entry_to_copy]

    def list_directory(self, path):
        directory = self.traverse_path(path)
        if not directory.is_directory:
            print(f"{path} is not a directory.")
            return
        else:
            print(".    \t\tDIR\n..   \t\tDIR")
            for entry in directory.contents:
                if entry.is_directory:
                    print(colorama.Fore.BLUE + f"{entry.name}/\t\tDIR" + colorama.Fore.RESET)
                else:
                    print(f"{entry.name}\t\tFILE\t{len(entry.contents)} BYTES")

class VirtualDiskShell:
    def __init__(self, virtual_disk):
        self.virtual_disk = virtual_disk
        self.current_directory = '/'
    
    def shell(self):
        user_input = shlex.split(input(colorama.Fore.GREEN + "VIRDISK@" + colorama.Fore.BLUE + f"{self.current_directory}" + colorama.Fore.RESET + "$ "))
        command = user_input[0]

        if command == 'mkdir':
            if len(user_input) != 2:
                print("USAGE: mkdir <Directory Name>")
                return
            else:
                self.virtual_disk.create_directory(self.current_directory + f'{user_input[1]}/')
        elif command == 'touch':
            if len(user_input) != 2:
                print("USAGE: touch <File Name>")
                return
            else:
                self.virtual_disk.create_file(self.current_directory + f'{user_input[1]}', '')
        elif command == 'cd':
            if len(user_input) != 2:
                print("USAGE: cd <Directory Name>")
                return
            else:
                directory_to_change = user_input[1]
                if directory_to_change == '..':
                    self.current_directory = os.path.dirname(os.path.dirname(self.current_directory))
                    if self.current_directory != '/':
                        self.current_directory += '/'
                    return

                if directory_to_change.startswith('/'):
                    dirptr = self.virtual_disk.traverse_path(directory_to_change)
                    if dirptr is not None:
                        self.current_directory = self.virtual_disk.get_traverse_string(directory_to_change)
                        return
                    else:
                        print("Error: No such path exists.")
                        return 
                    
                dirptr = self.virtual_disk.traverse_path(self.current_directory + directory_to_change)
                if dirptr is not None:
                    self.current_directory = self.current_directory + f'{user_input[1]}/'
                else:
                    print("Error: No such directory exists.")
        elif command == 'echo':
            if len(user_input) == 2:
                print(user_input[1])
            elif len(user_input) == 4:
                if user_input[2] == '>':
                    file_path = user_input[3]
                    directory = self.virtual_disk.traverse_path(self.current_directory + os.path.dirname(file_path))
                    if directory is None:
                        print("Error: No such path exists.")
                        return
                    for file in directory.contents:
                        if file.name == os.path.basename(user_input[3]) and not file.is_directory:
                            file.contents += user_input[1]
                            return
                    print('No such file exists.')
                    return
                else:
                    print("USAGE: echo 'text' > filename.txt")
            else:
                print("USAGE: echo 'text' > filename.txt")
        elif command == 'ls':
            self.virtual_disk.list_directory(self.current_directory)
        elif command == 'cat':
            if len(user_input) == 2:
                file_path = user_input[1]
                directory = self.virtual_disk.traverse_path(self.current_directory + os.path.dirname(file_path))
                for file in directory.contents:
                    if file.name == os.path.basename(file_path) and not file.is_directory:
                        print(file.contents)
                        return
                    print('No such file exists.')
        elif command == 'rm':
            if len(user_input) != 2:
                print('USAGE: rm <Directory or File Name>')
                return
            self.virtual_disk.remove_entry(self.current_directory + f'{user_input[1]}')
        elif command == 'cp' or command == 'mv':
            if len(user_input) != 3:
                print("USAGE: cp/mv <Source> <Destination>")
                return
            source_path = user_input[1]
            destination_path = user_input[2]
            
            if source_path == '.':
                source_path = self.current_directory
            elif not source_path.startswith('/'):
                source_path = self.current_directory + source_path
            
            if destination_path == '.':
                destination_path = self.current_directory
            elif not destination_path.startswith('/'):
                destination_path = self.current_directory + destination_path

            if command == 'cp':
                self.virtual_disk.copy_entry(source_path, destination_path)
            else:
                self.virtual_disk.copy_entry(source_path, destination_path, True)
        elif command == 'dump':
            if len(user_input) != 2:
                print('USAGE: dump <virtual disk dump path>')
                return
            with open(user_input[1], 'wb') as f:
                pickle.dump(self.virtual_disk, f)
        elif command == 'exit':
            exit(0)

if argc > 1:
    with open(argv[1], 'rb') as f:
        vd = pickle.load(f)
else:
    vd = VirtualDisk()
vds = VirtualDiskShell(vd)

while True:
    vds.shell()

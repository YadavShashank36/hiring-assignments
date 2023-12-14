# Shell

## Introduction

This is a simple virtual disk shell implemented in Python. It provides basic functionalities to create directories, files, navigate through directories, copy/move entries, and more.

## Clone the repo

```bash
git clone https://github.com/YadavShashank36/hiring-assignments
```
## Classes

### FileNode

- Represents a file or directory entry.
- Contains attributes such as name, is_directory, and contents (for directories).

### VirtualDisk

- Manages the virtual disk and its operations.
- Includes methods to create directories, files, remove entries, copy/move entries, and list directory contents.

### VirtualDiskShell

- Implements a shell interface for interacting with the virtual disk.
- Allows the user to execute commands such as creating directories/files, navigating directories, copying/moving entries, and more.

## Usage

1. Run the script.
2. Enter commands at the prompt, such as:
   - `mkdir` <Directory Name>: Create a new directory.
   - `touch` <File Name>: Create a new file.
   - `cd` <Directory Name>: Change the current directory.
   - `echo` 'text' > filename.txt: Output text to the screen or a file.
   - `ls`: List contents of the current directory.
   - `cat` <File Name>: Display the contents of a file.
   - `rm` <Directory or File Name>: Remove a directory or file.
   - `cp` <Source> <Destination>: Copy an entry.
   - `mv` <Source> <Destination>: Move an entry.
   - `dump` <Virtual Disk Dump Path>: Dump the virtual disk as a pickle.
   - `exit`: Exit the virtual disk shell.

## Examples

```python
# Example: Create a new directory
mkdir /new_directory/

# Example: Create a new file
touch /new_file.txt

# Example: Change directory
cd /new_directory/

# Example: Output text to a file
echo 'Hello, World!' > greeting.txt

# Example: List contents of the current directory
ls

# Example: Display the contents of a file
cat greeting.txt

# Example: Remove a directory
rm /new_directory/

# Example: Copy a file to a new location
cp /source_file.txt /destination/

# Example: Move a directory to a new location
mv /source_directory/ /new_location/
```
![Preview Image](https://github.com/YadavShashank36/hiring-assignments/blob/main/1.png)
![Preview Image](https://github.com/YadavShashank36/hiring-assignments/blob/main/2.png)


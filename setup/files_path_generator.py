# The program to generate files path that required for .nsi files.
# Status: Abandon because switched to one-file build instead because it is easier.
# Author: Miracutor
# License: MIT
from pathlib import Path
from typing import List


# Create a list of files' path
release_path = Path(__file__).parent.parent / Path("dist")


# function to remove files in subdirectories from the list
def remove_files_in_subdirectories(full_file_list: List[Path]) -> List[Path]:
    path = []
    for file_item in full_file_list:
        if file_item.parent == release_path:
            path.append(file_item)

    return path


# function to format path in the root directory
def format_folder_files_path(full_file_list: List[Path]) -> str:
    output_str = "  SetOutPath $INSTDIR"
    for file_item in full_file_list:
        if file_item.is_dir():
            output_str += output_format_subdirectory_path(file_item)
        else:
            output_str += output_format_files_path(file_item)
    return output_str


# function to format subdirectories path
def output_format_subdirectory_path(dir_path: Path) -> str:
    path = generate_full_path_of_folder_in_subdirectories(dir_path)
    output_str = f'\n\n  CreateDirectory "{path}\n  SetOutPath {path}"'
    for file_item in dir_path.iterdir():
        output_str += f"{output_format_files_path(file_item)}"
    return output_str


# function to format files path
def output_format_files_path(file_path: Path) -> str:
    if file_path.is_dir():
        return output_format_subdirectory_path(file_path)
    else:
        return f'\n  file "{file_path}"'


# function to generate full path of folder in subdirectories
def generate_full_path_of_folder_in_subdirectories(dir_path: Path) -> str:
    if dir_path.parent == release_path:
        return f"$INSTDIR\\{dir_path.name}"
    else:
        return f"$INSTDIR\\{dir_path.relative_to(release_path)}"


# function to sort files with files first and directories last.
def sort_files_with_files_first_and_directories_last(
    full_file_list: List[Path],
) -> List[Path]:
    list_dirs = []
    list_files = []
    for file_item in full_file_list:
        if file_item.is_dir():
            list_dirs.append(file_item)
        else:
            list_files.append(file_item)

    return list_files + list_dirs


if __name__ == "__main__":
    # Create text file named path.txt
    path_file = Path("path.txt")
    path_file.touch()
    # Get the list of all files and directories in the release_path
    files_list = release_path.glob("**/*")
    # Change to normal array format
    files_list = list(files_list)
    # Remove files in subdirectories
    files_list = remove_files_in_subdirectories(files_list)
    # Sort files with files first and directories last
    files_list = sort_files_with_files_first_and_directories_last(files_list)
    # Combine all files' path into a string
    output_text = format_folder_files_path(files_list)
    # Write the list of files' path to the path.txt
    path_file.write_text(output_text)

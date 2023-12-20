import os


def file_existence_check(file):
    if os.path.exists(file):
        if os.path.isfile(file):
            return True
    return False

def delete_all_files(folder_path):
    file_list = os.listdir(folder_path)

    # Loop through each file and delete it
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
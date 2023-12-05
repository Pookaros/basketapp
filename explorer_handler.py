import csv
import pandas as pd
import os
import shutil
import json
from functools import reduce

#creatig a path variable to work wit the right directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def append_shot_data_to_csv(path, new_data):
    # if the file does not exist we create it
    if not os.path.exists(path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            existing_data = new_data
    else:
        # create df for the existing data
        existing_data = pd.read_csv(path)
        # Concat the 2 dataframes
        #existing_data = existing_data.combine_first(new_data)
        existing_data = pd.concat([existing_data, new_data])
    
    print("existing data1: " , existing_data)  
    existing_data = existing_data.combine_first(existing_data)
    print("existing data2: " , existing_data)  
    
    #create the csv
    existing_csv = existing_data.to_csv(path, index=False)
    

    return existing_csv

def append_list_to_new_column(csv_file, new_data, new_column_name):
    # Read the CSV file into a pandas DataFrame
    existing_data = pd.read_csv(csv_file)

    # Add a new column with the specified name and populate it with the new data
    existing_data[new_column_name] = new_data

    # Write the updated DataFrame back to the CSV file
    existing_data.to_csv(csv_file, index=False)

def create_folders_in_path(path):
    try:
        # Create the specified path along with any missing parent directories
        os.makedirs(path)
        print(f"Folder(s) created at '{path}'.")
    except FileExistsError:
        print(f"Folder(s) already exist at '{path}'.")

    return path

def delete_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Deleted directory and its contents: {directory_path}")
    except FileNotFoundError:
        print(f"The directory {directory_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting {directory_path}: {str(e)}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    except FileNotFoundError:
        print(f"{file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_file_extension(file_path:str, without_dot=False):

    # Use os.path.splitext() to get the file extension
    file_extension = os.path.splitext(file_path)[1]

    if without_dot:
        # Remove the leading dot (.) to get the extension without the dot
        file_extension = file_extension.lstrip(".")
    
    return file_extension

def read_shot_data_from_csv(path):
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def find_file_in_dir(top_directory, target_filename):
    files = []
    for root, dirs, files in os.walk(top_directory):
        for filename in files:
            if filename == target_filename:
                # Print the full path of the matching file
                file_path = os.path.join(root, filename)
                print("Matching file:", file_path)
                files.append(file_path)

    #return the list of the paths of the files
    return files

def find_subdirectory_in_dir(top_directory, target_dir):
    dirs = []
    for root, dirs, files in os.walk(top_directory):
        for dirname in dirs:
            if dirname == target_dir:
                # Print the full path of the matching file
                dir_path = os.path.join(root, dirname)
                print("Matching dir:", dir_path)
                dirs.append(dir_path)
    #return the list of the paths of the directories       
    return dirs

def image_file_exists(image_path:str) -> bool:
        exists = reduce(lambda x, y: x or y, [os.path.exists(image_path + extension) for extension in ['.jpg', '.jfif', '.png','.jpeg','.bmp']])
        if exists: print(f"File already exist at '{image_path}'.")
        else: print(f"The file {image_path} does not exist.")
        return exists

def img_file_exists(image_path):
    exists =  os.path.exists(image_path)
    if exists: 
        print(f"File already exist at '{image_path}'.")
    else: 
        print(f"The file {image_path} does not exist.")
    return exists

def dump_data_tojson(data, json_path):
    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)
#print(image_file_exists(r"D:\New folder\george\ML DL AI\AAA app\Members\Kim Hatson\KimHatson"))
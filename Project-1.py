import os
import shutil



def organize_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for file in files:
        file_extension = file.split('.')[-1]

        folder_path = os.path.join(directory, file_extension)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            shutil.move(os.path.join(directory, file), os.path.join(folder_path, file))

def main():
    directory = input("Enter the path to organize directory: ")
    if not os.path.exists(directory):
        print("This directory does not exist.")
    
        return
    organize_files(directory)
    print("Files are organized.")

if __name__ == "__main__":
    main()

import os
import shutil
import schedule
import time

from datetime import datetime, timedelta


def read_todays_files(folder_path):
    today = datetime.now().date() - timedelta(days= 1)
    print('today= ',today)

    # List all files in the specified folder
    all_files = os.listdir(folder_path)

    # Filter files modified today and delete them
    for file_name in all_files:
        file_path = os.path.join(folder_path, file_name)
        modification_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()

        if modification_date == today:
            try:
                # os.remove(file_path)
                print(f"Deleted file: {file_name}")
            except Exception as e:
                print(f"Error deleting file {file_name}: {e}")


# Replace 'your_folder_path' with the actual path to your folder
folder_path = 'C:\\Users\\saniya.pathan\\Downloads\\unfilled\\28_days\\'
todays_files_content = read_todays_files(folder_path)

# # Print the content of each file
# for file_name, content in todays_files_content.items():
#     print(f"Content of {file_name}:\n{content}")

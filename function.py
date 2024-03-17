from pymongo import MongoClient
import os
import pyautogui
from time import sleep
import json

def import_source(file_path, file_name):
    # Connect to MongoDB
    # Update the connection URL as needed
    client = MongoClient(
        'mongodb+srv://edentheegg12:fLyLrg0rj07SnVQF@cluster0.28q6b8i.mongodb.net/')
    # Replace 'your_database_name' with your database name
    db = client['news-test']
    for item in file_name:
        # Replace 'your_collection_name' with your collection name
        collection = db[item]

        # Query the MongoDB collection and convert the documents to a list
        data = list(collection.find({}, {'_id': 0}))
        # Define the file_path variable or use an existing path
        path = f'{file_path}'
        # Create the directory if it doesn't exist
        os.makedirs(path, exist_ok=True)

        # Specify the path for the JSON file
        # Update the path as needed
        json_file_path = os.path.join(path, f'{item}.json')

        # Export the data to a JSON file
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f'The collection has been exported to {json_file_path}')


def pressTab(count):
    for _ in range(count):
        pyautogui.press('tab')
        print('pressed tab')
        sleep(0.5)

def pressSpace():
    pyautogui.press('space')

def pastePath(file_path):
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.press('backspace')
    pyautogui.typewrite(file_path)
    sleep(1)

def pressEnter():
    pyautogui.press('enter')

def selectfile():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('enter')

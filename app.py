from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
from time import sleep
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui
import shutil
from function import *
from datetime import datetime
import sys

# date = datetime.today().date()
date = '2024-03-14'
service = Service(executable_path = r"C:\chromedriver-win64\chromedriver.exe")
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9030")
driver = webdriver.Chrome(service = service, options = options)

file_path = fr"{os.getcwd()}\startsource"
file_name = [f'category_day.{date}',
             f'deep_research_day.{date}', f'extra_research_day.{date}']

result_path = fr"{os.getcwd()}\endsource"
result_name = [f'prediction-day.{date}',
               f'prediction-week.{date}', f'prediction-month.{date}']
if os.path.exists(file_path):
    shutil.rmtree(file_path)
if os.path.exists(result_path):
    shutil.rmtree(result_path)

import_source(file_path, file_name)
import_source(result_path, result_name)

url = "https://chat.openai.com/g/g-yn2fRQ9y2-ted-trends"
driver.get(url)

confirm_start = input("Please confirm start(y/n):")
if confirm_start == 'n': 
    print("Exit this task")
    sys.exit(0)

pyautogui.hotkey('alt','tab')

categories = ['Politics', 'Business and Finance', 'Entertainment', 'Science and Technology', 'Sports', 'Crypto/Web3', 'Gaming', 'Law and Crime', 'Lifestyle and Health', 'Art and Fashion', 'glance']

responses = []

for category in categories:
    driver.get(url)
    sleep(1)

    attach_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Attach files"]')
    attach_btn.click()

    sleep(1)

    pressTab(5)
    pressSpace()
    pastePath(file_path)
    pressEnter()
    pressTab(4)
    selectfile()

    if category == 'glance':
        prompt = ["""###Task###\\nLet's think step by step.\\n\\nDescribe what you believe to be the next biggest development or emerging trend in the overall category of the news in general based on the predictions and summaries to the most relevant news topics on a 1-day time frame, 1 week timeframe, and the 1 month timeframe.\\n\\nYour analysis should be based on current trends, ongoing research, industry news, or any other relevant information sources.\\n\\n###Goal###\\nThink of it as what to look out for in the coming days, week, and month. A convergence of what will happen from input files and information in the next 24 hours, 1 week, and 1 month. use information from all of the topics to justify your reasoning.\\n\\n###explanation of input files###\\n\\nIncluded are a few files. The first is a category_day.json file which contains all of the different groupings of topics we have collected for all of the categories of news, the second is a file called extra_research_day.json which attempts to provide deeper research and insights into the topics created from the category_day.json, and lastly is a file called deep_research_day.json which based off of the deeper research file gives some potential ideas into what might happen as a result of the story in the news article occuring.\\n\\nSince we are dealing with the overall category of news. take into account all of the data in the input files\\n\\n###Keep in Mind###\\nWhen formulating your output do not make references in wording back to the original prompt - output should sound and flow naturally\\n\\n###Format###\\n1 day timeframe\\nDeveloping\\nTrend:\\nExplanation:\\nOpportunities that may arise:\\nPotential Pitfalls:\\n\\n1 week timeframe\\nDeveloping\\nTrend:\\nExplanation:\\nOpportunities that may arise:\\nPotential Pitfalls:\\n\\n1 month timeframe\\nDeveloping \\nTrend:\\nExplanation:\\nOpportunities that may arise:\\nPotential Pitfalls:"""]
    else:
        prompt = [f"""Imagine you are a professional news analyst and journalist\\n\\n###Task###\\nLet's think step by step.\\n\\nDescribe what you believe to be the next biggest development or emerging trend in the {category} category of the news based on the predictions and summaries to the most relevant news topics on a 1-day time frame, 1 week timeframe, and the 1 month timeframe.\\n\\nYour analysis should be based on current trends, ongoing research, industry news, or any other relevant information sources.\\n\\n###Goal###\\nThink of it as what to look out for in the coming days, week, and month. A convergence of what will happen from input files and information in the next 24 hours, 1 week, and 1 month. use information from all of the topics to justify your reasoning.\\n\\n###explanation of input files###\\n\\nIncluded are a few files. The first is a category_day.json file which contains all of the different groupings of topics we have collected for the science and tech category of news, the second is a file called extra_research_day.json which attempts to provide deeper research and insights into the topics created from the category_day.json, and lastly is a file called deep_research_day.json which based off of the deeper research file gives some potential ideas into what might happen as a result of the story in the news article occuring.\\n\\nSince we are dealing with the {category} category of news. Only focus on information that is relevant to that particular field\\n\\n###Keep in Mind###\\nWhen formulating your output do not make references in wording back to the original prompt - output should sound and flow naturally\\n\\n###Format###\\n1 day timeframe\\nDeveloping Trend:\\nExplanation:\\nOpportunities that may arise:\\nPotential Pitfalls:\\n\\n1 week timeframe\\nDeveloping Trend:\\nExplanation:\\nOpportunities that may arise:\\nPotential Pitfalls:\\n\\n1 month timeframe\\nDeveloping Trend:\\nExplanation:\\nOpportunities that may arise:\\nPotential Pitfalls:"""]

    input_box = driver.find_element(By.ID, 'prompt-textarea')
    input_box.clear()
    input_box.send_keys(prompt)

    send_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="send-button"]')
    while send_btn.is_enabled() == False:
        print('runing...')
        sleep(1)
    driver.execute_script('arguments[0].click();', send_btn)

    while send_btn.is_enabled() == False:
        print('runing...')
        sleep(1)
    response = driver.find_element(
        By.CSS_SELECTOR, f'div[data-testid="conversation-turn-3"]').find_element(By.TAG_NAME, 'p').text
    responses.append({'Prompt':category, 'Response':response})
    print(responses)

with open(fr'{result_path}\response.json', 'w') as file:
    json.dump(responses, file, indent=4)

new_prompt = [f"""You are a professional data analyst\\n\\nLet's think step by step\\n\\n###Task###\\nUsing the various input files copy the format of: {result_name[0]} to create an output in a python dictionary for the 1 day timeframe. response.json is the data you should be gathering data from to construct the output\\n\\n###Format###\\nThe format should follow this exactly and fill in the empty sections also do not return any other text but the following:\\n""", f"""You are a professional data analyst\\n\\nLet's think step by step\\n\\n###Task###\\nUsing the various input files copy the format of: {result_name[1]} to create an output in a python dictionary for the 1 week timeframe. response.json is the data you should be gathering data from to construct the output\\n\\n###Format###\\nThe format should follow this exactly and fill in the empty sections also do not return any other text but the following:\\n""", f"""You are a professional data analyst\\n\\nLet's think step by step\\n\\n###Task###\\nUsing the various input files copy the format of: {result_name[2]} to create an output in a python dictionary for the 1 month timeframe. response.json is the data you should be gathering data from to construct the output\\n\\n###Format###\\nThe format should follow this exactly and fill in the empty sections also do not return any other text but the following:\\n"""]

number = 0

for prompt in new_prompt:

    client = MongoClient(
        'mongodb+srv://edentheegg12:fLyLrg0rj07SnVQF@cluster0.28q6b8i.mongodb.net/')
        
    # Replace 'your_database' with your database name
    db = client['news-test']

    if result_name[number] in db.list_collection_names():
        print("Old subdirectory is replaced with new one")
        db[result_name[number]].drop()

    classify = ["""[{\\n  "category": "Sports",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n},\\n{\\n  "category": "Crypto/Web3",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n},\\n{\\n  "category": "Entertainment",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n}]""", """[{\\n  "category": "Law and Crime",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential \\nPitfalls": ""\\n  }\\n},\\n{\\n  "category": "Science and Technology",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n},\\n{\\n  "category": "at_glance",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n}]""", """[{\\n  "category": "Lifestyle and Health",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n},\\n{\\n  "category": \\n"Business and Finance",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may \\narise": "",\\n    "Potential Pitfalls": ""\\n  }\\n},\\n{\\n  "category": "Art and Fashion",\\n  "prediction": {\\n    "Developing \\nTrend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n}]""", """[{\\n  "category": "Politics",\\n  "prediction": {\\n    "Developing Trend 1": "",\\n    "Explanation": ".",\\n    "Opportunities that \\nmay arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n},\\n{\\n  "category": "Gaming",\\n  "prediction": {\\n    "Developing Trend1": "",\\n    "Explanation": ".",\\n    "Opportunities that may arise": "",\\n    "Potential Pitfalls": ""\\n  }\\n}]"""]
    for index, item in enumerate(classify):
        input_prompt = f"{new_prompt[number]}{classify[index]}"
        driver.get(url)
        sleep(1)

        attach_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Attach files"]')
        attach_btn.click()

        sleep(1)

        pressTab(5)
        pressSpace()
        pastePath(result_path)
        pressEnter()
        pressTab(4)
        selectfile()

        input_box = driver.find_element(By.ID, 'prompt-textarea')
        input_box.clear()
        input_box.send_keys(input_prompt)

        send_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="send-button"]')
        while send_btn.is_enabled() == False:
            print('runing...')
            sleep(1)
        driver.execute_script('arguments[0].click();', send_btn)

        while send_btn.is_enabled() == False:
            print('runing...')
            sleep(1)
        response = driver.find_element(
            By.CSS_SELECTOR, f'div[data-testid="conversation-turn-3"]').find_element(By.TAG_NAME,'p').text
        print(response)
        dump = json.loads(f"""{response}""")
        print(dump)

        # Replace 'your_subdirectory' with the subdirectory name
        collection = db[result_name[number]]
        # Insert the data into the subdirectory (collection)

        result = collection.insert_many(dump)

        print(f'{len(result.inserted_ids)} documents inserted into MongoDB subdirectory {result_name[number]}')

    number += 1

print("\nOur task is completed")



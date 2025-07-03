import numpy as np
import pandas as pd
import json
import os

def load_json_files(folder_path):
    #this function reads all the json files from a folder and converts them into a dataframe

    all_data = []     #stores the individual file paths, used for later reference
    
    for filename in os.listdir(folder_path):
        if filename.endswith('json'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file_path)

                    #check weather the data in the json file is in a form of dictionary or list

                    if isinstance(data, dict):
                        all_data.append(data)
                    elif isinstance(data, list):
                        all_data.extend(data)
                    else:
                        print(f'{file_path} unsupported JSON format')
            
            except Exception as e:
                print(f'Error : {e}')
    return pd.DataFrame(all_data)



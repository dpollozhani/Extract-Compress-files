#!/usr/bin/env python
# coding: utf-8

# In[30]:


import zipfile
import fnmatch as fn
import os
from pathlib import Path
import pprint
import re
from datetime import datetime
from tqdm import tqdm

pp = pprint.PrettyPrinter()
compression_complete = False

today_date = datetime.today().date().strftime("%Y%m%d")

while not compression_complete:
    user_input = input('Enter directory or file path (drag and drop): ')
    user_input = user_input.strip('"')
    
    input_is_file = os.path.isfile(user_input)
    input_is_dir = os.path.isdir(user_input)

    if input_is_file:
        file_name_original = os.path.basename(user_input)
        output = user_input.replace(user_input.split('.')[-1], 'zip')
        file_name_output = os.path.basename(output)
        zip_ref = zipfile.ZipFile(output, 'w')
        print(f'Compressing {file_name_original} to {file_name_output}...')
        zip_ref.write(user_input, compress_type=zipfile.ZIP_DEFLATED)
        zip_ref.close()

        go_on = input('Continue? [Y/N]').lower()
        compression_complete = True if go_on == 'n' else False
    
    elif input_is_dir:
        #output_name = os.path.split(user_input) #split(r'\\')
        output = Path(user_input) / f"{today_date}.zip"
        files = []
        for file in os.listdir(user_input):
            if not fn.fnmatch(file, '*zip'):
                date_time_index = datetime.fromtimestamp(os.path.getmtime(os.path.join(user_input, file))).strftime("%Y/%m/%d, %H:%M:%S")
                file_size = str(os.stat(os.path.join(user_input, file)).st_size / 10**6) + 'MB'
                files.append((file, date_time_index, file_size))
        files = sorted(files, key=lambda t: t[1], reverse=True) #sort files in directory by timestamp
        files_index = {index+1: name for index, name in enumerate(files)}	
        pp.pprint(files_index)
        
        choice_match = False
        while (not choice_match) : 
            print('-----')
            print('* All files -> 0;\n* Specific files -> corresponding indeces.\n [Input examples: a) 1-4 | b) 1,2,4 | c) 1]')
            print('-----')
            files_to_compress = input('You choose:')
        
            pattern_a, pattern_b, pattern_c = r'[0-9]+[-]+[0-9]+', r'(\d+\,\d+)+(\,\d+)*', r'^\d+$'
            match_a, match_b, match_c = re.match(pattern_a, files_to_compress), re.match(pattern_b, files_to_compress), re.match(pattern_c, files_to_compress)

            if match_a:
                choice_match = True
                first_file, last_file = int(match_a.group().split('-')[0]), int(match_a.group().split('-')[-1])+1
                chosen_files = list(range(first_file, last_file))
            elif match_b:
                choice_match = True
                comma_sep_files = match_b.group().split(',')
                chosen_files = [int(s) for s in comma_sep_files]
            elif match_c:
                if int(files_to_compress) == 0: #all files
                    chosen_files = list(range(1,len(files)+1))
                else:
                    chosen_files = [int(match_c.group())]
                choice_match = True
            else:
                print('Please provide a correct input for indeces.')

        print(chosen_files)
        print(f'Compressing to {output}...')
        zip_ref = zipfile.ZipFile(output, 'w')
        for index in tqdm(chosen_files):
            file_path = os.path.join(user_input, files_index[index][0])
            output = file_path.replace(file_path.split('.')[-1], 'zip')
            zip_ref.write(file_path, compress_type=zipfile.ZIP_DEFLATED)
        zip_ref.close()

        go_on = input('Continue? [Y/N]').lower()
        compression_complete = True if go_on == 'n' else False

    else:
        print('Input error: insert a valid directory or file path!')

'''
file_dir = input('Enter directory of files: ')
print('Directory is: ', file_dir)
zip_file_dir = input('Enter directory to compress: ')
print('New directory is: ', zip_file_dir)

while extraction_complete == 0:
    files = sorted([(file, datetime.fromtimestamp(os.path.getmtime(os.path.join(file_dir, file))).strftime("%Y/%m/%d, %H:%M:%S")) for file in os.listdir(file_dir)], key=lambda t: str(t[1]))
    files_index = {key: value for key, value in enumerate(files)}
    pp.pprint(files_index)
    
    specific_file_index = input('Enter index of specific file to unzip: ')

    specific_file_name = files_index[int(specific_file_index)][0]
    print(specific_file_name)
    specific_file_name_zip = specific_file_name.replace(specific_file_name.split('.')[-1], 'zip')
    specific_file_path = os.path.join(file_dir, specific_file_name)
    specific_file_path_zip = os.path.join(file_dir, specific_file_name_zip)
    
    zip_ref = zipfile.ZipFile(specific_file_path_zip, 'w')

    if (not os.path.exists(specific_file_path_zip)) or (not os.path.isfile(specific_file_path_zip)):
        zip_ref.write(specific_file_path, compress_type=zipfile.ZIP_DEFLATED)
        print(f'...Compressing {specific_file_name} to {specific_file_name_zip}')
        zip_ref.close()
    
    go_on = str.upper(input('Do you want to continue? [Y/N] '))
    extraction_complete = 1 if go_on == 'N' else 0


specific_file_index = ''
'''
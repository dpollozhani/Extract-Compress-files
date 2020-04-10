#!/usr/bin/env python
# coding: utf-8

# In[30]:


import zipfile
import fnmatch as fn
import os
import pprint
import re
from datetime import datetime
from tqdm import tqdm
from pathlib import Path

today_date = datetime.today().date().strftime("%Y%m%d")

pp = pprint.PrettyPrinter()
extraction_complete = False

while not extraction_complete:
	user_input = input('Enter directory or file path (drag and drop): ')
	user_input = user_input.strip('"')

	input_is_file = os.path.isfile(user_input)
	input_is_dir = os.path.isdir(user_input)

	if input_is_file:
		#input is a file -- we extract it to the same directory
		#output = os.path.dirname(user_input)
		output_name = (user_input.split(r'\\')[-1]).replace('.zip', '')
		output = Path(user_input) / f"{output_name}_{today_date}"
		if fn.fnmatch(user_input, '*.zip'): #making sure that input file is a .zip file 
				zip_ref = zipfile.ZipFile(user_input, 'r')
				for member in tqdm(zip_ref.namelist()):	
					print('Unzipping...')
					print(member)
					zip_ref.extract(member, output)
		
		go_on = input('Continue? [Y/N]').lower()
		extraction_complete = True if go_on == 'n' else False

	elif input_is_dir:
		#input is a directory -- we present all .zip files in a folder under this directory  
		files = []
		for file in os.listdir(user_input):
			if fn.fnmatch(file, '*.zip'):
				date_time_index = datetime.fromtimestamp(os.path.getmtime(os.path.join(user_input, file))).strftime("%Y/%m/%d, %H:%M:%S")
				files.append((file, date_time_index))
		files = sorted(files, key=lambda t: t[1], reverse=True) #sort files in directory by timestamp
		files_index = {index+1: name for index, name in enumerate(files)}	
		pp.pprint(files_index)
		
		choice_match = False
		while (not choice_match):
			#User chooses which of the presented files to extract 
			print('-----')
			print('* All files -> 0;\n* Specific files -> corresponding indeces.\n [Input examples: a) 1-4 | b) 1,2,4 | c) 1]')
			print('-----')
			files_to_compress = input('You choose:')

			#Using regular expressions to accept inputs of different forms
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

		#Extracting chosen files into the same directory
		for index in chosen_files:
			output = Path(user_input) / f"Extract_{today_date}"
			file_path = os.path.join(user_input, files_index[index][0])
			zip_ref = zipfile.ZipFile(file_path, 'r')
			for member in tqdm(zip_ref.namelist()):
				print('Unzipping...')
				print(member)
				zip_ref.extract(member, output)

		go_on = input('Continue? [Y/N]').lower()
		extraction_complete = True if go_on == 'n' else False
	else:
		print('Input error: insert a valid directory or file path!')

	
		


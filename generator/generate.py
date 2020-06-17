import sys
import os
from pathlib import Path
sys.path.append("..")

from parser import SolParser
from mapper import EpicMapper 

import pandas as pd

class Generator(object):
	"""A class for generating soil input files for epic simulations."""

	def __init__(self, dir_path, file_name, country_name):
		self._sol_parser = SolParser(dir_path,file_name)
		self._components = self._sol_parser.generate_components()
		self._epic_mapper = EpicMapper(self._components)
		self.country_name = country_name

	def get_country_prefix(self):
		prefix = {
			"tanzania":"TZ"
		}

		return prefix[country_name]

	def epic_components(self):
		self._epic_mapper.gen_epic_components()
		slope_info = self.read_slopes_csv()
		ids_left = []
		for cmp in self._epic_mapper.epic_components:
			old_info = cmp.info
			ID = old_info["ID"][3:]
			query = 'id == "{}"'.format(ID)
			row = slope_info.query(query)

			try:
				old_info["slope"] = round(float(row["slope"]),2)
				old_info["slope_length"] = round(float(row["slope_length"]),2)
			except:
			
				ids_left.append(ID)
				continue
			
			cmp.info = old_info

		if len(ids_left)!=0:
			print("Following ids were left",ids_left)
			print("Total left = ",len(ids_left))
			print("Total = ",len(self._epic_mapper.epic_components))
			sys.exit(0)

		self._epic_mapper.epic_components[5].log()
		
	
		#epic_cmp.log()
		

	def generate_slopes_csv(self):
		root = Path(os.getcwd())
		slope_dir = root/Path("""generator/slope/""")
		os.chdir(slope_dir)
			
		# run the script
		cmd = "Rscript main.R {} > out.txt".format(self.country_name)
	
		os.system(cmd)
		os.system("rm -rf out.txt")

		os.chdir(root)

	def read_slopes_csv(self):
		root = Path(os.getcwd())
		slope_file = root/Path("""generator/slope/slope_files/slope_info.csv""")
		slope_info = pd.read_csv(slope_file)
	
		return slope_info	

	


	def write_components_csv(self):
		fname = "components.csv"
		
		df = pd.DataFrame(columns=['compname',
				'hydgrp','mukey','cokey','albedodry',
				'comppct_r','slope_r','sloper_len_1'])
		
		total = len(self._components)
		
		row_counter = 0
		mukey_counter = 1
		cokey_counter = 56

		for cmp in self._components[1:50]:
			cmp_info = cmp.info

			rows = []
			
			for i in range(6):
				cmp_name = cmp_info['name']
				hydgrp = cmp_info['SLMH'][i]
				row = [cmp_name, hydgrp, mukey_counter, cokey_counter, "NA","NA","NA","NA"]
				df.loc[row_counter] = row
				
				row_counter += 1
			
			mukey_counter += 1
			cokey_counter += 50
			
			total-=1
			print("Left = ",total)

		# write components.csv
		df.to_csv(fname, index=False, encoding='utf-8')	
							

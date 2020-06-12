import sys
sys.path.append("..")

from parser import SolParser
import pandas as pd

class Generator(object):
	"""A class for generating soil input files for epic simulations."""

	def __init__(self, dir_path, file_name):
		self._sol_parser = SolParser(dir_path,file_name)
		self._components = self._sol_parser.generate_components()

	def write_components_csv(self):
		fname = "components.csv"
		
		df = pd.DataFrame(columns=['compname',
				'hydgrp','mukey','cokey','albedodry',
				'comppct_r','slope_r','sloper_len_1'])
		
		total = len(self._components)
		
		row_counter = 0
		mukey_counter = 1
		cokey_counter = 56

		for cmp in self._components:
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
							

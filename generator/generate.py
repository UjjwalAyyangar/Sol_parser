import sys
import os
from pathlib import Path
sys.path.append("..")

from parser import SolParser, CsvParser
from mapper import EpicMapper, CsvEpicMapper 

import pandas as pd

class Generator(object):
	"""A class for generating soil input files for epic simulations."""

	def __init__(self, dir_path, file_name, country_name, ftype="sol"):
		if ftype=="sol":
			self._parser = SolParser(dir_path,file_name)
			self._components = self._parser.generate_components()
			self._epic_mapper = EpicMapper(self._components)
		else: # ftype is csv
			self._parser = CsvParser(dir_path, file_name)
			self._components = self._parser.generate_components()
			self._epic_mapper = CsvEpicMapper(self._components)
		
		self.file_name = file_name	
		self.country_name = country_name
		self.ftype = ftype

	def get_country_prefix(self):
		prefix = {
			"tanzania":"TZ"
		}

		return prefix[country_name]

	def epic_components(self):
		self._epic_mapper.gen_epic_components()
		if self.ftype != "sol":
			return

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

		#self._epic_mapper.epic_components[5].log()
		
	
		#epic_cmp.log()

	def adjust(self, val):
		new_val= "{:0.3f}".format(float(val))
		width = 8
		new_val = f'{new_val:>{width}}'
		return new_val

		# return str(round(float(val),3))

	def add(self, src, trg):
		for s in src:
			trg.append(s)
	
		return trg

	def get_line(self, vals):
		line = ""
		for val in vals:
			if "-" in str(val) or float(val)<0:
				val = "0.000"
			new_val = self.adjust(val)
			line+=new_val

		return line

	def generate_sol_files(self):
		print("Fetching epic components ...")
		self.epic_components()
		print("Generating sol file for each component")
		cmps = self._epic_mapper.epic_components
		total = len(cmps)
		for cmp in cmps:
			print("Left =",total)
			self.generate_sol_file(cmp.info)
			total-=1

	def generate_sol_file(self, cmp):
		if self.ftype !="sol":
			f_id = cmp["ID"].replace(" ","_").replace(",","").lower()
		else:
			f_id = cmp["ID"][3:]	

		file_name = Path("{}.SOL".format(f_id))
		sol_dir = Path("""soil_files""")
		file_dir = sol_dir/self.file_name[:-4]

		file_path = file_dir/file_name
	
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)
	
			
		
		with open(file_path,'w') as f:
			# line 1
			f.write("ID: {}\n".format(f_id))
			
			# line 2
			alb = self.adjust(cmp["SALB"])
			hsg = self.adjust(cmp["HSG"][-1])
			line2 = [alb,hsg,"0.000","0.000","0.000","0.000","5.000","100.000","0.000","0.000"]
			f.write(self.get_line(line2)+"\n")
			
			# line 3
			tsla = self.adjust(len(cmp["HSG"]) + 1)
			line3 = [tsla,"0.000","100.000","0.000","0.000","0.000","0.000","0.014","0.726","0.000"]
			f.write(self.get_line(line3)+"\n")
			
			# line 4 onwards

			epic_vars = ["Z", "BD", "UW", "FC", "SAN","SIL","WN","PH","SMB","WOC","CAC","CEC","ROK",
			"CNDS","PKRZ","RSD","BDD","PSP","SATC","HCL","WPO", "EXCK","ECND","STFR","ST","CPRV","CPRH",
			"WLS","WLM","WLSL","WLSC","WLMC", "WLSLC","WLSLNC","WBMC","WHSC","WHPC",
			"WLSN","WLMN","WBMN","WHSN","WHPN"]

			#print("total vars",len(epic_vars))
			
			inp = [cmp[x] for x in epic_vars]
	
			# print(inp)
			for l in inp:
				f.write(self.get_line(l)+"\n")


			f.write("    275.    200.    150.    140.    130.    120.    110." + "\n")
			f.write("    0.20    0.40    0.50    0.60    0.80    1.00    1.20" + "\n")
			f.write("    .004    .006    .008    .009    .010    .010    .010" + "\n")
			f.write(" ")	

		#print("Finished one soil file")	
		#print(cmp)

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
							

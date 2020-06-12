import sys
import pprint
from .interface import ParserInterface 
from pathlib import Path

class EpicComponent(object):
	"""Data Element which holds information about each component in the sol file
	"""
	@property
	def info(self):
		return self._info

	@info.setter
	def info(self, cmp_info):
		self._info = cmp_info


	def __init__(self,cmp_info = None):
		self._info = cmp_info
	
	def log(self, log_file=None):
		if not log_file:
			pprint.pprint(self._info)
		else:
			pprint.pprint(self._info, log_file)


class SolParser(ParserInterface):
	"""Class which realizes ParserInterface to parse epic sol files
	"""
	
	@property
	def file_name(self):
		return self._file_name

	@file_name.setter
	def file_name(self, file_name):
		self._file_name = file_name


	@property
	def dir_path(self):
		return self._dir_path
	
	@dir_path.setter
	def dir_path(self, dir_path):
		self._dir_path = dir_path	
			

	def __init__(self, dir_path: Path, file_name:str):
		self.file_name = file_name
		self.dir_path = dir_path

		pass

	def extract_text(self):
		full_path = self.dir_path/self.file_name
		with open(full_path,'r') as f:
			return(f.readlines())

	
	def get_component_info(self, content):
		""" Parses information inside a component into a python dictionary object
		
		Args:
			content(list): A list of lines containing the information inside a component
		
		Returns:
			cmp(Component): An object of type Component
		"""
		# each component has 12 lines

		cmp_info = {}

		# Metadata	
		meta = content[0].split(' ')
		cmp_info['name'] = meta[0][1 : len(meta[0])]
			
		# Geographical info	
		geo_info = list(filter(None,content[2].split(' ')))
		cmp_info['country'] = geo_info[1]
		cmp_info['lat'] = geo_info[2]
		cmp_info['lng'] = geo_info[3]
		
		# Measures
		measures = list(filter(None,content[4].split(' ')))
		m_vars = ["SCOM",  "SALB",  "SLU1",  "SLDR",  "SLRO",  "SLNF",  "SLPF",  "SMHB",  "SMPX",  "SMKE"]
		
		for i,var_name in enumerate(m_vars):
			cmp_info[var_name] = measures[i]		

		# Readings
		readings = [] 
		for line in content[6:len(content)]:
			temp = list(filter(None,line.split(' ')))
			readings.append(temp)
		
		readings = [*zip(*readings)]
		var_names = ['SLB' ,'SLMH' ,'SLLL', 'SDUL', 'SSAT',  'SRGF',  'SSKS',  'SBDM',
		  'SLOC',  'SLCL',  'SLSI',  'SLCF',  'SLNI',  'SLHW',  'SLHB',  'SCEC',  'SADC'] 
		
		for i,var_name in enumerate(var_names):
			cmp_info[var_name] = readings[i]

		
		cmp = EpicComponent(cmp_info)
		return (cmp)



	def generate_components(self):
		"""Generates a list of components out of a SOL file

		Returns:
			list of Data Elements of type EpicComponent 
		"""
		
		data = self.extract_text()
		components_list = []
		it = 0 # iteration counter
		total_lines = len(data)

		while it<total_lines:
			line = data[it]
			if line.startswith("*"):
				cmp = self.get_component_info(data[it:it+12])
				# cmp.log()
				components_list.append(cmp)
				it+=12
			else:
				it+=1

		return components_list



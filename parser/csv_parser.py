import sys
import pprint
from .interface import ParserInterface
from pathlib import Path
import pandas as pd


class CsvComponent(object):
	@property
	def info(self):
		return self._info
	
	@info.setter
	def info(self, cmp_info):
		self._info = cmp_info

	def __init__(self, cmp_info=None):
		self._info = cmp_info

	def log(self, log_file=None):
		if not log_file:
			pprint.pprint(self._info)
		else:
			pprint.pprint(self._info, log_file)


class CsvParser(ParserInterface):
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
		self._file_name = file_name
		self._dir_path = dir_path


	def extract_text(self):
		full_path = self._dir_path/self._file_name
		text = pd.read_csv(full_path, skiprows=1)
		#text = text.loc[1:]
		return text # a dataframe

	def get_component_info(self, content):
		cmp_info = {}
		# component name
		cmp_info['name'] = list(content['SOIL_NAME AND LABORATORY_NUMBER'])[0]
		cmp_info['hydgrp'] = list(content['HYDRO GROUP'])
		cmp_info['depth'] = list(content['DEPTH'])
		cmp_info['crs_frac'] = list(content['COARSE FRACTION'])
		cmp_info['sand'] = list(content['SAND'])
		cmp_info['silt'] = list(content['SILT'])
		cmp_info['clay'] = list(content['CLAY'])
		cmp_info['carbon'] = list(content['CARBON'])
		cmp_info['nitrogen']=list(content['NITROGEN'])
		cmp_info['matter'] = list(content['MATTER'])
		cmp_info['ph_h20'] = list(content['pH_H20'])
		cmp_info['sob'] = list(content['SUM_BASES'])
		cmp_info['cac03'] = list(content['CaCO3'])
		cmp_info['cec_soil'] = list(content['CEC_SOIL'])
		cmp_info['bd'] = list(content['BD'])
		cmp_info['wilting_point'] = list(content['theta1500 / wilting point'])
		cmp_info['fc'] = list(content['theta33 / field capacity'])
		cmp_info['b'] = list(content['B'])
		cmp_info['albedo'] = list(content['Albedo'])
		cmp_info['awc'] = list(content['AWC'])
		cmp_info['bd_dry'] = list(content['BD_Dry'])
		cmp_info["ks"] = list(content["KS"])
		cmp = CsvComponent(cmp_info)
		return (cmp)	


	def generate_components(self):
		data = self.extract_text()
		components_list = []
		it = 0 # iteration counter
		total_lines = len(data)
		while it < total_lines:
			#  find number of layers
			lyrs = 1
			next_it = it+1
			while next_it<total_lines and \
				 not isinstance(data.loc[next_it][0], str) :
					lyrs+=1
					next_it+=1
			
			
			cmp = self.get_component_info(data.loc[it:it+lyrs-1])
			components_list.append(cmp)
			it+=lyrs
			
		#	cmp = self.get_component_info(data,i)
		#components_list[-1].log()
		#print(data.tail())
		return components_list



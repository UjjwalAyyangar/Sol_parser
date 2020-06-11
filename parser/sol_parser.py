from .interface import ParserInterface 
from pathlib import Path

class SolParser(ParserInterface):
	
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
			

	def load_data_src(self, dir_path: Path, file_name:str):
		self.file_name = file_name
		self.dir_path = dir_path

		pass

	def extract_text(self):
		full_path = self.dir_path/self.file_name
		with open(full_path,'r') as f:
			return(f.readlines())


	def generate_component(self):
		"""Writes component.csv
		"""
		
		data = self.extract_text()
		print(data)

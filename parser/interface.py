import abc
from pathlib import Path

class ParserInterface(metaclass=abc.ABCMeta):
	@classmethod
	def __subclasshook__(cls, subclass):
		return (hasattr(subclass, 'load_data_src') and
			callable(subclass.load_data_src) and
			hasattr(subclass, 'extract_text') and
			callable(subclass.extract_text))


	@property
	@abc.abstractmethod
	def file_name(self):
		raise NotImplementedError("No file name provided")

	@file_name.setter
	@abc.abstractmethod
	def file_name(self, file_name):
		return
	
	@property
	@abc.abstractmethod
	def dir_path(self):
		return NotImplementedError("No directory path provided")	
	
	@dir_path.setter
	@abc.abstractmethod
	def dir_path(self, dir_path):
		return
	
	@abc.abstractmethod
	def extract_text(self) -> list:
		"""Extract text from the loaded file."""
		
		raise NotImplementedError

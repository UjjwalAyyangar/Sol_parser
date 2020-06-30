import generator as g 
from parser import CsvParser

from pathlib import Path

if __name__ == '__main__':
	file_name ='Patum_Nontaburi.csv'
	dir_path = Path("""/gpfs/data1/cmongp/ujjwal/thailand/epic_sol_parser/""")	
	country_name = "Thailand"
	gen = g.Generator(dir_path, file_name, country_name, "csv")
	#p.generate_components()
	#gen.generate_slopes_csv("tanzania")
	#gen.read_slopes_csv()
	#gen.epic_components()
	
	gen.generate_sol_files()
	# gen.write_components_csv()

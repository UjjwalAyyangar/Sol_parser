import generator as g 
from pathlib import Path

if __name__ == '__main__':
	file_name = 'TZ.SOL'
	dir_path = Path("""/gpfs/data1/cmongp/ujjwal/tanzania/tanzania_soil/""")
	country_name = "tanzania"	
	gen = g.Generator(dir_path, file_name, country_name)
	#gen.generate_slopes_csv("tanzania")
	#gen.read_slopes_csv()
	#gen.epic_components()
	gen.generate_sol_files()
	# gen.write_components_csv()

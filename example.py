import generator as g 
from pathlib import Path

if __name__ == '__main__':
	file_name = 'TZ.SOL'
	dir_path = Path("""/gpfs/data1/cmongp/ujjwal/tanzania/tanzania_soil/""")
	
	gen = g.Generator(dir_path, file_name)
	gen.write_components_csv()

import pprint
import sys

class EpicComponent(object):
	@property 
	def info(self):
		return self._info

	@info.setter
	def info(self, cmp_info):
		
		self._info = cmp_info
		default_vars = ["CAC", "ROK", "BDD", "WN", "CNDS","PKRZ",
			"RSD", "PSP", "HCL", "WPO", "EXCK", "ECND", "STFR",
			"ST", "CPRV", "CPRH", "WLS", "WLM", "WLSL", "WLSC",
			"WLMC", "WLSLC","WLSLNC", "WBMC", "WHSC", "WHPC",
			"WLSN", "WLMN", "WBMN", "WHSN", "WHPN", "OBC"]

		layers = len(cmp_info["HSG"])
		for var in default_vars:
			self._info[var] = ["0.000"]*layers

	def __init__(self, cmp_info = None):
		self._info = cmp_info

	def log(self, log_file= None):
		if not log_file:
			pprint.pprint(self._info)
		else:
			pprint.pprint(self._info, log_file)



class CsvEpicMapper(object):
	@property
	def epic_components(self):
		return self._components

	@epic_components.setter
	def epic_components(self, cmps):
		self._components = cmps


	def __init__(self, csv_components = None):
		self._csv_components = csv_components
		self._components = []


	def calc_hsg(self, slmh):
		try:
			first_letter = slmh[0]
			grps = ["A","B","C","D"]#,"AB","AC","BA","BC","CA","CB","ABC"]
			return (str(grps.index(first_letter)+1))
		except: 
			return 1

	def calc_sand(self, sand):
		return [x*100 for x in sand]	

	def calc_satc(self, ks):
		return [round(float(x),2) for x in ks]

	def calc_depth(self, depth):
		return [x/100 for x in depth]

	def calc_silt(self, silt):
		return [x*100 for x in silt]

	def to_epic(self, csv_component=None):
		c_cmp_info = csv_component.info

		cmp_info = {}
		cmp_info["ID"] = c_cmp_info["name"]
		cmp_info["SALB"] = c_cmp_info["albedo"][0] # recheck
		cmp_info['HSG'] = [self.calc_hsg(slmh) for slmh in c_cmp_info['hydgrp']]
		cmp_info["Z"] =  self.calc_depth(c_cmp_info["depth"])
		cmp_info["BD"] = c_cmp_info["bd"]
		cmp_info["UW"] = c_cmp_info["wilting_point"]
		cmp_info["FC"] = c_cmp_info["fc"]
		cmp_info["SAN"]  = self.calc_sand(c_cmp_info["sand"])
		cmp_info["SIL"] = self.calc_silt(c_cmp_info["silt"])
		cmp_info["PH"] = c_cmp_info['ph_h20']
		cmp_info["CEC"] = c_cmp_info["cec_soil"]
		cmp_info["SMB"] = c_cmp_info["sob"]
		cmp_info["WOC"] = c_cmp_info["carbon"] # recheck
		cmp_info["SATC"] = self.calc_satc(c_cmp_info["ks"])

		cmp = EpicComponent(cmp_info)
		cmp.info = cmp_info
		return (cmp)

	def gen_epic_components(self):
		cmps = []
		for c_cmp in self._csv_components:
			cmps.append(self.to_epic(c_cmp))

		self._components = cmps	




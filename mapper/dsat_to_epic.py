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
			"RSD", "PSP", "HCL", "WPO", "EXCK", "ECND", "SFTR",
			"ST", "CPRV", "CPRH", "WLS", "WLM", "WLSL", "WLSC",
			"WLMC", "WLSLC","WLSLNC", "WBMC", "WHSC", "WHPC",
			"WLSN", "WLMN", "WBMN", "WHSN", "WHPN", "OBC"]

		for var in default_vars:
			self._info[var] = "0"

	
	def __init__(self, cmp_info = None):
		self._info = cmp_info

	def log(self, log_file=None):
		if not log_file:
			pprint.pprint(self._info)
		else:
			pprint.pprint(self._info, log_file)
	

class EpicMapper(object):
	def __init__(self, dssat_components=None):
		self._dssat_components = dssat_components
		self._components =  None

	def calc_sob(self, ph, cec):
		sob_list = []
		
		for ph_val, cec_val in zip(ph,cec):

			ph_change =  ((float(ph_val)-5.9)/5.9)*0.5
			cec_change = ((float(cec_val)-18.1)/18.1)*0.4
			oc_change = ((float(cec_val)-1.9)/1.9)*0.1
		
			af = (ph_change +  cec_change + oc_change)*0.2
		
			sob = round(11.2 + (11.2*af),2)
			sob_list.append(str(sob))

		return sob_list
	
	def calc_hsg(self, slmh):
		grps = ["A","B","C","AB","AC","BA","BC","CA","CB","ABC"]
		return (str(grps.index(slmh)+1))


	def to_epic(self, dssat_component=None):
		d_cmp_info = dssat_component.info
		
		cmp_info = {}
		
		cmp_info['SALB'] = d_cmp_info['SALB']
		cmp_info['HSG'] = [self.calc_hsg(slmh) for slmh in d_cmp_info['SLMH']]
		cmp_info['Z'] = d_cmp_info['SLB']
		cmp_info['BD'] = d_cmp_info['SBDM']
		cmp_info['UW'] = d_cmp_info['SLLL']
		cmp_info['FC'] = d_cmp_info['SDUL']

		cmp_info['SAN'] = [100 - round(float(slcl) + float(slsi),2) \
				 	for slcl, slsi in zip(d_cmp_info['SLCL'], d_cmp_info['SLSI'])]

		cmp_info['SIL'] =  d_cmp_info['SLSI']
		cmp_info['PH'] = d_cmp_info['SLHW']
		cmp_info['CEC'] = d_cmp_info['SCEC']
		cmp_info['SMB'] = self.calc_sob(cmp_info['PH'], cmp_info['CEC'])

		cmp_info['WOC'] = d_cmp_info['SLOC']
		cmp_info['SATC'] = d_cmp_info['SSKS']
		  
		cmp = EpicComponent(cmp_info)
		return (cmp) 
	
	def epic_components(self):
		for dsat_cmp in self.dssat_components:
			self._components.append(to_epic(dsat_cmp))
	
		return self._components


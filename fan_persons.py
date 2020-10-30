
census_divisions={
	"Pacific":["WA","OR","CA","HI","AK"],
	"MountainNorth":["CO", "ID", "MT", "UT", "WY"],
	"MountainSouth":["AZ","NM","NV"],
	"WestNorthCentral":["ND","SD","NE","KS","MN","IA","MO"],
	"WestSouthCentral":["OK","TX","AR","LA"],
	"EastNorthCentral":["WI","MI","IL","IN","OH"],
	"EastSouthCentral":["KY","TN","MS","AL"],
	"SouthAtlantic":["WV","MD","DC","DE","VA","NC","SC","GA","FL"],
	"MiddleAtlantic":["NJ","NY","PA"],
	"NewEngland":["ME","VT","NH","MA","CT","RI"]
}

census_divisions_inv={}
for region,states in census_divisions.items():
	for state in states:
		census_divisions_inv[state]=region


class TempSettings(object):
	def __init__(self,do_not_use,xbrackets,y,heating):
		self.total=do_not_use+sum(y)
		self.xbrackets=xbrackets
		self.y=y
		self.heating=heating

	def query(t):
		p=0.0
		for i,v in enumerate(self.xbrackets):
			if(self.heating and v > t):
				p+=self.y[i]/self.total
			if((not self.heating) and v < t):
				p+=self.y[i]/self.total
		return p

def fan_persons(state,f_temp,humidity,precipitation,timestamp):
	

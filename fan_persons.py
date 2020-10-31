import csv
import numpy as np

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

class FPContext(object):
	def __init__(self,loc="data/recs.csv"):
		with open(loc,'r',newline='') as fo:
			dr=csv.DictReader(fo)
			allrows = list(dr)
			tempdata=np.zeros((28,10))
			labels=list(allrows[0])[1:]

			regions={}

			for region in labels:
				seasons={}
				ri=1
				for season in ["Summer","Winter"]:
					times={}
					for time in ["Day","Night"]:
						xb=[]
						yb=[]
						print(ri)
						print(allrows[ri])
						for _ in range(6):
							xb.append(float(allrows[ri]["TempBegin"]))
							yb.append(float(allrows[ri][region]))
							ri+=1
						dnu=float(allrows[ri][region])
						heating=(season=="Winter")
						ri+=1
						ts=TempSettings(dnu,xb,yb,heating)
						times[time]=ts
					seasons[season]=times
				regions[region]=seasons

			self.regions=regions
			

fp=FPContext()

def ts_to_category(ts):
	season= "Summer" if (ts/24.0 > 120 and ts/24 < 300) else "Winter"
	hr = int(ts) % 24
	tod="Day" (if hr >= 7 and hr < 19) else "Night"
	return season,tod

def fan_persons(state,f_temp,humidity,precipitation,timestamp):
	season,tod=ts_to_category(timestamp)
	region=census_divisions_inv[state]
	return fp.regions[region][season][tod].query(f_temp)



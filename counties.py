import csv
import numpy as np

class AllCounties(object):
	def LLRow(row):
		tests=[("pclat10","pclon10"),("pclat00","pclon00"),("clat10","clon10"),("clat00","clon00")]
		for lats,lons in tests:
			latsv,lonsv=row[lats],row[lons]
			if((latsv != "NA") and (lonsv != "NA")):
				return (float(latsv),float(lonsv))

		raise Exception("No ll found!")

	fips_states=[
	None,"AL","AK",None,"AZ","AR","CA",None,"CO","CT",
	"DE","DC","FL","GA",None,"HI","ID","IL","IN","IA",
	"KS","KY","LA","MN","MD","MA","MI","MN","MS","MO",
	"MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH",
	"OK","OR","PA",None,"RI","SC","SD","TN","TX","UT",
	"VT","VA",None,"WA","WV","WI","WY"]
		
	def __init__(self,loc="raw_data/county_centers.csv"):

		self.counties=[]
		self.centers=[]
		self.states=[]
		with open(loc,'r',newline='') as fo:
			dr=csv.DictReader(fo)
			for row in dr:
				cc=row["fips"]
				state=AllCounties.fips_states[int(cc[:2])]
				latlong=AllCounties.LLRow(row)
				if(state not in ('AK','HI')):
					self.counties.append(cc)
					self.centers.append(latlong)
					self.states.append(state)
			self.centers=np.array(self.centers)

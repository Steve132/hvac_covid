import hashlib
import csv
import zipfile
import sys
import datetime
import io
import re
import numpy as np
import scipy.interpolate


def latlong2gc(latlong):
	latlong[0]+=90.0
	latlong[1]+=180.0
	return (int(10*(latlong[0])),int(10*latlong[1]))



class StationData(object):
	fieldnames=[
		"WBANNO","UTC_DATE","UTC_TIME","LST_DATE","LST_TIME","CRX_VN",
		"LONGITUDE","LATITUDE","T_CALC","T_HR_AVG","T_MAX","T_MIN","P_CALC",
		"SOLARAD","SOLARAD_FLAG","SOLARAD_MAX","SOLARAD_MAX_FLAG","SOLARAD_MIN",
		"SOLARAD_MIN_FLAG","SUR_TEMP_TYPE","SUR_TEMP","SUR_TEMP_FLAG","SUR_TEMP_MAX",
		"SUR_TEMP_MAX_FLAG","SUR_TEMP_MIN","SUR_TEMP_MIN_FLAG","RH_HR_AVG","RH_HR_AVG_FLAG",
		"SOIL_MOISTURE_5","SOIL_MOISTURE_10","SOIL_MOISTURE_20","SOIL_MOISTURE_50",
		"SOIL_MOISTURE_100","SOIL_TEMP_5","SOIL_TEMP_10","SOIL_TEMP_20","SOIL_TEMP_50"
	]
	def __init__(self,fo,filename,interval=1.0):
		mo=re.search("\w+\-\w+\-(\w\w).*$",filename)
		self.state=mo[1]
		ifn=dict(zip(StationData.fieldnames,range(len(StationData.fieldnames))))

		jan12020=datetime.datetime(2020,1,1,tzinfo=datetime.timezone(datetime.timedelta(0)))
		
		timestamps=[]
		values=[]

		with io.TextIOWrapper(fo, encoding='utf-8') as text_file:
			for row in text_file:
				rit=row.split()
				utc_s=rit[ifn["UTC_DATE"]]+rit[ifn["UTC_TIME"]]+"+0000"
				utc=datetime.datetime.strptime(utc_s,"%Y%m%d%H%M%z")
				self.latlong=(float(rit[ifn["LATITUDE"]]),float(rit[ifn["LONGITUDE"]]))
				humidity=float(rit[ifn["RH_HR_AVG"]])
				precipitation=float(rit[ifn["P_CALC"]])
				temperature=float(rit[ifn["T_HR_AVG"]])
				utc_h=(utc-jan12020).total_seconds()/3600.0
				timestamps.append(utc_h)
				values.append((temperature,humidity,precipitation))

		top=max(timestamps)
		newts=np.arange(0.0,max(timestamps),interval,np.float64)
		timestamps=np.array(timestamps)
		values=np.array(values,dtype=np.float64)
		self.timestamps=newts
		interpfunc=scipy.interpolate.interp1d(timestamps,values,axis=0,fill_value="extrapolate")
		self.values=interpfunc(newts)

class AllStations(object):
	def __init__(self,fo,interval_hours=1.0):
		alls=[]
		with zipfile.ZipFile(fo) as zf:
			for nm in zf.namelist():
				if(not zf.getinfo(nm).is_dir()):
					with zf.open(nm) as sdata:
						print("Now loading %s" % (nm))
						sd=StationData(sdata,nm,interval=interval_hours)
						alls.append(sd)
		mnlen=min([len(st.timestamps) for st in alls])
		self.timestamps=alls[0].timestamps[:mnlen]
		self.latlongs=np.array([(st.latlong[0],st.latlong[1]) for st in alls])
		self.states=[st.state for st in alls]
		nTS=len(self.timestamps)
		nLL=len(alls)
		nV=len(alls[0].values[0])
		self.values=np.zeros((nLL,nTS,nV),dtype=np.float64)
		for sti,st in enumerate(alls):
			self.values[sti,:nTS,:]=st.values[:nTS,:]
			

if __name__=='__main__':
	print(sys.argv[1])

	ast=AllStations(sys.argv[1])

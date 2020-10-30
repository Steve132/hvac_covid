import hashlib
import csv
import zipfile
import sys
import datetime
import io
import re
import numpy as np
import scipy.interpolate
import os.path,os
import pickle

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
	def __init__(self,fo,filename):
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


		self.timestamps=np.array(timestamps)
		self.values=np.array(values,dtype=np.float64)
		

class AllStations(object):
	def interp_station(self,st,interval):
		top=max(st.timestamps)
		newts=np.arange(0.0,max(st.timestamps),interval,np.float64)
		timestamps=newts
		interpfunc=scipy.interpolate.interp1d(st.timestamps,st.values,axis=0,fill_value="extrapolate")
		values=interpfunc(newts)
		return timestamps,values

	def load_from_zip(self,fo,interval):
		alls=[]
		with zipfile.ZipFile(fo) as zf:
			for nm in zf.namelist():
				if(not zf.getinfo(nm).is_dir()):
					with zf.open(nm) as sdata:
						print("Now loading %s" % (nm))
						sd=StationData(sdata,nm)
						ts,vs=self.interp_station(sd,interval)
						sd.timestamps=ts
						sd.values=vs
						if(sd.state not in ('AK','HI')):
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
		self.interval_hours=interval

	def load_from_cache(self,pth2,pth,interval_hours):
		if(not os.path.exists(pth2)):
			return False
		if(os.path.getmtime(pth2) < os.path.getmtime(pth)):
			return False

		with np.load(pth2) as npf:
			self.timestamps=npf["timestamps"]
			self.latlongs=npf["latlongs"]
			self.states=npf["states"]
			self.values=npf["values"]
			self.interval_hours=npf["interval_hours"]
			return self.interval_hours == interval_hours
		return False

	def save_to_cache(self,pth2):
		np.savez(pth2,timestamps=self.timestamps,latlongs=self.latlongs,states=self.states,values=self.values,interval_hours=self.interval_hours)

	def __init__(self,fo,interval_hours=1.0):
		if(isinstance(fo,str)):
			pth=fo
			pth2=pth+".npz"
			if(not self.load_from_cache(pth2,pth,interval_hours)):
				self.load_from_zip(pth,interval_hours)
				self.save_to_cache(pth2)
			return
		else:
			self.load_from_zip(fo,interval_hours)

		


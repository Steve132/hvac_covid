import fan_persons
import county_temps
import numpy as np


if __name__=="__main__":
	ct=county_temps.CountyTemperatures()

	for i,ts in enumerate(ct.timestamps):
		v=ct.fetch_values(i)
		fp=np.zeros(v.shape[0])
		for ci,c in enumerate(ct.counties.counties):
			temp=v[ci,0]
			state=ct.counties.states[ci]
			fp[ci]=fan_persons.fan_persons(state,v[ci,0],v[ci,1],v[ci,2],ts)
		print(ts,np.mean(fp))
			

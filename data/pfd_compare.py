import fan_persons
import county_temps



if __name__=="__main__":
	ct=CountyTemperatures()

	for i,ts in enumerate(ct.timestamps):
		v=ct.fetch_values(i)
		fp=np.zeros(v.shape[0])
		for ci,c in enumerate(ct.counties):
			temp=v[ci,0]
			state=ct.states[ci]
			fp[ci]=fan_persons.fan_persons(state,v[ci,0],v[ci,1],v[ci,2],ts)
		print(ts,np.mean(fp))
			

from scipy.spatial import Delaunay,distance
import matplotlib.pyplot as plt
import uscrn
import counties
import numpy as np



def nearest_search(hull_points,test_point,dst):
	
	dv=distance.cdist(hull_points,[test_point],metric=dst)
	return np.argmin(dv)
		 

def get_closest_bary(hull_points,test_points,do_plot=True):
		tri = Delaunay(hull_points)
		if(do_plot):
			plt.triplot(hull_points[:,1], hull_points[:,0], tri.simplices)
			plt.plot(hull_points[:,1], hull_points[:,0], 'o')
			plt.plot(test_points[:,1],test_points[:,0],'+')
			plt.show()

		simp_indices=tri.find_simplex(test_points)
		simplices=tri.simplices[simp_indices]
		bary=np.zeros((test_points.shape[0],3),dtype=np.float64)
		for i,xsi in enumerate(simp_indices):
			if(xsi < 0):
				simplices[i,:]=np.array([nearest_search(hull_points,test_points[i],'euclidean'),0,0])
				bary[i,:]=np.array([1.0,0.0,0.0])
			else:
				T=tri.transform[xsi,:2,:2]
				r=tri.transform[xsi,2,:]
				b=T.dot(np.transpose(test_points[i]-r))
				bary[i,:]=np.array([b[0],b[1],1.0-b.sum()])

		return simplices,bary

if __name__=='__main__':
	ast=uscrn.AllStations("raw_data/hourly_uscrn.zip")
	counties=counties.AllCounties()
	simplices,bary=get_closest_bary(ast.latlongs,counties.centers)	
	

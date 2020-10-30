from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import uscrn
import counties

class Triangulation(object):
	def __init__(self,points,points2=None):
		tri = Delaunay(points)
		plt.triplot(points[:,1], points[:,0], tri.simplices)
		plt.plot(points[:,1], points[:,0], 'o')
		if(points2 is not None):
			plt.plot(points2[:,1],points2[:,0],'+')
		plt.show()
		#tri.simplices[tri.find_simplex(p_valids)]



if __name__=='__main__':
	ast=uscrn.AllStations("raw_data/hourly_uscrn.zip")
	counties=counties.AllCounties()
	#ll=np.array([ll for i,ll in enumerate(ast.latlongs) if ast.states[i] not in ('AK','HI')])
	ll=ast.latlongs
	ztr=Triangulation(ll,counties.centers)

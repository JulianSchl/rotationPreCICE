import numpy as np
import matplotlib.pyplot as plt

class Rotation:
	def makeGrid(self,Lx,Ly,meshDensity):
		self.Lx_min, self.Lx_max = Lx
		self.Ly_min, self.Ly_max = Ly
		
		self.YA, self.XA = np.mgrid[self.Ly_min:self.Ly_max:(meshDensity*1j), self.Lx_min:self.Lx_max:(meshDensity*1j)]
		return np.array((self.XA,self.YA))
	
	def importGrid(self,XA,YA):
		self.XA = XA
		self.YA = YA
		self.Lx_min = np.amin(self.XA)
		self.Lx_max = np.amax(self.XA)
		self.Ly_min = np.amin(self.YA)
		self.Ly_max = np.amax(self.YA)
		return np.array((self.Lx_min,self.Lx_max,self.Ly_min,self.Ly_max))
	
	def centerGrid(self,x0,y0):
		
		#translate
		self.XA = self.XA - x0
		self.YA = self.YA - y0

		return np.array((self.XA,self.YA))
		
	def translateBack(self,x0,y0):

		#translate
		self.XAprim = self.XAprim + x0
		self.YAprim = self.YAprim + y0

		return np.array((self.XAprim,self.YAprim))
	
	def rotate(self, rot_point = None, angle = None):
		
		#center of gravity if no center entered
		x0 = rot_point[0] if (rot_point is not None) else (self.Lx_max+self.Lx_min)/2.
		y0 = rot_point[1] if (rot_point is not None) else (self.Ly_max+self.Ly_min)/2.
		#import ipdb; ipdb.set_trace()
		self.centerGrid(x0,y0)
		
		angle = angle if (angle is not None) else 45.
		ang_rot = np.radians(angle)
		
		RotMatrix = np.array([[np.cos(ang_rot),  -np.sin(ang_rot)],	#counterclockwise
                      		[np.sin(ang_rot), np.cos(ang_rot)]])
		print(str(np.degrees(ang_rot))+"°")
		#rotate
		self.XAprim, self.YAprim = np.einsum('ji, mni -> jmn', RotMatrix, np.dstack([self.XA, self.YA]))
		self.XA, self.YA = self.translateBack(x0,y0)
		return np.array((self.XA, self.YA))
		
		
		
	def rotateCoordinates(self, rot_point = None, angle = None):
		
		#center of gravity if no center entered
		x0 = rot_point[0] if (rot_point is np.ndarray) else (self.Lx_max+self.Lx_min)/2.
		y0 = rot_point[1] if (rot_point is np.ndarray) else (self.Ly_max+self.Ly_min)/2.
		
		self.centerGrid(x0,y0)
		
		angle = angle if (angle is not None) else 45.
		ang_rot = np.radians(angle)
		if ang_rot > 0:
			print("pos")
		else:
			print("neg")
		
		RotMatrix = np.array([[np.cos(ang_rot),  -np.sin(ang_rot)],	#counterclockwise
                      		[np.sin(ang_rot), np.cos(ang_rot)]])
		#print(RotMatrix)
		print(np.degrees(angle))
		#rotate
		self.XAprim, self.YAprim = np.einsum('ji, mni -> jmn', RotMatrix, np.dstack([self.XA, self.YA]))
		self.XA, self.YA = self.translateBack(x0,y0)
		return np.array((self.XA, self.YA))	
		

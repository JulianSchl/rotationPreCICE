from __future__ import division
from matplotlib import pyplot as plt 
import precice
import time
import subprocess
import rotation		#rotation.py
import csvreader	#csvreader.py
import numpy as np
import decimal

configuration_file_name = "../precice-config.xml"
participant_name = "Solid"
mesh_name = ['Solid-Mesh-Hole1','Solid-Mesh-Hole2']
mesh_id = []
patch = []
patch_L = []
transform = []
transform_L = []
vertex_ids = []
read_data_id = []
write_data_id = []
write_data_name = ['Displacement_Hole1','Displacement_Hole2']
read_data_name = ['Force_Hole1','Force_Hole2']
write_data = []
write_data_tmp = []

if not (len(write_data_name) == len(read_data_name)):
	exit("need to define number of patches")
patches = len(write_data_name)


solver_process_index = 0
solver_process_size = 1

direction = True
current_time_step = decimal.Decimal(str(0))
current_time_manipulated = decimal.Decimal(str(0))

zeit = 0.5#10**2
omega = 2*np.pi/zeit
last_rot_angle = 0

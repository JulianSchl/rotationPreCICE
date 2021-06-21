from initialize import * #initialize

interface = precice.Interface(participant_name, configuration_file_name,
                              solver_process_index, solver_process_size)

for i in mesh_name:
	mesh_id.append(interface.get_mesh_id(str(i)))
dimensions = interface.get_dimensions()

for i in range(patches):
	patch.append(rotation.Rotation())
	transform.append(rotation.Rotation())
	XA, YA = np.hsplit(csvreader.csvImport('../fluid/patch' + str(i+1) + '.csv'),2)	#if mesh is in file
	patch_L.append(patch[i].importGrid(XA,YA))
	write_data.append(np.array([XA.flatten(),YA.flatten()]).T)
	
if not (len(write_data) == len(mesh_id)):
	exit("Cannot match mesh to vertices")

read_data = write_data.copy()
vertices = write_data.copy()

for i in range(patches):
	vertex_ids.append(interface.set_mesh_vertices(mesh_id[i],vertices[i]))
	read_data_id.append(interface.get_data_id(read_data_name[i], mesh_id[i]))
	write_data_id.append(interface.get_data_id(write_data_name[i], mesh_id[i]))

dt = interface.initialize()
iteration = -1

while interface.is_coupling_ongoing():

    iteration += 1
    
    if interface.is_action_required(
            precice.action_write_iteration_checkpoint()):
        print("DUMMY: Writing iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_write_iteration_checkpoint())

    if interface.is_read_data_available():
        read_data.clear()
        for i in range(patches):
        	read_data.append(interface.read_block_vector_data(read_data_id[i], vertex_ids[i]))

    print("angle")
    print(str(np.degrees(omega*float(current_time_manipulated))) + '°')
    angle = np.degrees(omega*float(current_time_manipulated))-last_rot_angle
    last_rot_angle = np.degrees(omega*float(current_time_manipulated)).copy()
    
    write_data.clear()
    for i in range(patches):
    	x0 = 0.5
    	y0 = 0.
    	rot_point = np.array((x0,y0))
    	XA, YA = patch[i].rotate(rot_point = rot_point, angle = angle)
    	write_data.append(np.array((XA.flatten(),YA.flatten())).T - vertices[i])

    if interface.is_write_data_required(dt):
    	for i in range(patches):
        	interface.write_block_vector_data(write_data_id[i], vertex_ids[i], write_data[i])
    
    print("DUMMY: Advancing in time")
    dt = interface.advance(dt)
    border = 45
    current_time_step += decimal.Decimal(str(dt))
    if(np.degrees(omega*float(current_time_manipulated)) > border):
    	direction = False
    if(np.degrees(omega*float(current_time_manipulated)) < -border):
    	direction = True
    if direction:
    	current_time_manipulated += decimal.Decimal(str(dt))
    else:
    	current_time_manipulated -= decimal.Decimal(str(dt))
    if interface.is_action_required(
            precice.action_read_iteration_checkpoint()):
        print("DUMMY: Reading iteration checkpoint")
        interface.mark_action_fulfilled(
            precice.action_read_iteration_checkpoint())

interface.finalize()
print("DUMMY: Closing python solver dummy...")

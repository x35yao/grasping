1. First we collected data for 4 objects which then are used to calculate the object_coordinates_wrt_table and  gipper_coordinates_wrt_object.(data_collection)
2. The gipper_coordinates_wrt_object data are then used to plot the mesh in Matlab to visualize the gripper position and orientation wrt objects.(mesh_in_matlab)
3. The gipper_coordinates_wrt_object data are then used to generate coordinates of rays which then are used to generate the depth maps.(depth_map)
4. Grasp_orientation is seperated from what is done above. It analyzes the orientation of the grasps.
5. All the old and messy code is in grasping_archive.zip.(Don't do it like this anymore!)

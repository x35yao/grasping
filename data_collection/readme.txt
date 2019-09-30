1. get_objct_coordinates_wrt_table using data collected in ../raw_data_object
2. Softscrub is different because it is asymmetrical. Therefore we need one specific .py file for it.
3. {}_gripper_wrt_object was generated in such a way that the offset between object mesh and the coordinate origin is compensated
4. When calculating the offset: For the rotation "roll", it is obteined based on observation. For translation "move", it is done by first finding the center of mass of the 
   object by using Findcenter.py. Then using the website "webplotdigitizer" to find the exact coordinates of the center of mass.  

'''
1. This file is used to find out the grasping angle between the z axis of the gripper and the -z axis of the table.
2. Plot the angles as histogram
'''
import numpy as np
from matplotlib import pyplot as plt
import os
import pandas as pd

plt.rcParams.update({'font.size': 22})

def axis_angle_to_rotmat(Rx,Ry,Rz):

    R = np.zeros((3,3),dtype=float)
    a1 = [Rx,Ry,Rz]
    angle = np.linalg.norm(a1)
    a1 = a1/angle

    c = np.cos(angle)
    s = np.sin(angle)
    t = 1.0-c

    R[0,0] = c + a1[0]*a1[0]*t
    R[1,1] = c + a1[1]*a1[1]*t
    R[2,2] = c + a1[2]*a1[2]*t

    tmp1 = a1[0]*a1[1]*t
    tmp2 = a1[2]*s
    R[1,0] = tmp1 + tmp2
    R[0,1] = tmp1 - tmp2

    tmp1 = a1[0]*a1[2]*t
    tmp2 = a1[1]*s
    R[2,0] = tmp1 - tmp2
    R[0,2] = tmp1 + tmp2

    tmp1 = a1[1]*a1[2]*t
    tmp2 = a1[0]*s
    R[2,1] = tmp1 + tmp2
    R[1,2] = tmp1 - tmp2

    return R

#### For all objects ######
# Based on the data we have, get the angle
my_data = pd.read_csv('matched_pos_data_in_table_coordinates.csv', delimiter=',')
doc = open('grasp_orientation.csv','w')
doc.write('Image ID' + ',' + 'Angle' + '\n')
for i in range((len(my_data))):
    axis_ang = my_data.ix[i,'rx':'rz'] * my_data.ix[i,'rot_mag']
    R = axis_angle_to_rotmat(axis_ang[0],axis_ang[1],axis_ang[2])
    z_ang = R[:,2]
    ang = np.arccos(z_ang @ np.array([0,0,-1]))  # The angle between the z axis of the gripper and the -z axis of the table
    doc.write(str(my_data.ix[i,'id']) + ',' + str(ang) + '\n')

# Plot the histogram for all the objects
my_data2 = pd.read_csv('grasp_orientation.csv', sep=',')
plt.hist(np.rad2deg(my_data2.loc[:,'Angle']),bins=300);
plt.xlabel('Grasp orientation(degree)')
plt.ylabel('Frequency')
plt.savefig('histogram_all_objects2.eps', format = 'eps',bbox_inches='tight')

#### For selected objects #####
# Get the data needed for selected object
all_data = pd.read_csv('gripper_pose.tsv',sep = '\t',header=0)
no_obstacle = all_data.loc[all_data.loc[:,'obstacles']==0]
no_obstacle = no_obstacle.set_index('object')

long_vet_object = ['mustard bottle','medium timmies cup','blue jug','chips can','water bottle','soft scrub','soup can',
                   'glue stick','sugar box','wine glass','timmies cup','plastic sleeve','plastic spiral','black flashlight',
                   'flashlight','small green cup','tall plastic tube','small battery pack','rubber ducky','small blue cup',
                   'small orange cup']
target = no_obstacle.loc[long_vet_object,:]
target.to_csv('target_object.csv', sep='\t')

doc = open('target_object_grasp_orientation.csv','w')
doc.write('Image ID' + '\t' + 'Angle' + '\n')
for i in range((len(target))):
    if np.isnan(target.iloc[i,0]):
        pass
    else:
        axis_ang = target.ix[i,'rx':'m1']
        R = axis_angle_to_rotmat(axis_ang[0],axis_ang[1],axis_ang[2])
        z_ang = R[:,2]
        ang = np.arccos(z_ang @ np.array([0,0,-1]))  # angle in radiance
        doc.write(str(target.ix[i,'id']) + '\t' + str(ang) + '\n')
# Plot the histogram for all selcted objects
my_data3 = pd.read_csv('target_object_grasp_orientation.csv',sep = '\t',header=0)
fig = plt.figure()
plt.hist(np.rad2deg(my_data3.loc[:,'Angle']),bins=300);
plt.xlabel('Grasp orientation(degree)')
plt.ylabel('Frequency')
# plt.title('Selected objects')
plt.savefig('histogram_selected_objects.eps', format = 'eps',bbox_inches='tight')

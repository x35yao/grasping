import numpy as np
import os
'''
This file is used to get the coordiantes of the gripper wrt to the object where the offset from the object center to the origin of the coordinates in Matlab is taken into consider.
'''
def csv_to_numpy(directory):
    # converts numerical data in csv file to numpy array
    floats = []
    with open(directory, "r") as f:
        lines = f.readlines()
        for line in lines:
            try:
                k = list(map(float, line.strip().split(",")))
                floats.append(k) # floats will be a list of arrays
            except ValueError:
                pass
    hello = np.array(floats)

    return hello


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


def homogenous_transform(R,vect):

    '''
    :param R: 3x3 matrix
    :param vect: list x,y,z
    :return:Homogenous transformation 4x4 matrix using R and vect
    '''

    H = np.zeros((4,4))
    H[0:3,0:3] = R
    frame_displacement = vect + [1]
    D = np.array(frame_displacement)
    D.shape = (1,4)
    H[:,3] = D
    return H

def inverse_homogenous_transform(H):

    '''
    :param H: Homogenous Transform Matrix
    :return: Inverse Homegenous Transform Matrix
    '''


    R = H[0:3,0:3]
    origin = H[:-1,3]
    origin.shape = (3,1)

    R = R.T
    origin = -R.dot(origin)
    return homogenous_transform(R,list(origin.flatten()))
def final_gripper_position(a):
    # returns the final gripper position from each grasp (time, x,y,z, Rx, Ry, Rz, ...)
    hello = csv_to_numpy(a)
    dist = np.sqrt(hello[:,1]**2+hello[:,2]**2+hello[:,3]**2)
    low_dist = min(dist) # Column with index 3 (4th column) has the z coordinates
    ind = np.where(dist == low_dist) # ind returns a tuple with the index of an element in an array
    row = int(ind[0])

    return hello[row]

transform_for_matlab = {'softscrub':[-33,-0.012652*1000, -0.0018937*1000, 0],
                        'sugarbox':[52,-0.008986*1000, 0.00022655*1000, 0],
                        'foambrick':[22,-0.0099107*1000, -0.0048833*1000, 0],
                        'mustard':[-39,0.0042344*1000, -0.0099301*1000,0 ]}

object = 'mustard'
transform_for_matlab[object]

# directory contains the gripper information wrt to table origin
directory = r"../400 Grasps/raw_data_{}/results".format(object)

# object_transform contains the data collected (coordinates of object from table origin and euler angles to orient table axes to intrinsic object axes).
object_transform = "./{}_coordinates_wrt_table.csv".format(object)

incidence = np.genfromtxt(object_transform, delimiter=',')[1:,:]

fnames = list(sorted(map(int, os.listdir(directory))))


doc = open("{}_gripper_wrt_object.csv".format(object), "w")

doc.write("Image ID" + "," + "x1 (cm)" + "," + "y1 (cm)" +"," + "z1(cm)"
    + "," + "," + "Zx(cm)" + "," + "Zy(cm)" + "," + "Zz(cm)"
    + "," + "," + "Yx(cm)" + "," + "Yy(cm)" + "," + "Yz(cm)"
    + "," + "," + "Xx(cm)" + "," + "Xy(cm)" + "," + "Xz(cm)" + "\n")
for filename in fnames:
    final = final_gripper_position(directory + "/" + str(filename))
    R_gripper = axis_angle_to_rotmat(final[4], final[5], final[6])
    vect_gripper = [final[1], final[2], final[3]]
    H_gripper = homogenous_transform(R_gripper,vect_gripper)

    ind = np.where(incidence[:,0] == filename)
    if len(incidence[ind]) == 0:
        continue
    object_coordinates = incidence[ind].reshape(7,1)
    R_object = axis_angle_to_rotmat(object_coordinates[4], object_coordinates[5], object_coordinates[6])
    vect_object = [object_coordinates[1],object_coordinates[2],object_coordinates[3]]
    H_object = homogenous_transform(R_object,vect_object)
    H_object_inverse = inverse_homogenous_transform(H_object)

    # To make it work in Matlab
    roll = transform_for_matlab[object][0]*np.pi/180
    R_mesh = axis_angle_to_rotmat(0,0,roll)
    vect_mesh = [transform_for_matlab[object][1], transform_for_matlab[object][2], transform_for_matlab[object][3]]
    H_mesh =  homogenous_transform(R_mesh,vect_mesh)

    # Express the origin and axix of the gripper wrt object
    origin = np.array([0,0,0,1])
    z_axix = np.array([0,0,30,1])
    y_axix = np.array([0,30,0,1])
    x_axix = np.array([30,0,0,1])

    transform_origin =  H_mesh @ H_object_inverse @ H_gripper @ origin
    transform_z =  H_mesh @  H_object_inverse @ H_gripper @ z_axix
    transform_y = H_mesh @ H_object_inverse @ H_gripper @ y_axix
    transform_x = H_mesh @  H_object_inverse @ H_gripper @ x_axix
    doc.write(str(filename) + "," + str(transform_origin[0]/10) + "," + str(transform_origin[1]/10) + "," + str(transform_origin[2]/10) + ","
                + "," + str(transform_z[0]/10-transform_origin[0]/10) + "," + str(transform_z[1]/10-transform_origin[1]/10) + "," + str(transform_z[2]/10-transform_origin[2]/10) + ","
                + "," + str(transform_y[0]/10-transform_origin[0]/10) + "," + str(transform_y[1]/10-transform_origin[1]/10) + "," + str(transform_y[2]/10-transform_origin[2]/10) + ","
                + "," + str(transform_x[0]/10-transform_origin[0]/10) + "," + str(transform_x[1]/10-transform_origin[1]/10) + "," + str(transform_x[2]/10-transform_origin[2]/10) + "\n")

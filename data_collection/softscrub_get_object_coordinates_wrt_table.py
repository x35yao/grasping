# object to table
import os
import numpy as np
import csv
import math

def rotation_matrix_from_quaternions(q_vector):

    '''
    :param q_vector: array, containing 4 values representing a unit quaternion that encodes rotation about a frame
    :return: an array of shape 3x3 containing the rotation matrix.
    Takes in array as [qr, qx, qy, qz]
    https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation, s = 1
    '''

    qr, qi, qj, qk = q_vector
    first = [1-2*(qj*qj+qk*qk), 2*(qi*qj-qk*qr),   2*(qi*qk+qj*qr)]
    second= [2*(qi*qj+qk*qr),   1-2*(qi*qi+qk*qk), 2*(qj*qk-qi*qr)]
    third = [2*(qi*qk-qj*qr),   2*(qj*qk+qi*qr),   1-2*(qi*qi+qj*qj)]
    R = np.array([first,second,third])
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

def rotmat_to_axis_angle(R):

    r00 = R[0, 0]
    r01 = R[0, 1]
    r02 = R[0, 2]
    r10 = R[1, 0]
    r11 = R[1, 1]
    r12 = R[1, 2]
    r20 = R[2, 0]
    r21 = R[2, 1]
    r22 = R[2, 2]
    # catch the error
    angle = (r00 + r11 + r22 - 1) / 2
    if angle > 1:
        angle = 0.99999
    elif angle < -1:
        angle = -0.99999
    theta = math.acos(angle)
    sinetheta = math.sin(theta)
    v = (2 * sinetheta) * theta

    cz = ((r10 - r01) / (2 * sinetheta)) * theta
    by = ((r02 - r20) / (2 * sinetheta)) * theta
    ax = ((r21 - r12) / (2 * sinetheta)) * theta

    return ax, by, cz
# object could be 'foambrick','sugarbox','mustard'
object = 'softscrub'
doc = open("{}_coordinates_wrt_table.csv".format(object), "w")
doc.write("Image ID" + "," + "x" + "," + "y" +"," + "z"
          "," + "Rx" + "," + "Ry" +"," + "Rz" "\n")

# Load coordinates of the base of object in marker frame
with open('marker_to_base.csv') as f1:
    rows1 = csv.reader(f1, delimiter=',')
    base_to_marker = {}
    for i, row in enumerate(rows1):
        if i ==0:
            continue
        else:
            base_to_marker[row[0]] = list(map(float,np.array([row[1],row[2],row[3]])))
# Build H1_a, H1_b, H1_c
x1_a = base_to_marker[object][0]
y1_a = base_to_marker[object][1]
z1_a = base_to_marker[object][2]
vect1_a = [x1_a,y1_a,z1_a]
# Rotation
r1a_1 = [1,0,0]
r1a_2 = [0,1,0]
r1a_3 = [0,0,1]
R1_a = [r1a_1,r1a_2,r1a_3]
H1_a = homogenous_transform(R1_a,vect1_a)

x1_b = base_to_marker['softscrub2'][0]
y1_b = base_to_marker['softscrub2'][1]
z1_b = base_to_marker['softscrub2'][2]
vect1_b = [x1_b,y1_b,z1_b]
# Rotation
r1b_1 = [0,1,0]
r1b_2 = [-1,0,0]
r1b_3 = [0,0,1]
R1_b = [r1b_1,r1b_2,r1b_3]
H1_b = homogenous_transform(R1_b,vect1_b)

x1_c = base_to_marker['softscrub3'][0]
y1_c = base_to_marker['softscrub3'][1]
z1_c = base_to_marker['softscrub3'][2]
vect1_c = [x1_c,y1_c,z1_c]
# Rotation
r1c_1 = [0,-1,0]
r1c_2 = [1,0,0]
r1c_3 = [0,0,1]
R1_c = [r1c_1,r1c_2,r1c_3]
H1_c = homogenous_transform(R1_c,vect1_c)
# Load coordinates of marker in NDI frame
object_coordinates = np.genfromtxt('./{}_object_coordinates.csv'.format(object),delimiter = ',')[1:]

# Load coordinates of NDI in table frame
with open('Origin_table.csv') as f3:
    rows3 = csv.reader(f3,delimiter = ',')
    origin_table = {}
    for j, row in enumerate(rows3):
        if j == 0:
            continue
        else:
            origin_table[row[0]] = list(map(float,np.array([row[1],row[2],row[3]])))

# Build Homogeneous transform for flip
r_flip_1 = [-1,0,0]
r_flip_2= [0,-1,0]
r_flip_3 = [0,0,1]
R_flip = [r_flip_1,r_flip_2,r_flip_3]
vect_flip = [2*x1_a,0,0]
H_flip = homogenous_transform(R_flip,vect_flip)

for row in object_coordinates:
    # Coordinates of marker in NDI frame
    q_vector = [row[4],row[5],row[6],row[7]]
    R2 = rotation_matrix_from_quaternions(q_vector)
    vect2 = [row[1],row[2],row[3]]
    H2 = homogenous_transform(R2,vect2)
    # Coordinates of NDI in table frame
    origin_indix = str(int(row[9]))
    vect3_inv = origin_table[origin_indix]
    vect3 = [-vect3_inv[2],-vect3_inv[1],vect3_inv[0]] # NDI in table frame!!
    r3_1 = [0,0,1]
    r3_2 = [0,1,0]
    r3_3 = [-1,0,0]
    R3 = [r3_1,r3_2,r3_3]
    H3 = homogenous_transform(R3,vect3)
    # Check for flip
    if row[8] == 1:
        H = H3 @ H2 @ H_flip @ H1_a
    elif row[8] == 0:
        H = H3 @ H2 @ H1_a
    elif row[8] == 3:
        H = H3 @ H2 @ H1_b
    else:
        H = H3 @ H2 @ H1_c
    R = H[0:3,0:3]
    axis_angle = rotmat_to_axis_angle(R)
    '''
    try:
        axis_angle = rotmat_to_axis_angle(R)
    except:
        print(row[0])
        pass
    '''
    vect = H[:,3]
    doc.write(str(row[0]) + ',' + str(vect[0]) + ',' + str(vect[1]) + ',' + str(vect[2]) + ',' + str(axis_angle[0]) + ',' + str(axis_angle[1]) + ',' + str(axis_angle[2]) + '\n')

from scipy.io import loadmat
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage.filters

'''
Given the depth maps genertaed in matlab, do analysis.
'''
depth_map = np.zeros([50,50])
objects = ['softscrub', 'foambrick','sugarbox','mustard']

sigma = 5
for obj in objects:
    path = r'{}/Depth_map_shifted'.format(obj)
#    path = r'{}/depth_map'.format(obj)
    files = os. listdir(path)
    for file in files:
        x = loadmat(path + '/' + file)
        depth_i = x['A'] * 1000
        if np.count_nonzero(depth_i) == 0: # get rid of the blank depth map
            continue
        else:
            depth_i[np.where(depth_i == 0)] = 300
            depth_i_filtered = scipy.ndimage.filters.gaussian_filter(depth_i,sigma)
            depth_map = np.dstack((depth_i_filtered,depth_map))
            # depth_map = np.dstack((depth_i,depth_map))
depth_map = depth_map[:,:,0:-1]
# depth_max = np.max(depth_map,axis = 2)
# depth_min = np.min(depth_map, axis = 2)
depth_mean = np.mean(depth_map,axis = 2)
depth_std = np.std(depth_map,axis = 2)
#depth_max = np.zeros((50,50))
#depth_min = np.zeros((50,50))
#for i in range(50):
#    for j in range(50):
#        pixel = depth_map[i,j,:]
#        pixel_sorted = sorted(pixel)
#        depth_max[i,j] = pixel_sorted[-4]
#        depth_min[i,j] = pixel_sorted[1]

# plt.imshow(depth_max)
#plt.imshow(depth_min)
plt.rcParams.update({'font.size': 22})
plt.imshow(depth_mean,extent = [-35,35,-35,35])
#plt.imshow(depth_std,extent = [-35,35,-35,35])

cb = plt.colorbar(label = 'Depth(mm)')
#cb.set_label('mm', labelpad=-40, y=1.05, rotation=0)
#plt.savefig('depth_map_std')
plt.xlabel('Angle in x direction(degree)')
plt.ylabel('Angle in y direction(degree)')

#plt.title('Depth map mean')

plt.savefig('depth_map_mean.eps', format = 'eps',bbox_inches='tight')

plt.show()


# plt.imshow(depth_max_filterd)
# plt.imshow(depth_min_filterd)
# plt.imshow(depth_mean_filterd)
# plt.imshow(depth_std_filterd)
#from PIL import Image
#from io import BytesIO
#png2 = Image.open('depth_map_mean.png')
#
## (3) save as TIFF
#png2.save('depth_map_mean.tiff')

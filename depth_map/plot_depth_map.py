from scipy.io import loadmat
import os
from matplotlib import pyplot as plt
import numpy as np
import scipy.ndimage.filters
# objects = ['softscrub', 'foambrick','sugarbox','mustard']

# for obj in objects:
# obj could be 'foambrick', 'mustard','softscrub','sugarbox'
obj = 'foambrick'
path = r'{}/depth_map'.format(obj)
#path = r'{}/Depth_map_shifted'.format(obj)
files = os. listdir(path)
sigma = 10

ind = np.zeros((len(files),2))
plt.figure(figsize = (10,10),dpi = 100)
for i,file in enumerate(files):
    # print(file)

    x = loadmat(path + '/' + file)
    depth_map= x['A']*1000
    depth_map[np.where(depth_map== 0)] = 300
    depth_map_filtered = scipy.ndimage.filters.gaussian_filter(depth_map,sigma,mode = 'constant',cval = 300)
    # plt.subplot(10,2,1)
    # plt.subplot(1,2,1)
    # plt.imshow(depth_map)
    # plt.colorbar()
    # plt.subplot(1,2,2)
#    plt.imshow(depth_map_filtered)
#    print(file)
#    plt.show()
    # plt.colorbar()
    #
    # plt.show()
    plt.subplot(10,10,i+1)
    plt.imshow(depth_map_filtered)
    plt.axis('off')
    plt.title(file, fontsize = 'x-small')
#    plt.colorbar()
#    depth_map_filtered_min = depth_map_filtered.min()
#    ind_i = np.where(depth_map_filtered == depth_map_filtered_min)
#    ind[i,0] = ind_i[0][0]
#    ind[i,1] += ind_i[1][0]
#print(ind.mean(axis = 0))
plt.tight_layout()
#plt.savefig('{}_depth_map_shifted'.format(obj))
plt.savefig('{}_depth_map'.format(obj))

# bad ones
#foambrick :446118, 897012, 422104

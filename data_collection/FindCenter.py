import imageio
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import ndimage
from scipy import stats
import statistics
import numpy as np


img = imageio.imread('sugarbox.jpg',pilmode='L')
threshold = 100
img_bin = img < threshold
s = ndimage.generate_binary_structure(2,2)
lbl, num_features = ndimage.label(img_bin, structure = s)
n = np.prod(lbl.shape)
lbl_flat = np.reshape(lbl,(n,))
lbl_flat_reduction = lbl_flat[ lbl_flat != 0 ]
[a,b] = ndimage.center_of_mass(lbl,labels=86)
plt.imshow(img)
plt.scatter(b, a, c='red', marker='o')
plt.show()

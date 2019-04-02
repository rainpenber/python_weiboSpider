import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)

# XY value
# X = np.arange(-4,4,0.25)
# Y = np.arange(-4,4,0.25)
# X,Y = np.meshgrid(X,Y)
# R = np.sqrt(X**2 + Y**2)
# # height Value
# Z = np.sin(R)
# point_dict = ()
with open("result/result.txt", "r") as zombie_sample:
    for line in zombie_sample.readlines():
        if line == '':
            break
        try:
            #split by space
            #['1111111 123 12 23'] → ['1111111','123','12','23']
            p = list(filter(None,line.split(" ")))

            # get label and value
            # p_label = p_tmp[0]
            # p_value = [p_tmp[1],p_tmp[2],p_tmp[3]]
            ax.scatter(int(p[1]),int(p[2]),int(p[3]),p[0],s = 1, cmap='Blue')

        except Exception as e:
            print(e)


plt.show()
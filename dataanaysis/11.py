import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams.update({'font.size': 14})
plt.rcParams['axes.unicode_minus'] = False
Np = 11
from sklearn.svm import SVR

plt.rcParams['font.sans-serif'] = ['Times New Roman']
# plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams.update({'font.size': 14})
plt.rcParams['axes.unicode_minus'] = False
# from matplotlib.font_manager import FontProperties
# fontst = FontProperties(fname=r"C:\\Windows\\Fonts\\STSong.ttf", size=16)
# fontst2 = FontProperties(fname=r"C:\\Windows\\Fonts\\STSong.ttf", size=12)

X_in_1227 = np.loadtxt("./x_in.txt")
y_in_u = np.loadtxt("./y_in_u.txt")
y_in_v = np.loadtxt("./y_in_v.txt")
y_in_r = np.loadtxt("./y_in_r.txt")
X_in_1227[:, 2] = X_in_1227[:, 2] * 100
y_in_r = y_in_r * 100
# print("svrregU")
# svrregU = SVR(kernel="rbf"
#               , gamma=0.1
#               , epsilon=0.01
#               # ,gamma=0.068
#               , C=1000000
#               , cache_size=50000
#               )
#
# svrregU.fit(X_in_1227, y_in_u)
# print("svrregV")
# svrregV = SVR(kernel="rbf"
#               , gamma=0.1
#               , epsilon=0.01
#               # ,gamma=0.068
#               , C=1000000
#               , cache_size=50000
#               )
#
# svrregV.fit(X_in_1227, y_in_v)

svrregR = SVR(kernel="rbf"
              , gamma=0.1
              , epsilon=0.01
              # ,gamma=0.068
              , C=1000000
              , cache_size=500000
              )

svrregR.fit(X_in_1227, y_in_r)

# y = svrregU.predict(X_in_1227)
# plt.plot(y)
# plt.plot(y_in_u, ls='--')
# plt.show()
# y = svrregV.predict(X_in_1227)
# plt.plot(y)
# plt.plot(y_in_v,ls='--')
# plt.show()
#
y = svrregR.predict(X_in_1227)
plt.plot(y)
plt.plot(y_in_r,ls='--')
plt.show()
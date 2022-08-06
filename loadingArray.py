import numpy as np
import matplotlib.pyplot as plt


def rsq(p, x, y):
    yfit = np.polyval(p, x)
    yresid = y - yfit
    SSresid = np.sum(np.square(yresid))
    SStotal = (len(y) - 1) * np.var(y)
    rsq = 1 - SSresid/SStotal
    return rsq


# plt.rcParams.update({'font.size': 16})
loadedArr = "100x100_CorrectDistanceEnergyDataSet.npy"

# maxDistance = 32080000
# minDistance = 8640000
maxDistance = 207360000000  # 207,360,000,000 m
minDistance = 8640000000  # 8,640,000,000 m

maxVelocity = 80000
minVelocity = 20000

velocitySamples = 100
distanceSamples = 100
# velocitySamples = 5
# distanceSamples = 5

velocityArr = np.linspace(minVelocity, maxVelocity, velocitySamples)
distanceArr = np.linspace(-maxDistance, -minDistance, distanceSamples)
Z = np.load(loadedArr)

# ax = plt.axes(projection='3d')
X, Y = np.meshgrid(velocityArr, distanceArr)

# fg = ax.plot_surface(X, Y, Z, cmap='viridis')
#
# ax.set_title("Min deltaV for no collision")
# ax.set_xlabel("velocity")
# ax.set_ylabel("distance")
# ax.set_zlabel("min vertical velocity")
#
# plt.colorbar(fg)
# plt.show()
#
# # Z = np.load(loadedArr)
# # for i in range(100):
# #     for j in range(100):
# #         if Z[i][j] > 10000:
# #             Z[i][j] = Z[i-1][j-1]
# #
# # np.save("100x100_CorrectDistanceVelocityDataSet3.1", Z)

# maxEnergyTransfer = 3.138 * 10**16
# counter = 0
# diffCounter = 0
# arr = np.full(shape=Z.shape, fill_value=False, dtype=bool)

# for i in range(velocitySamples):
#     for j in range(distanceSamples):
#         if Z[i][j] < maxEnergyTransfer:
#             counter += 1
#             diffCounter += maxEnergyTransfer-Z[i][j]
#             arr[i][j] = True


# arr = Z - maxEnergyTransfer
# plt.pcolor(X, Y, Z, cmap='plasma')
# plt.show()

# print(counter / (velocitySamples * distanceSamples) * 100, " %")
# print((diffCounter / counter) / maxEnergyTransfer * 100, "%")
# print(maxEnergyTransfer / Z[99][99] * 100, '%')

# pos = 99
# pos2 = 0
# deg = 5
# y2 = Z[pos]
# y4 = Z[pos2]
#
# x = velocityArr
#
# p2 = np.polyfit(x=x, y=y2, deg=deg)
# f2 = np.poly1d(p2)
# p4 = np.polyfit(x=x, y=y4, deg=deg)
# f4 = np.poly1d(p4)
#
# plt.scatter(x, y2, s=3, c='g')
# plt.plot(x, f2(velocityArr))
# # plt.scatter(x, y4, s=3, c='b')
# # plt.plot(x, f4(velocityArr), c='m')
#
# # print(f2(20000))
# # print(Z[99][0])
# # print(f4(20000))
# # print(Z[0][0])
#
# rsq2 = rsq(p2, x, y2)
# rsq4 = rsq(p4, x, y4)
#
# # print(rsq2)
# # print(rsq4)
# # print((1-rsq2/rsq4) * 100, "%")
#
# # counter = 0
# # counter2 = 0
# # for x in range(len(distanceArr)):
# #     for y in range(len(velocityArr)):
# #         if Z[x, y] > (6.276 * 10**9):
# #             counter += 1
# #             if x >= 89:
# #                 counter2 += 1
# # print(counter2 / counter * 100)
#
# plt.suptitle("Energy transfer with minimum initial distance", fontsize=18)
# plt.title('R-Squared: ' + str(rsq2), fontsize=13)
# plt.xlabel('Initial Horizontal Velocity (m.s^-1)', fontsize=14)
# plt.ylabel('Change in Energy (J)', fontsize=14)
# plt.tick_params(axis='both', labelsize='12', labelrotation=0)

pos = 0
pos2 = 99
deg = 25
y1 = Z[:, pos]
y3 = Z[:, pos2]

x = distanceArr
for i in range(100, 0, -1):
    try:
        print("checking")
        p1 = np.polyfit(x=x, y=y1, deg=i)
        deg = i
        print(i)
        break
    except:
        continue
print("tuvieja")
print(deg)

p1 = np.polyfit(x=x, y=y1, deg=deg)
f1 = np.poly1d(p1)
p3 = np.polyfit(x=x, y=y3, deg=deg)
f3 = np.poly1d(p3)

plt.scatter(x, y3, s=3, c='g')
plt.plot(x, f3(x))
plt.scatter(x, y1, s=3, c='b')
plt.plot(x, f1(x), c='m')

# plt.suptitle("Energy transfer with minimum initial distance", fontsize=18)
# plt.title('R-Squared: ' + str(rsq2), fontsize=13)
plt.xlabel('Initial Distance (m)', fontsize=14)
plt.ylabel('Change in Energy (J)', fontsize=14)
plt.tick_params(axis='both', labelsize='12', labelrotation=0)
plt.legend(["80kms^-1 scatter", "80kms^-1 trend", "20kms^-1 scatter", "20kms^-1 trend"], fontsize=14)

plt.show()

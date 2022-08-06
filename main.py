# 1 unit = 1 meter
# normal tick = 1 second (may change according to the time multiplier)
# so that 1 unit of velocity = 1 m/s

from GravitySimulation import \
    Universe, \
    Body, \
    BodyParameters, \
    MinVerticalVelocityParameters

import numpy as np
# import matplotlib.pyplot as plt

gravitationalConstant = 6.67 * 10 ** -11
timeMultiplier = 1800

universe = Universe(timeMultiplier=timeMultiplier)

earthDiameter = 12742000
earthDensity = 5513

asteroidDiameter = 10000
asteroidDensity = 2250

earthParameters = BodyParameters(
    universe,
    diameter=earthDiameter,
    density=earthDensity,
    # position=(0, 0),
    # velocity=(0, 0)
)
earth = Body(
    earthParameters
)


asteroidParameters = BodyParameters(
    universe,
    diameter=asteroidDiameter,
    density=asteroidDensity,
    # position=(-10000000, 0),
    # velocity=(10000, 0)
)
asteroid = Body(
    asteroidParameters
)

print(earth.radius)
print(asteroid.radius)

minVerticalVelocityParameters = MinVerticalVelocityParameters(
    earth=earth,
    asteroid=asteroid,
    gravitationalConstant=gravitationalConstant,
    # maxVelocityChanges=100,
    maxVelocityChanges=100,
    # maxCollisionChecks=10 * timeMultiplier,
    maxVerticalVelocity=10000
)

# maxX = -32080000  | minX = -8640000
# maxV = 80000 | minV = 20000

# maxDistance = 32080000  # 3,208,000,000
# minDistance = 8640000  # 8,640,000,000

maxDistance = 207360000000  # 207,360,000,000 m
minDistance = 8640000000  # 8,640,000,000 m

maxVelocity = 80000
minVelocity = 20000

# velocitySamples = 100
# distanceSamples = 100
velocitySamples = 100
distanceSamples = 100

velocityArr = np.linspace(minVelocity, maxVelocity, velocitySamples)
distanceArr = np.linspace(-maxDistance, -minDistance, distanceSamples)
Z = universe.runSimulation(
    velocityArr=velocityArr,
    distanceArr=distanceArr,
    minVerticalVelocityParameters=minVerticalVelocityParameters
)

np.save("100x100_CorrectDistanceVelocityDataSet4.0", Z)

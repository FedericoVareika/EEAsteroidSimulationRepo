import math
import numpy as np

import time


class BodyParameters:
    def __init__(
            self,
            universe,
            diameter,
            density,
            # position=(0, 0),
            # velocity=(0, 0),
    ):
        self.universe = universe
        self.diameter = diameter
        self.density = density
        self.position = (0, 0)
        self.velocity = (0, 0)


class Body:
    def __init__(
            self,
            parameters: BodyParameters,
    ):
        super().__init__()

        # self.mass = parameters.mass
        self.diameter = parameters.diameter
        self.density = parameters.density

        self.position = parameters.position
        self.originalPosition = parameters.position
        self.previousPosition = parameters.position
        self.previousPreviousPosition = parameters.position

        self.V_0 = parameters.velocity
        self.deltaV = (0, 0)

        self.velocity = parameters.velocity
        self.previousVelocity = parameters.velocity

        # self.volume = self.mass / self.density
        # self.radius = (3 * self.volume / (4 * math.pi)) ** (1 / 3)

        self.radius = self.diameter / 2
        self.volume = (4 * np.pi * self.radius) / 3
        self.mass = self.volume * self.density

        parameters.universe.addBody(self)

    def move(self, timeMultiplier):  # , timeMultiplier
        self.previousPreviousPosition = self.previousPosition
        self.previousPosition = self.position

        deltaX = (
            (self.V_0[0] + self.deltaV[0]) * timeMultiplier,
            (self.V_0[1] + self.deltaV[1]) * timeMultiplier

        )

        # self.position = (
        #     self.position[0] + (self.V_0[0] + self.deltaV[0]),
        #     self.position[1] + (self.V_0[1] + self.deltaV[1])
        # )

        self.position = (
            self.position[0] + deltaX[0],
            self.position[1] + deltaX[1]
        )

        self.velocity = (
            self.V_0[0] + self.deltaV[0],
            self.V_0[1] + self.deltaV[1]
        )

    def distance(self, args):
        if isinstance(args, Body):  # receive a Body
            distance = math.sqrt(
                (args.position[0] - self.position[0]) ** 2 +
                (args.position[1] - self.position[1]) ** 2
            )
        else:  # receive a coordinate
            distance = math.sqrt(
                (args[0] - self.position[0]) ** 2 +
                (args[1] - self.position[1]) ** 2
            )
        return distance

    def resetPosition(self, deltaVelocity, deltaPosition):
        self.originalPosition = (
            self.originalPosition[0] + deltaPosition[0],
            self.originalPosition[1] + deltaPosition[1]
        )
        self.position = self.originalPosition
        self.previousPosition = self.position
        self.previousPreviousPosition = self.position

        self.velocity = (
            self.previousVelocity[0] + deltaVelocity[0],
            self.previousVelocity[1] + deltaVelocity[1]
        )

        self.previousVelocity = self.velocity
        self.deltaV = (0, 0)
        self.V_0 = self.velocity

    def angleTo(self, args):
        if isinstance(args, tuple):
            angle = np.arctan2(
                args[1] - self.position[1],
                args[0] - self.position[0]
            )
        elif isinstance(args, Body):
            angle = np.arctan2(
                args.position[1] - self.position[1],
                args.position[0] - self.position[0]
            )
        return angle


class MinVerticalVelocityParameters:
    def __init__(
            self,
            earth: Body,
            asteroid: Body,
            gravitationalConstant,
            maxVelocityChanges,
            # maxCollisionChecks,
            maxVerticalVelocity
    ):
        self.earth = earth
        self.asteroid = asteroid
        self.gravitationalConstant = gravitationalConstant
        self.maxVelocityChanges = maxVelocityChanges
        # self.maxCollisionChecks = maxCollisionChecks
        self.maxVerticalVelocity = maxVerticalVelocity


class Universe:
    def __init__(
            self,
            timeMultiplier
    ):

        self.timeMultiplier = timeMultiplier
        self.bodies = []

    def addBody(self, body):
        self.bodies.append(body)

    def removeBody(self, body):
        body.clear()
        self.bodies.remove(body)

    def updateAll(self):
        for body in self.bodies:
            body.move(timeMultiplier=self.timeMultiplier)

    def applyGravity(
            self,
            earth: Body,
            asteroid: Body,
            gravitationalConstant
    ):
        # force = np.divide(np.multiply(gravitationalConstant, earth.mass, asteroid.mass), np.power(earth.distance(asteroid), 2))
        force = (gravitationalConstant * earth.mass * asteroid.mass) / np.power(earth.distance(asteroid), 2)
        angle = earth.angleTo(asteroid)
        reverse = 1
        for body in self.bodies:
            acceleration = force / body.mass
            acc_x = acceleration * np.cos(angle)
            acc_y = acceleration * np.sin(angle)

            # body.deltaV = (
            #     body.deltaV[0] + (reverse * acc_x * self.timeMultiplier),
            #     body.deltaV[1] + (reverse * acc_y * self.timeMultiplier)
            # )
            body.deltaV = (
                body.deltaV[0] + (reverse * acc_x),
                body.deltaV[1] + (reverse * acc_y)
            )
            reverse = -1

    # def detectCollision(self,
    #                     earth: Body,
    #                     asteroid: Body,
    #                     maxChecks
    #                     ):
    #     # print(earth.distance(asteroid.position) - earth.distance(asteroid.previousPosition))
    #     if earth.distance(asteroid.position) < (earth.radius + asteroid.radius):
    #         return 1  # collision
    #     elif earth.distance(asteroid.previousPosition) < earth.distance(asteroid.position):
    #         if self.collisionLogic(
    #             earth,
    #             asteroid,
    #             closestPosition=asteroid.previousPosition,
    #             farthestPosition=asteroid.position,
    #             maxChecks=maxChecks
    #         ) or self.collisionLogic(
    #             earth,
    #             asteroid,
    #             closestPosition=asteroid.previousPreviousPosition,
    #             farthestPosition=asteroid.previousPosition,
    #             maxChecks=maxChecks
    #         ):
    #             print(asteroid.distance(asteroid.previousPosition))  # / self.timeMultiplier
    #             return 1  # collision
    #         print(asteroid.distance(asteroid.previousPosition))
    #         return 0  # no collision and stop
    #     return -1  # no collision but continue

    def getMinVerticalVelocity(
            self,
            parameters: MinVerticalVelocityParameters,
    ):
        maxVerticalVelocity = parameters.maxVerticalVelocity

        timeCounter = 0
        changingVelocityCounter = 0

        minVerticalVelocity = 0

        start = time.time()
        while changingVelocityCounter < parameters.maxVelocityChanges:
            # repeat this the amount of instances one chooses to run the program through

            # start = timeit.timeit()
            # collision = self.detectCollision(parameters.earth, parameters.asteroid)
            # end = timeit.timeit()
            # print("collision time: ---%s seconds---" % (end-start))

            collision = detectCollision(earth=parameters.earth, asteroid=parameters.asteroid)  # , parameters.maxCollisionChecks

            if collision == 1:
                # print("collision")

                parameters.earth.resetPosition(deltaVelocity=(0, 0), deltaPosition=(0, 0))
                # reset position of earth

                deltaVerticalVelocity = (maxVerticalVelocity + minVerticalVelocity) / 2 - parameters.asteroid.previousVelocity[1]
                # find the middle between max and min then find the difference between that and the last velocity

                minVerticalVelocity = parameters.asteroid.previousVelocity[1]
                # since last velocity hit, it is now set as min vertical velocity
                parameters.asteroid.resetPosition(deltaVelocity=(0, deltaVerticalVelocity), deltaPosition=(0, 0))
                # reset velocity asteroid and change it

                changingVelocityCounter += 1
            elif collision == 0:
                # print("no collision")

                parameters.earth.resetPosition(deltaVelocity=(0, 0), deltaPosition=(0, 0))
                # reset position of earth

                deltaVerticalVelocity = (maxVerticalVelocity + minVerticalVelocity) / 2 - parameters.asteroid.previousVelocity[1]
                # find the middle between max and min then find the difference between that and the last velocity

                maxVerticalVelocity = parameters.asteroid.previousVelocity[1]
                # since last velocity didn't hit, it is now the max vertical velocity
                parameters.asteroid.resetPosition(deltaVelocity=(0, deltaVerticalVelocity), deltaPosition=(0, 0))
                # reset velocity asteroid and change it

                changingVelocityCounter += 1

            self.applyGravity(
                parameters.earth,
                parameters.asteroid,
                parameters.gravitationalConstant
            )
            self.updateAll()
        end = time.time()
        print("---%s seconds---" % (end-start))

        # print(maxVerticalVelocity)
        return maxVerticalVelocity

    def runSimulation(
            self,
            velocityArr,
            distanceArr,
            minVerticalVelocityParameters: MinVerticalVelocityParameters,
    ):
        Z = np.empty((len(velocityArr), len(distanceArr)), float)

        x = 0
        y = 0
        for distance in distanceArr:
            for velocity in velocityArr:
                minVerticalVelocityParameters.asteroid.previousVelocity = (velocity, 0)
                minVerticalVelocityParameters.asteroid.originalPosition = (distance, 0)

                Z[y][x] = self.getMinVerticalVelocity(
                    parameters=minVerticalVelocityParameters
                )
                print(Z[y][x])
                x += 1
                Counter = y * len(distanceArr) + x
                print("Counter: ", Counter, " -- ", 100 * Counter / (len(velocityArr) * len(distanceArr)), "%")
            x = 0
            y += 1
        return Z


# def collisionLogic(
#         self,
#         earth: Body,
#         asteroid: Body,
#         closestPosition,
#         farthestPosition,
#         maxChecks
# ):
#     counter = 0
#     while counter < maxChecks:
#         middlePosition = [
#             (closestPosition[0] + farthestPosition[0]) / 2,
#             (closestPosition[1] + farthestPosition[1]) / 2
#         ]
#         if earth.distance(middlePosition) < (earth.radius + asteroid.radius) / 2:
#             counter = maxChecks
#             return True
#         else:
#             if earth.distance(closestPosition) > earth.distance(middlePosition):
#                 closestPosition = middlePosition
#                 # if middle position is closer to closest position, make middle the new closest
#             else:
#                 farthestPosition = middlePosition
#             counter += 1
#     return False


def equationOfLine(
        p1=(0, 0),
        p2=(0, 0)
):
    division = (p2[1] - p1[1]) / (p2[0] - p1[0])
    a = division
    b = -1
    c = division * p1[0] + p1[1]
    # print(p1, p2)
    # print("a: ", a, "b: ", b, "c: ", c)
    return a, b, c


def distanceFromPointToStraightLine(
        eq=(0, 0, 0),
        point=(0, 0)
):
    num = (eq[0] * point[0]) + (eq[1] * point[1]) + eq[2]
    den = np.sqrt(np.square(eq[0]) + np.square(eq[1]))
    distance = np.abs(num) / den
    # print("point: ", point)
    # print(distance)
    return distance


def detectCollision(
        earth: Body,
        asteroid: Body
):
    minDistance = earth.radius + asteroid.radius
    if earth.distance(asteroid.position) < minDistance:
        # print("Direct collision")
        return 1  # collision
    elif earth.distance(asteroid.previousPosition) < earth.distance(asteroid.position):
        # print("Current Di: ", earth.distance(asteroid.position))
        # print("Previous D: ", earth.distance(asteroid.previousPosition))
        # print(earth.distance(asteroid.position) - earth.distance(asteroid.previousPosition))
        if distanceFromPointToStraightLine(
            eq=equationOfLine(
                p1=asteroid.previousPosition,
                p2=asteroid.position
            ),
            point=earth.position
        ) < minDistance or distanceFromPointToStraightLine(
            eq=equationOfLine(
                p1=asteroid.previousPreviousPosition,
                p2=asteroid.previousPosition
            ),
            point=earth.previousPosition
        ) < minDistance:
            # print("non-direct collision")
            return 1
        # print("No collision")
        return 0
    return -1

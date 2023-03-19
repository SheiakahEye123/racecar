import pygame
import numpy as np
from main import CarRacing
import matplotlib.pyplot as plt
import cv2


env = CarRacing(render_mode="human")
# rgb_env = CarRacing(render_mode="rgb_array")

quit = False

record = []
drecord = []
precord = []

a = np.array([0.0, 0.0, 0.0])

def screenCheck(render,y):
    ledge = 0
    redge = 0
    green = 160
    for pixel in range(len(render[y])):
        if 0 < pixel < len(render[y]) - 1:
            if render[y][pixel - 1][1] < green < render[y][pixel][1]:
                ledge = pixel
                continue
            if render[y][pixel][1] > green > render[y][pixel + 1][1]:
                redge = pixel
                continue
    if ledge == 0 and redge == 0:
        for pixel in range(len(render[-y])):
            if 0 < pixel < len(render[-y]) - 1:
                if render[-y][pixel - 1][1] < green < render[-y][pixel][1]:
                    ledge = pixel
                    continue
                if render[-y][pixel][1] > green > render[-y][pixel + 1][1]:
                    redge = pixel
                    continue
    return (ledge+redge) / 2


while not quit:
    env.reset()
    total_reward = 0.0
    steps = 0
    restart = False
    while True:
        # register_input()
        s, r, terminated, truncated, info = env.step(a)
        p = (screenCheck(s,30) - int(s.shape[1] / 2)) / 40
        d = 0
        if len(precord) > 10:
            d = (precord[-10] - p) / 2

        drecord.append(d)
        precord.append(p)

        a[0] = p - d
        record.append(a[0])
        a[1] = 0.1
        plt.xlim([0,50])
        plt.ylim([-1,1])
        plt.plot(range(len(drecord[-50:-1])), drecord[-50:-1], "r",label="D")
        plt.plot(range(len(precord[-50:-1])), precord[-50:-1], "g",label="PI")
        plt.plot(range(len(record[-50:-1])),record[-50:-1],"b",label="final")
        plt.legend()
        plt.pause(0.0000000000000000000000000000000000000000000000000000000000000001)
        plt.clf()


        cv2.imshow("s",s)
        cv2.waitKey(1)

        total_reward += r
        if steps % 200 == 0 or terminated or truncated:
            print("\naction " + str([f"{x:+0.2f}" for x in a]))
            print(f"step {steps} total_reward {total_reward:+0.2f}")
        steps += 1
        if terminated or truncated or restart or quit:
            break
env.close()
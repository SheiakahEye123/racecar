import pygame
import numpy as np
from main import CarRacing
import matplotlib.pyplot as plt


env = CarRacing(render_mode="rgb_array")

quit = False

a = np.array([0.0, 0.0, 0.0])

def screenCheck(y):
    render = env.render()
    plt.imshow(render)
    plt.pause(0.0000000000000000000000000000000000001)
    ledge = 0
    redge = 0
    green = 160
    for pixel in range(len(render[y])):
            if 0 < pixel < len(render[y]) - 1:
                if render[y][pixel - 1][1] < green and green < render[y][pixel][1]:
                    ledge = pixel
                    continue
                if render[y][pixel][1] > green and green > render[y][pixel + 1][1]:
                    redge = pixel
                    continue

    mid = (ledge+redge) / 2

    print(mid)


    return


while not quit:
    env.reset()
    total_reward = 0.0
    steps = 0
    restart = False
    while True:
        # register_input()
        screenCheck(200)
        s, r, terminated, truncated, info = env.step(a)
        total_reward += r
        if steps % 200 == 0 or terminated or truncated:
            print("\naction " + str([f"{x:+0.2f}" for x in a]))
            print(f"step {steps} total_reward {total_reward:+0.2f}")
        steps += 1
        if terminated or truncated or restart or quit:
            break
env.close()
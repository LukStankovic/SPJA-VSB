# -*- coding: utf-8 -*-

"""
Distance Field Rendering

SPJA, (c)2017 Tomas Fabian

Notes:
- all vectors are represented as triplets, e.g. (2.3, 5.6, -7.8)
"""

import math


# returns length of vector v
def length(v, n=2):
    return (v[0]**n + v[1]**n + v[2]**n)**(1/n)


# returns normalized vector v
def normalize(v):
    tmp = 1/length(v)
    return v[0] * tmp, v[1] * tmp, v[2] * tmp


# returns cross product (i.e. vector) of two vectors a and b
def cross(a, b):
    return a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]


# returns dot product (i.e. scalar) of two vectors a and b
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


# returns vector v multiplied by scalar a
def mul(v, a):
    return v[0]*a, v[1]*a, v[2]*a


# returns the sum of two vectors a and b
def plus(a, b):
    return a[0]+b[0], a[1]+b[1], a[2]+b[2]


# returns the difference of two vectors
def minus(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


# save image list of lists of triplets (r,g,b) where r, g and b are floats from the range <0,1>
def save_ppm(image, file_name="output.ppm", gamma=1 / 2.2):
    image_height = len(image)
    image_width = len(image[0])
    f = open(file_name, 'w')
    f.write("P3\n")
    f.write(str(image_width) + " " + str(image_height) + "\n")
    f.write("255\n")
    for line in image:
        for pixel in line:
            f.write(str(round(pixel[0]**gamma*255)))
            f.write(" ")
            f.write(str(round(pixel[1]**gamma*255)))
            f.write(" ")
            f.write(str(round(pixel[2]**gamma*255)))
            f.write("\t")
        f.write("\n")

    # follow the specification of plain PPM format
    # http://netpbm.sourceforge.net/doc/ppm.html
    # don't forget to change the range of values ​​in individual channels from 0..1 to 0..255

    f.close()


# x_ndc = (x_i+0.5)/width-0.5 and y_ndc = (0.5-(y_i+0.5)/height)*(height/width)
# ndc ... normalized image coordinates
# i   ... image coordinates in pixels
def generate_ray(x, y, origin=(-8, 2, 4), view_at=(0, 0, 0.5), up=(0, 0, 1), f=2.0):
    direction = normalize(minus(view_at, origin))
    cx = normalize(cross(direction, up))
    cy = normalize(cross(cx, direction))
    return (origin, normalize(plus(mul(direction, f), plus(mul(cx, x), mul(cy, y)))))


def generate_shadow_ray(origin, light):
    light_dir = minus(light, origin)
    return ((origin, normalize(light_dir)), length(light_dir))


# signed distance functions
# returns signed distance of given point p from sphere
def dist_sphere(p, center=(0, 0, 0), radius=0.5):
    return length(minus(center, p )) - radius


# returns signed distance of given point p from plane
def dist_plane(p, normal=normalize((0, 0, 1)), d=0):
    return dot(normal, p) - d


# returns the minimum distance from scene objects
def scene_distance(p):
    distances = []
    # compute distances from p to individual scene objects with the help of dist_x functions
    distances.append(dist_plane(p))
    distances.append(dist_sphere(p, (0, 0, 1)))
    return min(distances)


def scene_normal(p, h=0.001):
    return normalize((scene_distance(plus(p, (h, 0, 0))) - scene_distance(plus(p, (-h, 0, 0))),
                      scene_distance(plus(p, (0, h, 0))) - scene_distance(plus(p, (0, -h, 0))),
                      scene_distance(plus(p, (0, 0, h))) - scene_distance(plus(p, (0, 0, -h)))))


# sphere tracing
def ray_march(ray, lights, max_steps=10000, epsilon=0.0001, max_dist=1e+6, background=(0, 1, 0)):
    t = 0
    for i in range(max_steps):
        p = plus(ray[0], mul(ray[1], t))
        d = scene_distance(p)
        if d > max_dist: break
        if d < epsilon:
            normal = scene_normal(p)
            pixel = (0, 0, 0)
            for light in lights:
                shadow_ray, light_dist = generate_shadow_ray(p, light[0])
                if not occlusion_test(shadow_ray, light_dist):
                    pixel = plus(pixel, mul(mul(light[1], 1 / light_dist ** 2), max([0, dot(normal, shadow_ray[1])])))
            return pixel
        t += d
    return background


def occlusion_test(ray, max_dist, max_steps=10000, epsilon=0.0001):
    t = 10 * epsilon
    for i in range(max_steps):
        p = plus(ray[0], mul(ray[1], t))
        d = scene_distance(p)
        if d < epsilon and t < max_dist - 10 * epsilon:
            return True
        elif t >= max_dist:
            return False
        t += d
    return False


def main():
    #image = [[(0,1,0),(1,0,1)],[(1,0,1),(1,0,1)],[(1,0,1),(1,1,1)]]
    #save_ppm(image)

    # list of omni lights [(light_position, light_color), (light_position, light_color), (light_position, light_color)]
    lights = [((-3.2, -2.1, 4), (1, 1, 1)), ((0, 0, 0.5), (1, 0.01, 0.01)), ((2, 1, 4), (0.1, 0.2, 0.5))]

    # image size
    width = 1024 // 16;
    height = 768 // 16
    image = []

    # iterate each pixel
    for y in range(height):
        row = []
        for x in range(width):
            ray = generate_ray((x + 0.5) / width - 0.5, (0.5 - (y + 0.5) / height) * (height / width))
            pixel = ray_march(ray, lights)
            row.append(pixel)
        image.append(row)
        print("{:0.1f} % done".format(y / height * 100), end="\r")
    save_ppm(image)
    print("\rDone")


if __name__ == '__main__':
    main()
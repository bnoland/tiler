import math
import numpy as np
from scipy.stats import uniform
from imageio import imwrite, mimsave

# NOTE: These vectors are *not* drawn uniformly from the unit sphere. To correct
# this, see:
# http://corysimon.github.io/articles/uniformdistn-on-sphere/
def random_vector_3d(magnitude):
    theta = uniform.rvs(0, np.pi)
    psi = uniform.rvs(0, 2 * np.pi)
    x = magnitude * np.sin(theta) * np.cos(psi)
    y = magnitude * np.sin(theta) * np.sin(psi)
    z = magnitude * np.cos(theta)
    return np.array([x, y, z], dtype=float)

def interpolate(x0, x1, w):
    return x0 + w * (x1 - x0)

def ease_function(t):
    return 3 * t**2 - 2 * t**3

def perlin_point_3d(x, y, z, cell_x, cell_y, cell_z, gradients):
    x = x / cell_x
    y = y / cell_y
    z = z / cell_z

    # Compute cell edges.
    x0, y0, z0 = int(x), int(y), int(z)
    x1, y1, z1 = x0 + 1, y0 + 1, z0 + 1

    d1 = np.dot((x - x0, y - y0, z - z0), gradients[x0, y0, z0])
    d2 = np.dot((x - x1, y - y0, z - z0), gradients[x1, y0, z0])
    d3 = np.dot((x - x0, y - y1, z - z0), gradients[x0, y1, z0])
    d4 = np.dot((x - x1, y - y1, z - z0), gradients[x1, y1, z0])
    d5 = np.dot((x - x0, y - y0, z - z1), gradients[x0, y0, z1])
    d6 = np.dot((x - x1, y - y0, z - z1), gradients[x1, y0, z1])
    d7 = np.dot((x - x0, y - y1, z - z1), gradients[x0, y1, z1])
    d8 = np.dot((x - x1, y - y1, z - z1), gradients[x1, y1, z1])

    w = ease_function(x - x0)
    i1 = interpolate(d1, d2, w)
    i2 = interpolate(d3, d4, w)
    i3 = interpolate(d5, d6, w)
    i4 = interpolate(d7, d8, w)

    w = ease_function(y - y0)
    i5 = interpolate(i1, i2, w)
    i6 = interpolate(i3, i4, w)

    w = ease_function(z - z0)
    value = interpolate(i5, i6, w)
    return value

# NOTE: For now cell_x *must* evenly divide size_x, etc.
def perlin_noise_3d(size_x, size_y, size_z, cell_x, cell_y, cell_z):
    n_cell_x = size_x // cell_x
    n_cell_y = size_y // cell_y
    n_cell_z = size_z // cell_z

    # +1 for edge nodes
    gradients = np.empty([n_cell_x+1, n_cell_y+1, n_cell_z+1, 3], dtype=float)
    for i in range(gradients.shape[0]):
        for j in range(gradients.shape[1]):
            for k in range(gradients.shape[2]):
                gradients[i, j, k] = random_vector_3d(magnitude=1)

    buffer = np.empty([size_z, size_y, size_x], dtype=float)
    for z in range(size_z):
        for y in range(size_y):
            for x in range(size_x):
                buffer[z, y, x] = perlin_point_3d(
                    x, y, z, cell_x, cell_y, cell_z, gradients)

    return buffer

def normalize_buffer(buffer):
    buffer = buffer - buffer.min()
    buffer = buffer / buffer.ptp()
    buffer = np.around(255 * buffer).astype(np.uint8)
    return buffer

def turbulence_3d(size):
    pass

def cloud_3d(size):
    pass

def marble_3d(size):
    pass

if __name__ == '__main__':
    size = 256
    cell_size = 8
    buffer = perlin_noise_3d(size, size, size, cell_size, cell_size, cell_size)
    buffer = normalize_buffer(buffer)
    mimsave('test.gif', list(buffer))

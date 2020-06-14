import random, math
import numpy as np
from scipy.stats import uniform
from imageio import imwrite

def random_vector(magnitude):
    theta = uniform.rvs(0, 2 * np.pi)
    x, y = magnitude * np.cos(theta), magnitude * np.sin(theta)
    return np.array([x, y], dtype=float)

def interpolate(x0, x1, w):
    return x0 + w * (x1 - x0)

def ease_function(t):
    return 3 * t**2 - 2 * t**3

def perlin_point(x, y, cell_width, cell_height, gradients):
    x = x / cell_width
    y = y / cell_height

    # Compute cell edges.
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + 1, y0 + 1

    s = np.dot((x - x0, y - y0), gradients[x0, y0])
    t = np.dot((x - x1, y - y0), gradients[x1, y0])
    u = np.dot((x - x0, y - y1), gradients[x0, y1])
    v = np.dot((x - x1, y - y1), gradients[x1, y1])

    w = ease_function(x - x0)
    a = interpolate(s, t, w)
    b = interpolate(u, v, w)

    w = ease_function(y - y0)
    value = interpolate(a, b, w)
    return value

# NOTE: For now, cell_width and cell_height *must* evenly divide width and
# height, respectively.
def perlin_noise(width, height, cell_width, cell_height):
    n_horz_cells, n_vert_cells = width // cell_width, height // cell_height

    # +1 for edge nodes
    gradients = np.empty([n_horz_cells+1, n_vert_cells+1, 2], dtype=float)
    for i in range(gradients.shape[0]):
        for j in range(gradients.shape[1]):
            gradients[i, j] = random_vector(magnitude=1)

    image_buffer = np.empty([height, width], dtype=float)
    for y in range(height):
        for x in range(width):
            image_buffer[y, x] = perlin_point(
                x, y, cell_width, cell_height, gradients)

    image_buffer = image_buffer - image_buffer.min()
    image_buffer = image_buffer / image_buffer.ptp()
    image_buffer = np.around(255 * image_buffer).astype(np.uint8)

    return image_buffer

max_k = 8
size = 2 ** max_k
image_buffers = np.empty([size, size, max_k], dtype=np.uint8)
for k in range(1, max_k+1):
    cell_size = 2 ** k
    image_buffers[..., k-1] = perlin_noise(size, size, cell_size, cell_size)
    imwrite('test{}.png'.format(k), image_buffers[..., k-1], format='png')

# Quick n' dirty test.
image_buffer = np.zeros([size, size])
for k in range(1, max_k+1):
    image_buffer += image_buffers[..., k-1] / (2 ** (max_k-k+1))
image_buffer = image_buffer.astype(np.uint8)
imwrite('test.png', image_buffer, format='png')

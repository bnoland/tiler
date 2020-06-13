from PIL import Image, ImageFilter
import random, math

def random_gradient(magnitude):
    theta = 2 * math.pi * random.random()
    x, y = magnitude * math.cos(theta), magnitude * math.sin(theta)
    return x, y

cell_width, cell_height = 20, 20
n_horz_cells, n_vert_cells = 20, 20
gradient_magnitude = 1

gradients = {
    (x, y): random_gradient(gradient_magnitude)
    # +1 for outside edges
    for x in range(n_horz_cells+1) for y in range(n_vert_cells+1)
}

# import sys
# for key in gradients: print(key, gradients[key])
# sys.exit()

def interpolate(x0, x1, w):
    return w * x0 + (1 - w) * x1

# TODO: Possible to have a tuple as a function argument?
def dot(x0, y0, x1, y1):
    return x0 * x1 + y0 * y1

def perlin(x, y):
    # Compute cell edges.
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + 1, y0 + 1

    s = dot(x - x0, y - y0, *gradients[(x0, y0)])
    t = dot(x - x1, y - y0, *gradients[(x1, y0)])
    u = dot(x - x0, y - y1, *gradients[(x0, y1)])
    v = dot(x - x1, y - y1, *gradients[(x1, y1)])

    a = interpolate(s, t, x - x0)
    b = interpolate(u, v, x - x0)

    value = interpolate(a, b, y - y0)
    return value

width, height = n_horz_cells * cell_width, n_vert_cells * cell_height
mode = 'L'
image = Image.new(mode, (width, height))

pixels = image.load()

sigmoid = lambda x: 1 / (1 + math.exp(-x))

for x in range(width):
    for y in range(height):
        cell_x = x / cell_width
        cell_y = y / cell_height
        perlin_val = perlin(cell_x, cell_y)
        # print(perlin_val)
        pixel = round(perlin_val * 255)  # TODO: need some scaling
        pixels[x, y] = pixel

#image = image.filter(ImageFilter.GaussianBlur(radius=10))

image.show()

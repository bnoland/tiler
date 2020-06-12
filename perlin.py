from PIL import Image, ImageFilter
import random

def random_gradient():
    scale = 20
    x, y = scale*(random.random()-0.5), scale*(random.random()-0.5)
    return x, y

cell_width, cell_height = 10, 10
n_horz_cells, n_vert_cells = 50, 50
gradients = {
    (x, y): random_gradient()
    # +1 for outside edges
    for x in range(n_horz_cells+1) for y in range(n_vert_cells+1)
}

def interpolate(x0, x1, t):
    return t * x0 + (1 - t) * x1

# TODO: Possible to have a tuple as a function argument?
def dot(x0, y0, x1, y1):
    return x0 * x1 + y0 * y1

def perlin(x, y):
    # Compute cell edges.
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + 1, y0 + 1

    v00 = dot(x - x0, y - y0, *gradients[(x0, y0)])
    v10 = dot(x - x1, y - y0, *gradients[(x1, y0)])
    i0 = interpolate(v00, v10, x - x0)

    v01 = dot(x - x0, y - y1, *gradients[(x0, y1)])
    v11 = dot(x - x1, y - y1, *gradients[(x1, y1)])
    i1 = interpolate(v01, v11, x - x0)

    return interpolate(i0, i1, y - y0)

width, height = n_horz_cells * cell_width, n_vert_cells * cell_height
mode = 'RGB'  # TODO: grayscale
image = Image.new(mode, (width, height))

pixels = image.load()

for x in range(width):
    for y in range(height):
        cell_x = x / cell_width
        cell_y = y / cell_height
        perlin_val = round(perlin(cell_x, cell_y) * 255)
        pixel = (perlin_val, perlin_val, perlin_val)
        # print(pixel)
        pixels[x, y] = pixel

image = image.filter(ImageFilter.GaussianBlur(radius=10))

image.show()

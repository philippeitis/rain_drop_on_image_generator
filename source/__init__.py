import time

import PIL.ImageGrab
from PIL import ImageFilter
class Drop:
    def __init__(self,size,location):
        self.radius = size
        self.location = location
        self.heightmap = [[0] * size * 2] * size * 2
        self.initialize_heightmap()

    def initialize_heightmap(self):
        import math
        midpoint = self.radius
        for i in range(0,self.radius*2):
            for j in range(0,self.radius*2):
                x = abs(i - midpoint)
                y = abs(j - midpoint)
                radius = math.sqrt(x**2 + y**2)
                ## given point in heightmap in the sphere?
                if radius - 0.5 < midpoint:
                    ## determine height of given point
                    self.heightmap[i][j] = math.sqrt(self.radius**2 - (radius -0.5)**2)
                else:
                    self.heightmap[i][j] = 0

    def get_location(self):
        return self.location

def get_images():
    import os
    # May need to adjust for mac
    filenames = os.listdir("../input")
    return filenames

def get_image(filename):
    from PIL import Image
    return Image.open(filename)


def circle_crop(im):
    from PIL import Image, ImageOps, ImageDraw

    size = (128, 128)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    output = output.transpose(Image.FLIP_LEFT_RIGHT)
    output = output.transpose(Image.FLIP_TOP_BOTTOM)

    return output


def generate_images(num_drops = 10, min_drop_size = 10, max_drop_size = 25):
    filenames = get_images()
    for filename in filenames:
        # May need to adjust for mac
        #set_up_folder("../input/" + filename)
        im = get_image("../input/" + filename)
        circle_crop_im = circle_crop(im)
        drop_locations = seed_image_with_drops(im,num_drops)
        drops = set_drop_sizes(drop_locations, min_drop_size, max_drop_size)
        #merge_drops(drops,drop_locations)
        drop_images = generate_drop_images(drops,circle_crop_im)
        im = place_drop_images(drop_images,drops,im)
        im.save("../output/" + filename)

def set_up_folder(filename):
    from PIL import Image
    im = Image.open(filename)
    # Try to pass in 1920 x 1280 images or factors thereof
    im.save("../website/demo.jpg", "JPEG")


def seed_image_with_drops(image, num_drops):
    import random
    x, y = image.size
    drop_locations = []
    for i in range(num_drops):
        newX = random.randint(0,x)
        newY = random.randint(0,y)
        drop_locations.append((newX,newY))
    return drop_locations


def set_drop_sizes(drop_locations, min_size, max_size):
    import random
    array = []

    for location in drop_locations:
        drop = Drop(random.randint(min_size,max_size), location)
        drop.initialize_heightmap()
        array.append(drop)

    return array


## This is a whole array operation
# TODO: implement this lol
#def merge_drops(drops):
#    for drop in drops:
#        intersections = get_intersections(drop,drops)
#        merge_droplets(intersections)


## This merges a set of drops unconditionally


## Need to generate distortions
def generate_drop_images(drops, drop_image):
    drop_image_arr = []
    for drop in drops:
        drop_image_copy = drop_image.copy()
        drop_image_copy = drop_image_copy.resize((drop.radius*2,drop.radius*2))
        drop_image_arr.append(drop_image_copy)
    return drop_image_arr


def place_drop_images(drop_images,drops,im):
    for i in range(len(drop_images)):
        im.paste(drop_images[i],drops[i].get_location(),drop_images[i])

    return im


if __name__ == '__main__':
    import sys

    args = sys.argv

    ## First arg is num drops, second is min size in pixels, third is max size in pixels
    generate_images(int(args[1]),int(args[2]),int(args[3]))
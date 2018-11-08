# Jake Laney

import numpy as np
from PIL import Image
import math
import random

def zero(x, y):
    return x

def one(x, y):
    return y

def five(x, y):
    value = 0
    value += math.cos(2 * math.pi * x / 255.0)
    value += math.sin(2 * math.pi * y / 255.0) 
    value = 255 * abs(value) / 2.0
    return int(value)

def six(x, y):
    value = 0
    value += math.cos(3 * math.pi * x / 255.0)
    value += math.sin(2 * math.pi * y / 255.0)
    value = 255 * abs(value) / 2.0
    return int(value)

def nine(x, y): 
    value = 0
    value += math.cosh(x + y) % 256
    return int(value)

def thirteen(x, y):
    value = 0
    value += 255 * abs(math.tan((x + y) * math.pi / (8.0 * 255)))
    return int(value)


class Gene:
    ALLOWED_FUNCTIONS = [0, 1, 5, 6, 9, 13]
    FUNCTIONS = {}
    FUNCTIONS[0] = zero
    FUNCTIONS[1] = one
    FUNCTIONS[5] = five
    FUNCTIONS[6] = six
    FUNCTIONS[9] = nine
    FUNCTIONS[13] = thirteen

    def __init__(self, col):
        self.col = col
        self.f = self.randFunctionIndex()
        if col != 0:
            self.a = self.randCoor()
            self.b = self.randCoor()

    def randFunctionIndex(self):
        return self.ALLOWED_FUNCTIONS[random.randint(0, len(self.ALLOWED_FUNCTIONS) - 1)]
    
    def randCoor(self):
        return random.randint(0, self.col - 1)

    def compute(self, genome, x, y):
        if self.col == 0:
            return x
        elif self.col == 1:
            return y
        else:
            inputX = genome[self.a].compute(genome, x, y)
            inputY = genome[self.b].compute(genome, x, y)
            return self.FUNCTIONS[self.f](inputX, inputY)

class ImageGenerator():
    IMAGE_WIDTH = 255 # must be a 255x255 image for now
    IMAGE_HEIGHT = 255

    INPUTS = 2
    OUTPUTS = 3
    GENES = 100

    def main(self):
        genome = self.initGenome()
        pixels = self.decodeGenome(genome)
        self.showImage(pixels)

    def initGenome(self):
        genome = []
        for i in xrange(self.INPUTS):
            genome.append(Gene(i))
        for i in xrange(self.GENES):
            genome.append(Gene(self.INPUTS + i))
        return genome

    def decodeGenome(self, genome):
        outputs = []
        for i in xrange(self.OUTPUTS):
            outputs.append(random.randint(0, len(genome) - 1))
        pixels = np.zeros((self.IMAGE_WIDTH, self.IMAGE_HEIGHT, 3), dtype=np.uint8)
        for y in xrange(self.IMAGE_WIDTH):
            for x in xrange(self.IMAGE_HEIGHT):
                r = genome[outputs[0]].compute(genome, x, y)
                g = genome[outputs[1]].compute(genome, x, y)
                b = genome[outputs[2]].compute(genome, x, y)
                pixels[x][y] = [r, g, b]
        return pixels 

    def showImage(self, pixels):
        Image.fromarray(pixels, mode='RGB').show()

if __name__ == "__main__":
    ImageGenerator().main()




import cv2 as cv
import numpy as np
import random 

class Polygon:
    def __init__(self, sides, image):
        '''
        Parameters
        ------------
        
        sides:
            Number of sides of the polygon

        image:
            Target image to create the polygon.
            This is used to calculate the maximum x and y values for the polygons' vertices
        '''
        
        self.vertices, self.color = Polygon.random(sides, image)
    
    def __str__(self):
        return f'Vertices: {self.vertices} \nColor: {self.color}\n'
    
    def draw(self, canvas, fill=False):
        '''
        Draws polygon from points argument into canvas

        Parameters
        -------------

        canvas:
            Image to draw the polygon on

        fill:
            Whether to Fill the polygon with the same color.

        Return
        ---------

        image:
            image with the drawn polygon

        '''
        image = canvas

        for point in self.vertices:
            if type(point) != list or len(point) != 2:
                raise ValueError('Input must be arrays of size 2 describing each point in a 2-d plane. Ex: [x, y].')

        pts = np.array(self.vertices, np.int32)
        pts = pts.reshape((-1,1,2))

        cv.polylines(image, [pts], True, self.color)

        if fill:
            cv.fillPoly(image, [pts], self.color)
        
        return image
    
    def mutate(self, ratio, target):
        '''
        Applies mutation to polygon, this means, perturbations to vertex and color change.
        
        Parameters
        ------------
        
        ratio:
            float that represents the intensity of the mutation.
            Generally this should be in the interval (0.0, 1.0]
        '''
        def mutate_color(color):
            color = min(255, max(0, random.uniform(color - ratio * color, color + ratio * color)))
            return color
        
        def mutate_vertex(vertex):
            x = vertex[0]
            y = vertex[1]
            
            width = target.shape[0]
            height = target.shape[1]
            
            x = min(height, max(0.0, random.uniform(x - ratio * x, x + ratio * x)))
            y = min(width, max(0.0, random.uniform(y - ratio * y, y + ratio * y)))
            
            return [x, y]
    
        b, g, r = self.color
        self.color = (mutate_color(b),
                      mutate_color(g),
                      mutate_color(r))
                      
        for i in range(len(self.vertices)):
            self.vertices[i] = mutate_vertex(self.vertices[i])

        return self
    
    @classmethod
    def random(cls, sides, image):
        """
        Generates a random polygon with a random color.
        
        Parameters
        ------------
        
        sides: 
            Number of sides
            
        Return
        ------------
        
        Polygon: 
            A tuple ([v_1, v_2, ..., v_sides], (b, g, r))
            where v_i is the i-th vertex and (b, g, r) is the color.
        
        """

        width = image.shape[0]
        height = image.shape[1]

        randint = random.randint
        def random_point():
            return [randint(0, height), randint(0, width)]
        
        def random_color():
            return (randint(0, 255), randint(0, 255), randint(0, 255))

        return [*[random_point() for _ in range(sides)]], random_color()

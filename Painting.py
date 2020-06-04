from Polygon import Polygon

import copy
import cv2 as cv
import numpy as np
import random

class Painting:
    def __init__(self, num_genes, reference):
        '''
        Painting of a collection of polygons
        
        Parameters
        ------------
        
        genes:
            Number of genes to paint (number of polygons)
        
        reference:
            Target image to calculate fitness against.
            
        '''
        
        self.polygons = [Polygon(3, reference) for _ in range(num_genes)]
        self.canvas = np.zeros(reference.shape, np.int32)
        self.target = reference
    
    def __lt__(self, other):
        try:
            return self.fitness < other.fitness
        except AttributeError:
            print('You must call fit before sorting.')
        
    def paint(self):
        '''Paints genes into the canvas in order to calculate fitness of the being.'''
        for pol in self.polygons:
            self.canvas = pol.draw(self.canvas, fill=True)
            
    def fit(self, reference):
        '''Calculates fitness of the canvas against reference image'''
        self.canvas =  np.zeros(reference.shape, np.int32)
        self.paint()
        
        self.fitness = self.rmse(reference, self.canvas)
        return self

    @staticmethod
    def rmse(reference, canvas) -> float:
        '''Calculates root mean squared error between canvas and reference'''
        b_a, g_a, r_a = cv.split(reference)
        b_b, g_b, r_b = cv.split(canvas)

        def get_error(channel_a, channel_b):
            sq_diff = (channel_a - channel_b) ** 2
            summed = np.sum(sq_diff)
            num_pix = sq_diff.shape[0] * sq_diff.shape[1]
            return summed / num_pix

        rmse = np.sqrt((get_error(b_a, b_b) + get_error(g_a, g_b) + get_error(r_a, r_b)) / 3.0)
        return rmse
    
    @classmethod
    def random_population(cls, population_size, genes, image) -> list:
        '''
        Gerenates random population
        
        Parameters
        ------------
        
        population_size:
            Size of the population
        
        genes:
            Number of genes in each individual (that is, number of polygons in each painting)
            Be careful, this uses a lot of memory.
            
        reference:
            Target image to calculate fitness against

        Return
        --------
        
        population:
            list with all individuals in the population.
        '''

        return [cls(genes, image) for _ in range(population_size)]
    
    @classmethod
    def crossover(cls, daddy, mommy, ratio):
        '''
        Reproduces daddy and moddy to generate a new child Painting (life is beautiful).

        Parameters
        ------------

        daddy:
            Painting object

        mommy:
            Painting object

        ratio:
            proportion of the genoma to construct using daddy's genoma.

        Return
        --------

        child:
            Painting object
        '''
        
        polygons = []
        
        size = len(daddy.polygons)
        
        polygons.extend(copy.deepcopy(random.choices(daddy.polygons, k=int(ratio*size))))
        polygons.extend(copy.deepcopy(random.choices(mommy.polygons, k=size-int(ratio*size))))
        
        child = cls(0, daddy.target)
        child.polygons = polygons
        
        return child
        
    def mutate(self, recreation_chance, mutation_chance, ratio, target):
        '''
        Mutates entire painting by applying mutations in each polygon.
        See Polygon.mutate() for more info

        Parameters
        ------------

        recreation_chance: float
            chance that mutation will cause individual to be recreated
            
        mutation_chance: float
            chance that the mutation will actually happen

        ratio: float
            proportion of father's genes to get for child

        target: float
            target image
            
        '''
        
        happen = random.uniform(0.0, 1.0)
        if happen > mutation_chance:
            return self
        
        size = len(self.polygons)
        for pi in range(size):
            chance = random.uniform(0.0, 1.0)
            
            if chance <= recreation_chance:
                return Painting(size, target)
            else:
                self.polygons[pi] = self.polygons[pi].mutate(ratio, target)
            
        return self

import cv2
import numpy as np
import matplotlib.pyplot as plt


class GanglionicCell():
    def __init__(self, position, central_radius=5, peripherial_radius=11, isoff=False):
        self.pos = position
        self.s1 = central_radius
        self.s2 = peripherial_radius
        self.size = (central_radius, peripherial_radius)
        self.isoff = isoff

    def get_response(self, image):
        ## ганг - фильтр разность гауссиан с разной дисперсией
        ## 
        gauss_d1 = cv2.GaussianBlur(image, (self.s1, self.s1), sigmaX=0)
        gauss_d2 = cv2.GaussianBlur(image, (self.s2, self.s2), sigmaX=0)
        if self.isoff:
            ## поле реакций клеток с разным центром поля 
            laplace_response = gauss_d2 - gauss_d1
        else:
            laplace_response = gauss_d1 - gauss_d2
        v = laplace_response[self.pos[1], self.pos[0]]
        return v

    '''  Implement the model of the simple cell that can contain several ganglionic cells.
    The cell should respond to the line of the particular orientation, 
    It shouldn't respond to any other stimulus. It shouldn't be invaritant 
    to the orientation of the stimulus.
    It SHOULDN'T be invariant to the postition of the line in the receptive field.
    You can assume only single orientation.
    '''


class SimpleCell():
    def __init__(self, position, size=5):
        self.g_cells = []
        self.size = size
        d = 3
        for i in range(-(size//2), size//2 + 1):
            # for j in range(-(size//2), size//2 + 1):
            isoff = False
            self.g_cells.append(GanglionicCell((position[0], position[1] + i * d), isoff=isoff))

    def get_response(self, image):
        response = 0
        for cell in self.g_cells:
            response += cell.get_response(image)
        return response


'''  Implement the model of the complex cell that can contain several simple cells.
    The cell should respond to the line of the particular orientation, 
    It shouldn't respond to any other stimulus. 
    It SHOULD be invariant to the postition of the line in the receptive field.
    You can assume only single orientation.
    '''


class ComplexCell():
    def __init__(self, position, size=2):
        self.s_cells = []
        self.size = size
        d = 1
        for i in range(-(size//2), size//2 + 1):
            # for j in range(-(size//2), size//2 + 1):
            self.s_cells.append(SimpleCell((position[0] + i*d, position[1]), 2))

    def get_response(self, image):
        response = 0
        resp_arr = []
        for cell in self.s_cells:
            # response += cell.get_response(image)
            resp_arr.append(cell.get_response(image))
        
        return max(resp_arr)
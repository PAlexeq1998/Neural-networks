import cv2
import numpy as np
import matplotlib.pyplot as plt
from cells import GanglionicCell, SimpleCell, ComplexCell


def check_point_stimulus(cell):
    responses = []
    response_map = np.zeros((256, 256), dtype=np.int16)
    for i in range(0,13):
        for j in range(0,13):
            image = np.zeros((256,256), dtype=np.int16)
            cv2.circle(image, center=(128 + i - 6, 128 + j - 6), radius=1, color=(255,200,200), thickness=-1)
            v = cell.get_response(image)
            # responses.append(v + 128)
            cv2.circle(response_map, center=(i*16 + 32, j*16 + 32), radius=2, color=int(v), thickness=-1)
    return response_map

def check_circle_stimulus(cell):
    responses = []
    for i in range(0,30):
        image = np.zeros((256, 256), dtype=np.int16)
        cv2.circle(image, (128, 128), radius=i, color=(255, 255, 255), thickness=i*2+1)
        v = cell.get_response(image)
        responses.append(v)
    return responses

def rotate_line(cell):
    responses = []
    angles = []
    for i in range(0, 360, 10):
        angle_grad = i
        angle = i / 180 * np.pi
        image = np.zeros((256, 256), dtype=np.int16)
        cv2.line(image, (128 + int(100 * np.cos(angle)), 128 + int(100 * np.sin(angle))),
               (128 - int(100 * np.cos(angle)), 128 - int(100 * np.sin(angle))), color=(255, 255, 255), thickness=3, lineType=8)
        v = cell.get_response(image)
        responses.append(v)
        angles.append(angle_grad)
    return responses, angles


def shift_vertical_line_horizontally(cell):
    responses = []
    shifts = []
    for j in range(-20,20):
        shifts.append(j)
        image = np.zeros((256, 256), dtype=np.int16)
        cv2.line(image, (128 + j, 0), (128 + j, 256), color=255, thickness=3, lineType=8)

        v = cell.get_response(image)
        responses.append(v)
    return responses, shifts

def TestCell(cell, name='Test'):
    plt.figure(name)
    plt.subplot(2,2,1)
    response_map = check_point_stimulus(cell)
    plt.title('point_response')
    plt.imshow(response_map)
    plt.subplot(2,2,2)
    print('1')

    responses = check_circle_stimulus(cell)
    plt.plot(responses)
    plt.title('circle_response')
    plt.xlabel('radius, pix')
    plt.ylabel('response')
    plt.subplot(2,2,3)
    print('2')

    responses, angles = rotate_line(cell)
    plt.plot(angles, responses)
    plt.title('rotated line')
    plt.xlabel('angle, grad')
    plt.ylabel('response')
    plt.subplot(2,2,4)
    print('3')

    responses, shifts = shift_vertical_line_horizontally(cell)
    plt.plot(shifts, responses)
    plt.title('shifted line')
    plt.xlabel('shift, pix')
    plt.ylabel('response')
    plt.show()
    print(name)

if __name__ == '__main__':
    cell = GanglionicCell(position=(128,128), central_radius=7, peripherial_radius=15)
    TestCell(cell, name='Ganglionic-on')
    cell = GanglionicCell(position=(128,128), central_radius=15, peripherial_radius=7)
    TestCell(cell, name='Ganglionic-off')
    cell = SimpleCell(position=(128, 128))
    TestCell(cell, name='Simple')
    cell = ComplexCell(position=(128, 128))
    TestCell(cell, name='Complex')
    pass

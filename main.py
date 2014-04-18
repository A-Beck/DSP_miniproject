from Rect import Rect
import segment
from scipy.cluster.vq import kmeans, vq, whiten
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import array

def get_vectors(point_list):
    x_list = []
    y_list = []
    vel_list = []
    acc_list = []
    for pt in point_list:
        x_list.append(pt.x)
        y_list.append(pt.y)
        vel_list.append(pt.velocity)
        acc_list.append(pt.acceleration)
    return [x_list, y_list, vel_list, acc_list]


def make_matrix(point_list):
    matrix = []
    for pt in point_list:
        vect = []
        vect.append(pt.x)
        vect.append(pt.y)
        vect.append(pt.velocity)
        vect.append(pt.acceleration)
        matrix.append(vect)
    return matrix


if __name__ == '__main__':
    rect = Rect(12094847.66846662, 3511329.41319890, 12095742.17970170, 3510025.27955079)
    pt_list = segment.select_insar_points('raw_data.csv', rect)
    data = make_matrix(pt_list)
    whitened_data = whiten(data)
    #print whitened_data
    codebook, distortion = kmeans(whitened_data, 10, iter=100)
    a = vq(whitened_data, codebook)
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    # blue, green, red, cyan, magenta, yellow, black, white
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(1, 1, 1, marker='x',  color=colors[2])
   # ax.scatter(2, 2, 2, marker='o',  color=colors[3])
    plt.show()

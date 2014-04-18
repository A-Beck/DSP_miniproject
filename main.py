from Rect import Rect
import segment
from scipy.cluster.vq import kmeans, vq, whiten
import matplotlib.pyplot as plt
import copy


COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# blue, green, red, cyan, magenta, yellow, black, white
MARKERS = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'D', ]


def make_matrix(point_dict, filter=[]):
    matrix = []
    for key in point_dict.keys():
        obs = copy.deepcopy(point_dict[key])
        if 'xy' in filter:  # allows you to isolate velocity and acceleration
            obs.remove(obs[0])
            obs.remove(obs[0])
        matrix.append(obs)
    # each row in the matrix is an observation
    return matrix


def run_kmeans(matrix, num_centroids=5, iterations=10):
    """
    Runs K means Algorithm
    """
    if num_centroids > 63:
        num_centroids = 63  # Max number of groups = 63
    w_matrix = whiten(matrix)
    code_book, distortion = kmeans(w_matrix, num_centroids, iter=iterations)
    code, dist = vq(w_matrix, code_book)
    return code


def plot_data(point_dict, code):
    """
     Plots the data aquired by the Kmeans algorithm and insar pts
    """
    group_dict = {}
    length = len(code)
    keys = point_dict.keys()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # This loop plots each point
    for i in range(length):
        x = point_dict[keys[i]][0]
        y = point_dict[keys[i]][1]
        group = code[i]
        marker, color = get_marker(group)
        p = ax.scatter(x, y, marker=marker, color=color)
        # Stages data to create legend
        if group not in group_dict.keys():
            group_dict[group] = p
    # This creates the Legend
    label_list = []
    plot_list = []
    for key in group_dict.keys():
        label = 'Group %d' % key
        plot_list.append(group_dict[key])
        label_list.append(label)
    plt_tup = tuple(plot_list)
    label_tup = tuple(label_list)
    fig.legend(plt_tup, label_tup)
    plt.draw()
    plt.show()


def get_marker(num):
    c_i = num % len(COLORS)
    m_i = num % len(MARKERS)
    return MARKERS[m_i], COLORS[c_i]


if __name__ == '__main__':
    filename = '/home/andrew/Dropbox/LabStuff/TRE_data/MMMBT_RST_F3_A_T122-TSR.shp'
    rect = Rect(12094847.66846662, 3511329.41319890, 12095742.17970170, 3510025.27955079)
    pt_dict = segment.select_insar_points(filename, rect, filter=['time_series', 'area'])
    data = make_matrix(pt_dict, filter=[])
    code = run_kmeans(data, iterations=10, num_centroids=10)
    plot_data(pt_dict, code)

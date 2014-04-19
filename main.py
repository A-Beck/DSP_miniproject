from Struct import Rect, Cluster
import segment
from scipy.cluster.vq import kmeans, vq, whiten
import matplotlib.pyplot as plt
import copy
import sys
import getopt
import os
import thread


COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# blue, green, red, cyan, magenta, yellow, black
MARKERS = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'D', ]


def make_matrix(point_dict, filter=[]):
    """
    Makes a matrix that can be run through the K means algo
    filter:
        include 'xy' if you want to exclude x and y coordinates
    """
    matrix = []
    for key in point_dict.keys():
        obs = copy.deepcopy(point_dict[key])
        if 'xy' in filter:  # allows you to isolate velocity and acceleration
            obs.remove(obs[0])
            obs.remove(obs[0])
        if 'va' in filter:
            obs.remove(obs[2])
            obs.remove(obs[2])
        matrix.append(obs)
    # each row in the matrix is an observation
    return matrix


def run_kmeans(matrix, num_centroids=5, iterations=10):
    """
    Runs K means Algorithm
    """
    if num_centroids > 63:
        num_centroids = 63  # Max number of groups = 63
    w_matrix = whiten(matrix)  # normalize data
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
    plt.title('Clusters')
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



def generate_stats(point_dict, code):
    length = len(code)
    cluster_dict = {}
    keys = point_dict.keys()
    for item in code:
        if item not in cluster_dict.keys():
            cluster_dict[item] = Cluster(item)
    for i in range(length):
        pt_list = point_dict[keys[i]]
        clust = code[i]
        cluster_dict[clust].add_pt(pt_list)
    for key in cluster_dict.keys():
        x,  y, v, a = cluster_dict[key].get_avgs()
        print 'Group %d averages' % cluster_dict[key].group_id
        print 'x coordinate: %f' % x
        print 'y coordinate: %f' % y
        print 'Velocity: %f mm/yr' % v
        print 'Acceleration: %f mm/yr^2\n' % a


def get_marker(num):
    c_i = num % len(COLORS)
    m_i = num % len(MARKERS)
    return MARKERS[m_i], COLORS[c_i]


def main():

    # Default values for everything
    rect = Rect(12094847.66846662, 3511329.41319890, 12095742.17970170, 3510025.27955079)
    filename = '/home/andrew/Dropbox/LabStuff/TRE_data/MMMBT_RST_F3_A_T122-TSR.shp'
    iterations = 10
    filter = []
    centroids = 5
    method = 'k-means'

    options = ["file=", "iter=", "filt=", "centroids="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc", options)
    except getopt.GetoptError:
        print 'main.py --file=<shp file> --iter=<num iterations> --filt=<filter type>, ' \
              '\n--centriods=<num centriods>'
        sys.exit()

    for opt, arg in opts:

        if opt == '-h':
            print 'main.py --file=<shp file> --iter=<num iterations>\n ' \
                  '--filt=<filter type>, --centriods=<num centriods>'
            print 'filter options: \n\txy to remove xy coordinates\n\tva to remove velocity and acceleration'
            print 'file info: file entered must be a shapefile (.shp)'
            print 'iter info: number of iterations for kmeans. Must be an integer'
            print 'centroid info: number of centroids for kmeans. Must be an integer'
            print 'To change ROI, run with -c option. All coordinates in EPSG:2284 NAD83'
            sys.exit()

        elif opt == '-c':
            # Allows chages to the region of interest
            rect = segment.prompt_for_coordinates()

        elif opt == '--file':
            # Change shapefile being used
            filename = arg
            if not os.path.isfile(filename):
                print 'Error: Path supplied is not a file'
                sys.exit()
            if filename.split('.')[1] == 'shp':
                print 'Error: Path supplied is not a shp file'
                sys.exit()

        elif opt == '--iter':
            # change number of iterations for k-means
            try:
                iterations = int(arg)
            except ValueError:
                print 'Number of iterations must be a positive integer'

        elif opt == "--filt":
            if arg == 'va' or arg == 'xy':
                filter.append(arg)
            else:
                print 'Error: Unsupported filter!'

        elif opt == "--centroids":
            try:
                centroids = int(arg)
            except ValueError:
                print 'ERROR: Number of centroids must be a positive integer'

    # run Kmeans algorithm
    pt_dict = segment.select_insar_points(filename, rect, filter=['time_series', 'area'])
    data = make_matrix(pt_dict, filter=filter)
    code = run_kmeans(data, iterations=iterations, num_centroids=centroids)
    thread.start_new_thread(generate_stats, (pt_dict, code, ))  # spin up a thread to generate statistics
    plot_data(pt_dict, code)


if __name__ == '__main__':
    main()

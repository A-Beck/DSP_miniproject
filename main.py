from Struct import Rect, Cluster
import segment
from scipy.cluster.vq import kmeans, vq, whiten
from scipy.cluster.hierarchy import fclusterdata
import matplotlib.pyplot as plt
import copy
import sys
import getopt
import os
import thread
from sets import Set

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


def run_fclusterdata(matrix, thresh, metric, method):
    w_matrix = whiten(matrix)  # normalize data
    code = fclusterdata(w_matrix, thresh, metric=metric, method=method)
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
    algo = 'kmeans'
    thresh = 1.153
    metric = 'euclidean'
    method = 'single'

    options = ["file=", "iter=", "filt=", "centroids=", "algo=", "thresh=", "metric=", "method="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc", options)
    except getopt.GetoptError:
        print 'ERROR in Arguments : Run \'python main.py -h\' for help =)'
        sys.exit()

    for opt, arg in opts:

        if opt == '-h':
            print 'main.py --file=<shp file> --iter=<num iterations>\n ' \
                  '--filt=<filter type>, --centriods=<num centriods> --algo=<type>' \
                  '--thresh=<val> --metric=<type> --method=<type>'
            print '--filt options: \n\txy to remove xy coordinates\n\tva to remove velocity and acceleration'
            print '--file info: file entered must be a shapefile (.shp)'
            print '--iter info: number of iterations for kmeans. Must be an integer'
            print '--centroid info: number of centroids for kmeans. Must be an integer'
            print '--algo info: Must be "kmeans"  or hier'
            print '--thresh info: Must be a positive float. Used for hier method'
            print '--metirc info: Way to calculate distance. See http://docs.scipy.org/doc/scipy-0.13.0' \
                  '/reference/generated/scipy.spatial.distance.pdist.html'
            print '--method info: Method to run hier under. See' \
                  'http://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage'        
            print 'To change ROI, run with -c option. All coordinates in EPSG:2284 NAD83'
            print 'General Warnings: This was tested with only one the shapefile I was intereted in. Due to variations in' \
                  'shapefile format, this program may not work with other files. Should be easy to alter to make it work, just need' \
                  'to alter indexes in the segment.py file and in main.py file. Happy Coding!'
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

        elif opt == "--algo":
            if arg == 'kmeans' or arg == 'hier':
                algo = arg
            else:
                print 'Error: Unsupported method Entered'

        elif opt == "--thresh":
            try:
                thresh = float(arg)
            except ValueError:
                print 'ERROR: threshold must be a positive float'

        elif opt == "--metric":
            metric = arg

        elif opt == "--method":
            method = arg

    # run Kmeans algorithm
    pt_dict = segment.select_insar_points(filename, rect, filter=['time_series', 'area'])
    data = make_matrix(pt_dict, filter=filter)
    code = None
    if algo == "kmeans":
        code = run_kmeans(data, iterations=iterations, num_centroids=centroids)
    elif algo == "hier":
        code = run_fclusterdata(data, thresh, metric, method)
    thread.start_new_thread(generate_stats, (pt_dict, code, ))  # spin up a thread to generate statistics
    plot_data(pt_dict, code)



if __name__ == '__main__':
    main()

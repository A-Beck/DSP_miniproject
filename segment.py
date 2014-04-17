from liblas import file
from Rect import Rect, Point
import csv

def prompt_for_coordinates():
    """
    Prompts user for coordinates to create the region of interest
    """
    print 'Please enter coordinates in form x,y of native map projection'
    point_a = (tuple(map(float, raw_input('Please enter upper left point : ').split(','))))
    point_b = (tuple(map(float, raw_input('Please enter lower right point : ').split(','))))
    return Rect(point_a[0], point_a[1], point_b[0], point_b[1])


def select_insar_points(filename, rect):
    """
    Takes the region of interest specified by rect and
    extracts all insar points within it
    """
    point_list = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            id = row[0]
            x = row[1]
            y = row[2]
            vel = row[3]
            acc = row[4]
            area = row[5]
            if not rect.outside_rectangle(x,y):
                pt = Point(id, x, y, vel, acc, area)
                point_list.append(pt)
    return point_list


# Code below will run when 'python segment.py' is entered on the command line
if __name__ == '__main__':
    rect  = prompt_for_coordinates()
    select_insar_points('raw_data.csv', rect)
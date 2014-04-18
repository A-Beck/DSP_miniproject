import shapefile
from Rect import Rect, Point


def prompt_for_coordinates():
    """
    Prompts user for coordinates to create the region of interest
    """
    print 'Please enter coordinates in form x,y of native map projection'
    point_a = (tuple(map(float, raw_input('Please enter upper left point : ').split(','))))
    point_b = (tuple(map(float, raw_input('Please enter lower right point : ').split(','))))
    return Rect(point_a[0], point_a[1], point_b[0], point_b[1])


def select_insar_points(filename, rect, filter=[]):
    """
    Takes the region of interest specified by rect and
    extracts all insar points within it
    If area_flag is True, only points with non-zero area will be accepted
    """
    sf_reader = shapefile.Reader(filename)
    shapes = sf_reader.shapes()  # This gives X and Y coordinates
    records = sf_reader.records()
    num_points = len(shapes)
    point_dict = {}
    for i in range(num_points):
        x = float(shapes[i].points[0][0])
        y = float(shapes[i].points[0][1])
        code = records[i][0]
        velocity = records[i][3]
        acceleration = records[i][5]
        area = records[i][8]  # in case we want to exclude TS
        time_series = records[i][9:]
        if not rect.outside_rectangle(x, y):
            point_list = [x, y, velocity, acceleration]
            if 'area' in filter:  # filter out non-ps Points
                if area > 0:
                    continue
            if 'time_series' not in filter:  # easier to add it then to remove it
                for value in time_series:
                    point_list.append(value)
            point_dict[code] = point_list
    return point_dict

# Code below will run when 'python segment.py' is entered on the command line
if __name__ == '__main__':
    # rect  = prompt_for_coordinates()
    filename = '/home/andrew/Dropbox/LabStuff/TRE_data/MMMBT_RST_F3_A_T122-TSR.shp'
    rect = Rect(12094847.66846662, 3511329.41319890, 12095742.17970170, 3510025.27955079)
    dictionary = select_insar_points(filename, rect)
    print dictionary
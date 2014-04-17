import shapefile
import csv

SOURCE = '/home/andrew/Dropbox/LabStuff/TRE_data/MMMBT_RST_F3_A_T122-TSR.shp'
DEST = '/home/andrew/Dropbox/Spring2014/DSP/Miniproject/raw_data.csv'

sf_reader = shapefile.Reader(SOURCE)
shapes = sf_reader.shapes()  # This gives X and Y coordinates
records = sf_reader.records()  # This is the data that TRE gives

# print len(shapes)  # This has 20708 items
num_points = len(shapes)

with open(DEST, 'w') as f:
	writer = csv.writer(f)

	for i in range(0, num_points):
		x = shapes[i].points[0][0]
		y = shapes[i].points[0][1]
		code = records[i][0]
		shape = records[i][1]
		velocity = records[i][4]
		acceleration = records[i][6] 
		area = records[i][8]  # in case we want to exclude TS
		time_series = records[i][9:]
		writer.writerow([code, x, y, velocity, acceleration, area])
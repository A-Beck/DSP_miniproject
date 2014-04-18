from Rect import Rect
import segment
from scipy.cluster.vq import kmeans
import numpy as np

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
	return zip(x_list, y_list, vel_list, acc_list)


if __name__ == '__main__':
	rect = Rect(12094847.66846662, 3511329.41319890, 12095742.17970170, 3510025.27955079)
	pt_list =  segment.select_insar_points('raw_data.csv', rect)
	print get_vectors(pt_list)
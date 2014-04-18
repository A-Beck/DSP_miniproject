class Rect():
    """ A class that models a rectangular area of interest """

    def __init__(self, ax, ay, bx, by):
        """
        Takes in the upper left hand corner vertex and lower right hand corner
        vertex to create a rectangle
        """
        self.upper_left = (ax, ay)
        self.lower_left = (ax, by)
        self.upper_right = (bx, ay)
        self.lower_right = (bx, by)

    def __str__(self):
        return str(self.upper_left) + " " + str(self.lower_left) + " " + str(self.upper_right) + " " + str(
            self.lower_right)

    def __repr__(self):
        return str(self)

    def outside_rectangle(self, x, y):
        """
        Parameters : x and y coordinates of the suspect point
        Returns : True if outside the rectangle, false if inside rectangle
        """
        y_flag = (y > self.upper_left[1]) or (y < self.lower_right[1])
        x_flag = (x < self.upper_left[0]) or (x > self.lower_right[0])
        return y_flag or x_flag


class Point():
    """ A class that represents a point """

    def __init__(self, id, x, y, vel, acc):
        self.id = id
        self.x = x
        self.y = y
        self.velocity = vel
        self.acceleration = acc
        self.group_id = None

    def assign_to_cluster(self, group_id):
        self.group_id = group_id
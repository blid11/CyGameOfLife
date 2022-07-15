class Characterize:

    def __init__(self):

        # can store functions for object characterization in this class
        # this class will store the information about all the glider objects and enable access to it
        # to run collision simulations
        # additionally it will produce the inverted, mirrored and inverted-mirrored versions of any gliders

        #dict of summarized info about glider: period, signatures, coordinates of the captured glider, rule in which it was found 
        # the key encoding a glider will be a vector that is the sum of its individual signatures (carried out in SimRand class)
        self.dict_of_gliders = {}

        #dict where encode_glider is key, but the value is a list of lists of the coordinates of the original, 
        #inverted, mirrored and inverted-mirrored versions of the glider
        self.dict_of_coords = {}

        self.inverse_cells = []
        self.mirror_cells = []
        self.inv_mirror_cells = []

    def check_in_dict(self, encode_glider):

        # this function will allow the Simulation class to check if a glider found in random soups
        # is currently present in the dictionary
        if encode_glider in self.dict_of_gliders.keys():
            return True
        else:
            return False

    def add_to_dict(self, encode_glider, summary_of_object):

        self.dict_of_gliders[encode_glider] = summary_of_object

    def get_dict_of_coords(self):
        return self.dict_of_coords

    def inverse_and_mirror(self):

        # for each glider object in dict of gliders, we will need to come up with sets of coordinates for
        # the inverted and mirrored versions of the gliders
        # we will start by finding the max and min values for the xs, ys and zs of the glider 
        # the coords of the glider is the first element of summary of object (from SimRand class)
        # summary_of_object = [object_cells, extreme_cell_of_object, dist_x, dist_y, dist_z,
        #                      object_signature_list, period, self.rule_tuple]

        for key in self.dict_of_gliders.keys():
            summary_obj = self.dict_of_gliders[key]
            print(summary_obj)
            cells_of_object = summary_obj[0]

            if len(cells_of_object) == 0:
                print("object has 0 cells")

            # first, move the entire object to a central position for collisions (to be carried out in SimCollision)
            # by finding the difference between the most extreme cell of the object and 65,65,65
            # then add that difference vector to each of the cells in the object to
            # "drag" it to the center of the grid.

            extreme_cell = summary_obj[1]

            print("extreme cell is {}".format(extreme_cell))
            difference_tuple = (65 - extreme_cell[0], 65 - extreme_cell[1], 65 - extreme_cell[2])

            # this will be the first set of coordinates stored under the glider name in coordsdict
            # additionally prior to the coordinates, the dist_x, dist_y, dist_z will be stored
            # as a tuple as the first element
            # these are the distances that the glider travels in each respective axis during one period
            translated_obj = []

            for cell in cells_of_object:
                new_x = cell[0] + difference_tuple[0]
                new_y = cell[1] + difference_tuple[1]
                new_z = cell[2] + difference_tuple[2]
                new_cell = (new_x, new_y, new_z)
                translated_obj.append(new_cell)

            # want to find the maximum and minimum y and z values
            first_cell = translated_obj[0]
            min_x = first_cell[0]
            max_x = first_cell[0]
            min_y = first_cell[1]
            max_y = first_cell[1]
            min_z = first_cell[2]
            max_z = first_cell[2]

            for cell in translated_obj:
                if cell[0] < min_x:
                    min_x = cell[0]
                elif cell[0] > max_x:
                    max_x = cell[0]
                elif cell[1] < min_y:
                    min_y = cell[1]
                elif cell[1] > max_y:
                    max_y = cell[1]
                elif cell[2] < min_z:
                    min_z = cell[2]
                elif cell[2] > max_z:
                    max_z = cell[2]
                else:
                    next

            #this function can fill in three lists which will then be stored with translated obj
            # the three lists are the 
            # in coords dict under the object's name
            self.make_flipped(translated_obj, min_x, max_x, min_y, max_y, min_z, max_z)

            obj_period_dist = (summary_obj[2], summary_obj[3], summary_obj[4])
            obj_dims = (max_x - min_x, max_y - min_y, max_z - min_z)

            # print("translated obj has length {}".format(len(translated_obj)))

            obj_coords_and_deg_free = [obj_period_dist, obj_dims, translated_obj,
                                       self.inverse_cells, self.mirror_cells,
                                       self.inv_mirror_cells, summary_obj[7]]

            # one needs to run collision simulations for an object, stored under the object's name.
            # inverse cells and inverse mirror cells should be offset from centre point 65, 65, 65 by several
            # units along the x axis in the positive direction. i.e. it should start 7 or 8 units away at 72, 65, 65
            # this translation will be carried out in RuleIter class, after the object has been flipped in this class. 

            self.dict_of_coords[key] = obj_coords_and_deg_free

            self.inverse_cells = []
            self.mirror_cells = []
            self.inv_mirror_cells = []


        # summary_of_object = [object_cells, extreme_cell_of_object, dist_x, dist_y, dist_z,
        #                      object_signature_list, period]

    def make_flipped(self, translated_obj, min_x, max_x, min_y, max_y, min_z, max_z):

        # mirror cells
        # print(translated_obj)
        # print(min_x, max_x, min_y, max_y, min_z, max_z)

        # if the width is odd, then we don't touch the centre cells
        # also we swap the positions or states of cells at (x, y, z) and (width - x, y, z)
        # now need to make a 3 dimensional image of translated obj and copy it

        # print("translated obj has length {}".format(len(translated_obj)))

        #CODE FOR MIRROR IMAGE

        x_range = max_x - min_x

        #range and the function in general must have at least 1 item to perform operations on in the loop
        # 83, 82, 81. 83 -81 is 2. If the difference in x is 1 or 2, then we say the following

        if x_range <= 2:
            x_halfway = min_x + 1

        #otherwise we find the midpoint to be the end of the range for the loop,
        # the loop will loop to x_halfway - 1
        else:
            num_elements = x_range + 1

            x_halfway = num_elements // 2 + min_x

        if (max_x - min_x) % 2 == 0:
            # there could be centre cells that the flip algorithm does not account for
            for cell in translated_obj:
                if cell[0] == x_halfway:
                    self.mirror_cells.append(cell)

        for xcoord in range(min_x, x_halfway):
            for ycoord in range(min_y, max_y + 1):
                for zcoord in range(min_z, max_z + 1):

                    cell = (xcoord, ycoord, zcoord)
                    mirrorCell = ((max_x - (xcoord - min_x)), ycoord, zcoord)

                    if (cell in translated_obj) and (mirrorCell in translated_obj):
                        # both cells stay as swapping leads to both cells still being alive
                        self.mirror_cells.append(cell)
                        self.mirror_cells.append(mirrorCell)
                    elif cell in translated_obj:
                        self.mirror_cells.append(mirrorCell)
                        # no need to remove cell from a new list
                    elif mirrorCell in translated_obj:
                        self.mirror_cells.append(cell)
                    else:
                        next

        # print("mirror cells has length {}".format(len(self.mirror_cells)))
        # print(self.mirror_cells)


        #CODE FOR INVERTED IMAGE

        z_range = max_z - min_z

        # range and the function in general must have at least 1 item to perform operations on in the loop
        # 83, 82, 81. 83 -81 is 2. If the difference in x is 1 or 2, then we say the following

        if z_range <= 2:
            z_halfway = min_z + 1

        # otherwise we find the midpoint to be the end of the range for the loop,
        # the loop will loop to x_halfway - 1
        else:
            num_elements = z_range + 1

            z_halfway = num_elements // 2 + min_z

        if (max_z - min_z) % 2 == 0:
            # there could be centre cells that the flip algorithm does not account for
            for cell in translated_obj:
                if cell[2] == z_halfway:
                    self.inverse_cells.append(cell)

        for xcoord in range(min_x, max_x + 1):
            for ycoord in range(min_y, max_y + 1):
                for zcoord in range(min_z, z_halfway):

                    cell = (xcoord, ycoord, zcoord)
                    inverseCell = (xcoord, ycoord, (max_z - (zcoord - min_z)))

                    if (cell in translated_obj) and (inverseCell in translated_obj):
                        # both cells stay as swapping leads to both cells still being alive
                        self.inverse_cells.append(cell)
                        self.inverse_cells.append(inverseCell)
                    elif cell in translated_obj:
                        self.inverse_cells.append(inverseCell)
                        # no need to remove cell from a new list
                    elif inverseCell in translated_obj:
                        self.inverse_cells.append(cell)
                    else:
                        next

        # print("inverse cells has length {}".format(len(self.inverse_cells)))
        # print(self.inverse_cells)


        # CODE FOR MIRROR INVERSE IMAGE

        z_range = max_z - min_z

        # range and the function in general must have at least 1 item to perform operations on in the loop
        # 83, 82, 81. 83 -81 is 2. If the difference in x is 1 or 2, then we say the following

        if z_range <= 2:
            z_halfway = min_z + 1

        # otherwise we find the midpoint to be the end of the range for the loop,
        # the loop will loop to x_halfway - 1
        else:
            num_elements = z_range + 1

            z_halfway = num_elements // 2 + min_z

        if (max_z - min_z) % 2 == 0:
            # there could be centre cells that the flip algorithm does not account for
            for cell in self.mirror_cells:
                if cell[2] == z_halfway:
                    self.inv_mirror_cells.append(cell)


        for xcoord in range(min_x, max_x + 1):
            for ycoord in range(min_y, max_y + 1):
                for zcoord in range(min_z, z_halfway):

                    cell = (xcoord, ycoord, zcoord)
                    inv_mir_Cell = (xcoord, ycoord, (max_z - (zcoord - min_z)))

                    if (cell in self.mirror_cells) and (inv_mir_Cell in self.mirror_cells):
                        # both cells stay as swapping leads to both cells still being alive
                        self.inv_mirror_cells.append(cell)
                        self.inv_mirror_cells.append(inv_mir_Cell)
                    elif cell in self.mirror_cells:
                        self.inv_mirror_cells.append(inv_mir_Cell)
                        # no need to remove cell from a new list
                    elif inv_mir_Cell in self.mirror_cells:
                        self.inv_mirror_cells.append(cell)
                    else:
                        next
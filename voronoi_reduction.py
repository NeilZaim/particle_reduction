""" Voronoi reduction algorithm """

import argparse
import os
dict_parametrs_names = {'position/x', 'position/y', 'position/z', 'momentum/x', 'momentum/y', 'momentum/z'}


class Dimentions_data():

    def __init__(self, name, vector):
        self.vector = numpy.array(vector)
        self.name = name
        self.standard_deviation = -1.
        self.lenght = -1.
        self.weights = []
        self.sum_weights = -1.


    def set_weights(self, weights):
        self.weights = weights
        self.sum_weights = numpy.sum(weights)

    def get_statistical_average(self):
        vector_mult = self.vector * self.weights
        sum_mult = numpy.sum(vector_mult)
        normalised_average = sum_mult / self.sum_weights
        return normalised_average

class Particles_data():

    def __init__(self, name, data):
        self.name_particles = name
        self.data = data


class Particles_groups():
    """ Collect values from datasets in hdf file """

    def __init__(self, particles_name):
        self.particles_groups = []
        self.positions = []
        self.name_particles = particles_name

    def __call__(self, name, node):
        if isinstance(node, h5py.Group):
            print('is instance group ')
            name_idx = node.name.find(self.name_particles)
            if name_idx != -1:
                group_particles_name = node.name[name_idx + len(self.name_particles) + 1:]
                if group_particles_name.endswith('position'):
                    self.positions.append(node)
                if group_particles_name.find('/') == -1 and len(group_particles_name) != 0:
                    self.particles_groups.append(node)
        return None

def voronoi_algorithm(hdf_file, hdf_file_reduction, tolerance_momentum, tolerance_position):

    print(' hdf file: ' + str(hdf_file))
    print(' hdf file reduction ' + str(hdf_file_reduction))
    print(' tolerance momentum  ' + str(tolerance_momentum))
    print(' tolerance position ' + str(tolerance_position))


def voronoi_reduction(hdf_file, hdf_file_reduction, tolerance_momentum, tolerance_position):

    name_hdf_file_reduction = ''

    if hdf_file != '':
        if os.path.exists(hdf_file):
            name = hdf_file[:-4]
            idx_of_name = name.rfind('/')
            if idx_of_name != -1:
                name_hdf_file_reduction = hdf_file_reduction + hdf_file[idx_of_name + 1: -6] + 'reduction.h5'
            else:
                name_hdf_file_reduction = hdf_file_reduction + hdf_file[:-3] + '.h5'

            voronoi_algorithm(hdf_file, hdf_file_reduction, tolerance_momentum, tolerance_position)
        else:
            print('The .hdf file does not exist')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="voronoi reduction")

    parser.add_argument("-hdf", metavar='hdf_file', type=str,
                        help="hdf file without patches")

    parser.add_argument("-hdf_re", metavar='hdf_file_reduction', type=str,
                        help="reducted hdf file")

    parser.add_argument("-momentum_tol", metavar='tolerance_momentum', type=float,
                        help="tolerance of momentum")

    parser.add_argument("-momentum_pos", metavar='tolerance_position', type=float,
                        help="tolerance of position")

    args = parser.parse_args()
    voronoi_reduction(args.hdf, args.hdf_re, args.momentum_tol, args.momentum_pos)


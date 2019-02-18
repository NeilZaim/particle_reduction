
import numpy
import math
import copy


class Point:

    def __init__(self, coords, weight):
        """A weighted point, coords is array-like, weight is float"""

        self.coords = coords
        self.weight = weight


class VoronoiMergingAlgorithmParameters:
    """Tolerance is array-like, first -- coordinate tolerance, second -- momentum tolerance"""

    def __init__(self, tolerance):
        self.tolerance = tolerance


class VoronoiMergingAlgorithm:
    """Main algorithm. Parameters is VoronoiMergingAlgorithmParameters """

    def __init__(self, parameters):
        self.parameters = parameters

    def run(self, data, weigths):

        """Points is a collection of Point"""
        return _merge(data, weigths, self.parameters)


class _VoronoiCell:

    """Used to store points in Voronoi cell"""

    def __init__(self, data, weigths):

        """Points is array of Points"""

        self.vector = data
        self.weights = weigths

    def get_coeff_var(self):

        """Get max variance coefficient of Voronoi cell"""

        dimension = len(self.vector[0])
        avg_values = []

        for i in range(0, dimension):
            values_dimension = []
            weights_dimension = []
            for j in range(0, len(self.vector)):
                values_dimension.append(self.vector[j][i])
                weights_dimension.append(self.weights[j])

            std = weighted_std(values_dimension, weights_dimension)
            avg_values.append(std)

        max_idx, max_avg = get_max_coef(avg_values)
        return max_idx, max_avg

    def divide(self, max_idx, max_key):

        """

        Devide Voronoi cell into two Voronoi cells
        max_idx --
        max_key --

        """

        max_value = float("-inf")
        min_value = float("inf")

        for point in self.points[max_key]:
            if max_value < point.coords[max_idx]:
                max_value = point.coords[max_idx]

            if min_value > point.coords[max_idx]:
                min_value = point.coords[max_idx]

        middle_value = (max_value + min_value)/2.

        array_first = {}
        array_secound = {}

        array_first['position'] = []
        array_first['momentum'] = []
        array_secound['position'] = []
        array_secound['momentum'] = []

        for i in range(0, len(self.points[max_key])):
            if self.points[max_key][i].coords[max_idx] > middle_value:
                for keys in self.points:
                       array_first[keys].append(self.points[keys][i])
            else:
                for keys in self.points:
                    array_secound[keys].append(self.points[keys][i])

        first_cell = _VoronoiCell(array_first)
        secound_cell = _VoronoiCell(array_secound)
        return first_cell, secound_cell
        #"""component - index of coordinate to use for subdivision, this function returns two Voronoi Cells"""

    def merge(self):
        """ Merge Voronoi cell into one point """

        dimension = len(self.vector[0])

        self.vector, self.weights = merge_points(dimension, self.vector, self.weights)


def merge_points(dimension, vector, weights_vector):
    """ Merge coordinates into one point """

    values_vector = []
    sum_weights = numpy.sum(weights_vector, dtype=float)

    for i in range(0, dimension):
        value = 0.
        for j in range(0, len(vector)):
            value = value + vector[j][i] * weights_vector[j]
        values_vector.append(float(value / sum_weights))

    return values_vector, sum_weights


def get_max_coef(avg_values):
    """ Find max coefficient of variance """

    max_value = float("-inf")
    max_idx = -1

    for i in range(0, len(avg_values)):
        if avg_values[i] > max_value:
            max_value = avg_values[i]
            max_idx = i

    return max_idx, max_value


def weighted_avg(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.

    """

    average = numpy.average(values, weights=weights)
    # Fast and numerically precise:
    variance = numpy.average((values-average)**2, weights=weights)
    return math.sqrt(variance)


def _merge(data, weigths, parameters):
    """
    Merging algorithm:
    points -- original points
    parametes -- input parameters for Voronoi algorithm(tolerances)

    """
    initial_cell = _VoronoiCell(copy_data, copy_weights)


    result = []
    cells = [initial_cell]

    while len(cells) > 0:
        cell = cells[0]

        max_idx, max_key, max_avg = cell.get_coeff_var()
        needs_subdivision = check_needs_subdivision(parameters, max_avg, max_key)

        if needs_subdivision:

            first_part_cell, secound_part_cell = cell.divide(max_idx, max_key)
            cells.append(secound_part_cell)
            cells.append(first_part_cell)
        else:
            cell.merge()
            new_particle = copy.deepcopy(cell)
            result.append(new_particle)

        cells.remove(cells[0])

    return result


def check_needs_subdivision(parameters, max_avg, max_key):
    """
    Check that Voronoi cell need to devide
    parametrs -- subdivision tolerances
    max_avg -- value of max variance
    max_key -- parameter with max variance

    """

    position_tolerance = parameters.tolerance[0]
    momentum_tolerance = parameters.tolerance[1]

    if max_key == 'position':
        return max_avg > position_tolerance

    if max_key == 'momentum':
        return max_avg > momentum_tolerance

import read_hdf_file
import h5py


class WeightReader():

    def __init__(self):
        self.weight = []

    def __call__(self, name, node):
        if isinstance(node, h5py.Dataset):
            if node.name.endswith('weighting'):
                self.weight = node.value


def compute_weight_sum(weight, values):

    dimension = values.get_dimension()

    sum_x = 0.
    sum_y = 0.
    sum_z = 0.

    if dimension == 3:
        size_of_position = len(values.vector_x)
        for i in range(0, size_of_position):
            sum_x += values.vector_x[i] * weight[i]
            sum_y += values.vector_y[i] * weight[i]
            sum_z += values.vector_z[i] * weight[i]

    elif dimension == 2:
        size_of_position = len(values.vector_x)
        for i in range(0, size_of_position):
            sum_x += values.vector_x[i] * weight[i]
            sum_y += values.vector_y[i] * weight[i]

    return sum_x, sum_y, sum_z


def get_dataset_values(group, name_dataset):

    values = read_hdf_file.DatasetReader(name_dataset)
    group.visititems(values)
    weight_reader = WeightReader()
    group.visititems(weight_reader)

    return weight_reader.weight, values


def count_weight_difference(weight_first, values_first, weight_second, values_second):

    sum_first = compute_weight_sum(weight_first, values_first)

    sum_second = compute_weight_sum(weight_second, values_second)

    for i in range(0, values_first.get_dimension()):
        relative_error = (sum_first[i] - sum_second[i]) / sum_first[i]
        print(relative_error)
        assert math.fabs(relative_error) < 1e-6, "Big relative error, reduction is wrong"

    return sum_first, sum_second


def compute_standard_deviation(weights, coords):

    sum_weights = numpy.sum(weights)
    sum_coords = 0.
    for i in range(0, len(weights)):
        sum_coords += weights[i] * coords[i]

    average_value = sum_coords / sum_weights

def count_weight_momentum_difference(first_group, second_group):

    print('weight momentum')

    hdf_datasets = read_hdf_file.Particles_functor()
    first_group.visititems(hdf_datasets)
    momentum_group_first = hdf_datasets.momentum[0]
    momentum_values_first = read_hdf_file.Dataset_reader('momentum')
    momentum_group_first.visititems(momentum_values_first)
    mass_reader_first = Mass_reader(first_group)
    first_group.visititems(mass_reader_first)

    size_of_positions_first = len(momentum_values_first.vector_x)
    momentum_values_first.get_demention()
    first_mass = convert_mass_to_array(mass_reader_first.mass, size_of_positions_first)
    sum_first = compute_weight_positions_sum(first_mass, momentum_values_first)

    print('first sum == ' + str(sum_first))

def compute_momentum_standart_deviation(weights, momentum_values):

    deviation_values = []
    if momentum_values.get_dimension() == 3:
        deviation_values.append(compute_standard_deviation(weights, momentum_values.vector_x))
        deviation_values.append(compute_standard_deviation(weights, momentum_values.vector_y))
        deviation_values.append(compute_standard_deviation(weights, momentum_values.vector_z))

    if momentum_values.get_dimension() == 2:
        deviation_values.append(compute_standard_deviation(weights, momentum_values.vector_x))
        deviation_values.append(compute_standard_deviation(weights, momentum_values.vector_y))

    return deviation_values


def compare_weight_coordinates(first_hdf_file_name, second_hdf_file_name):


    first_hdf_file = h5py.File(first_hdf_file_name, 'a')
    second_hdf_file = h5py.File(second_hdf_file_name, 'a')

    particles_name_first = read_hdf_file.get_particles_name(first_hdf_file)
    particles_groups_first = read_hdf_file.Particles_groups(particles_name_first)
    first_hdf_file.visititems(particles_groups_first)

    particles_name_second = read_hdf_file.get_particles_name(second_hdf_file)
    particles_groups_second = read_hdf_file.Particles_groups(particles_name_second)
    second_hdf_file.visititems(particles_groups_second)

    size_groups = len(particles_groups_second.particles_groups)


    for i in range(0, size_groups):
        count_weight_coordinates_difference(particles_groups_first.particles_groups[i],
                                            particles_groups_second.particles_groups[i])
        count_weight_momentum_difference(particles_groups_first.particles_groups[i],
                                            particles_groups_second.particles_groups[i])



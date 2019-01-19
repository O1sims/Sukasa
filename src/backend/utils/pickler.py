import pickle as pk

from os.path import isfile
from sukasa.config import BASE_PATH


def save_data_pickle(data, file_name):
    data_file = '{}{}.pickle'.format(
        BASE_PATH, file_name)
    with open(data_file, 'wb') as f:
        pk.dump(data, f,
                protocol=pk.HIGHEST_PROTOCOL)


def load_data_pickle(file_name):
    data_file = '{}{}.pickle'.format(
        BASE_PATH, file_name)
    if isfile(data_file):
        with open(data_file, 'rb') as f:
            return pk.load(f)
    else:
        raise NameError('The file {} was not found!'.format(
            data_file))

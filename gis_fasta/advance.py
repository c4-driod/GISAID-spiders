import pickle
import os


store_folder = '.' + os.sep + 'advance'
file_suffix = '.dat'


def set_advance(filename, ac_nums_list):
    if not os.path.exists(store_folder):
        os.mkdir(store_folder)
    with open(store_folder + os.sep + filename + file_suffix, 'wb') as f:
        data = ac_nums_list
        pickle.dump(data, f)


def get_advance(filename):
    if os.path.exists(store_folder + os.sep + filename + file_suffix):
        with open(store_folder + os.sep + filename + file_suffix, 'rb') as f:
            data = pickle.load(f)
            return data
    else:
        return None


def clear_adv(filename):
    if os.path.exists(store_folder + os.sep + filename + file_suffix):
        os.remove(store_folder + os.sep + filename+file_suffix)

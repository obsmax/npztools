from __future__ import print_function
import numpy as np
from numpy.lib.npyio import _savez
import os

"""
a generalized object to store processing results under conventional npz files
designed to be subclassed in each application for quick display
PYTHON 2/3

11/02/2020
"""


def add_to_npz(npzfile, allow_pickle=False, **kwargs):
    """
    add onei or more field(s) to an existing npzfile (implies loading the existing fields)
    :param npzfile: name of the file to load and write 
    :param kwargs: fields to add or update
    """
    if os.path.isfile(npzfile):

        # load if not in kwargs
        keys = kwargs.keys()
        with np.load(npzfile) as loader:
            loaded = {f: loader[f] for f in loader.files if f not in keys}

        # concatenate
        d = dict(loaded, **kwargs)
        
    else:
        d = kwargs

    # save
    # np.savez(npzfile, **d)
    _savez(npzfile, args=(), kwds=d, compress=True, allow_pickle=allow_pickle)


def loadkeys_from_npz(npzfilename, keys=None, allow_pickle=False):
    """
    :param npzfilename:
    :param keys: keys to load, or None (raise with the list of keys) or "*"
    :param allow_pickle:
    """
    if not npzfilename.endswith(".npz"):
        raise ValueError('filename does not end with .npz')

    kwargs = {}
    with np.load(npzfilename, mmap_mode='r', allow_pickle=allow_pickle) as loader:
        available_keys = loader.files  # nothing loaded yet
        if keys is None:
            raise Exception('please specify at least one key among : {}'.format(available_keys))

        elif keys == "*":
            keys = available_keys

        for key in keys:
            if key not in available_keys:
                raise KeyError('could not find item {} in {},'
                               'available keys are {}'
                               .format(key, npzfilename, available_keys))

            kwargs[key] = loader[key]
    if not len(keys):
        raise Exception('please provide the name of the keys to load or "*"')
    return kwargs


class Container(dict):
    """
    a container is a dict that can be easily saved to npz with or without pickling
    avoiding pickling is safer and less system dependent but prevents from saving complex objects
    (only numpy arrays or built-in objects will be storable)

    I add possibility to easily reload only parts of the file using loadkeys

    Subclass may attach some displaying methods of file format control methods
    """

    def __new__(cls, **kwargs):
        """
        :param kwargs: ignored here, passed to __init__ for affectation
        :return:
        """
        container_instance = super(Container, cls).__new__(cls, {})
        return container_instance

    def __init__(self, **kwargs):
        """use __new__ to subclass, not __init__"""
        super(Container, self).__init__()
        for key, value in kwargs.items():
            self[key] = value

    def savez(self, npzfilename, allow_pickle=False, keys='*', ignore_protected=True):
        """
        :param npzfilename: name of the .npz file to write
        :param allow_pickle: wether to allow pickling
        :param keys: list of keys to save or '*'
        :param ignore_protected: if True, keys starting with "_" won't be saved
        :return:
        """
        if not npzfilename.endswith(".npz"):
            raise ValueError('npzfilename must ends with .npz')
        if isinstance(keys, str):
            if not keys == '*':
                raise ValueError('keys must be a list of keys or "*"')
        elif hasattr(keys, "__iter__"):
            available_keys = self.keys()
            for k in keys:
                if k not in available_keys:
                    raise AttributeError('key {} not found, did you mean {}?'.format(k, available_keys))
        else:
            raise TypeError('keys must be a list of keys or "*"')

        if keys == '*':
            keys = self.keys()

        if ignore_protected:
            # exclude keys starting with "_"
            out = {key: self[key] for key in keys if not key.startswith('_')}
        else:
            out = {key: self[key] for key in keys}

        if allow_pickle:
            np.savez(npzfilename, **out)  # this syntax forces allow_pickle to True
        else:
            # hack to force allow_pickle to False
            _savez(npzfilename, args=(), kwds=out, compress=True, allow_pickle=False)

    def loadkeys(self, npzfilename, keys=None, allow_pickle=False):
        """
        load some attributes from a npz file

        :param npzfilename:
        :param keys: list of key names or '*'
        :param allow_pickle:
        :return:
        """
        loader = loadkeys_from_npz(npzfilename, keys=keys, allow_pickle=allow_pickle)
        for key, value in loader.items():
            self[key] = value

    def __getitem__(self, item):
        """
        intercept user command value = cont['key'] or value = cont.key
        and converts array to scalar if necessary
        :param item:
        :return:
        """
        value = dict.__getitem__(self, item)
        if isinstance(value, np.ndarray) and value.shape == ():
            # scalars are stored as numpy arrays with shape ()
            value = value[()]
        return value

    def __getattr__(self, item):
        """
        self.key <=> self['key']
        """
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        """
        self.key = value <=> self['key'] = value
        """
        self.__setitem__(key, value)

    def __delattr__(self, item):
        """
        del self.key <=> del self['key']
        """
        self.__delitem__(item)

    def __getstate__(self):
        # return dict(self)
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state

    # ================= user section : to custom in subclasses
    def __str__(self):
        """
        define here how the container should be represented in str
        :return:
        """
        raise NotImplementedError('please subclass')

    def show(self, ax, **kwargs):
        """
        define here how the container should be displayed
        :param ax: a matplotlib.axes.Axes object or so
        :param kwargs: kwargs to pass to the display method
        :return: collections or graphic handles ...
        """
        raise NotImplementedError('please subclass')


if __name__ == '__main__':
    a = {"a": np.arange(10), "b": 1., "c": "lkkljlk", 'd': [1, 2, 3],
         'e': {"a": np.arange(10), "b": 1., "c": "lkkljlk", 'd': [1, 2, 3]}}

    cont = Container(**a)

    cont.savez('toto.npz', allow_pickle=True)
    del cont
    cont = Container()
    cont.loadkeys('toto.npz', keys='*', allow_pickle=True)
    print(cont.keys())
    print(cont['a'])
    print(cont['c'])
    print(cont['b'])
    print(cont['d'])
    print(cont['e'])

    print(cont.a)
    cont.a = 123456789.
    print(cont.a)

    del cont.a
    print(cont.b)

    del cont
    cont = Container(scalar=1., array=np.array([1, 2, 3]))
    cont.savez("toto.npz")

    del cont
    cont = Container()
    cont.loadkeys('toto.npz', keys='*')
    print(type(cont.scalar), cont.scalar.shape == ())
    print(type(cont.scalar[()]))

    state = cont.__getstate__()
    print(list(state.items()))


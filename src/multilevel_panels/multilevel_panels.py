import logging
from functools import reduce

import numpy as np

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def setopnd_functor(op):
    """Return a binary function that will perform the passed 1-dimensional set operation on n-dimensional array arguments.
    """
    def setopnd(a, b):
        result = op(
            a.view(
                [('', a.dtype)] * a.shape[1]
            ).ravel(),
            b.view(
                [('', b.dtype)] * b.shape[1]
            ).ravel(),
        )

        return result.view(a.dtype).reshape(-1, a.shape[1])

    return setopnd


intersectnd = setopnd_functor(np.intersect1d)
unionnd = setopnd_functor(np.union1d)
setdiffnd = setopnd_functor(np.setdiff1d)


def intersectml(a, b):
    # TODO: expand to n-tuples
    # a and b are 2-tuples of ndarrays where the first element is the highest (most general) level
    logging.debug(f'a: {a}')
    logging.debug(f'b: {b}')
    a_0, a_1 = a
    b_0, b_1 = b

    intersection_0 = intersectnd(a_0, b_0)
    logging.debug(f'intersection_0: {intersection_0}')
    intersection_1 = intersectnd(a_1, b_1)
    logging.debug(f'intersection_1: {intersection_1}')

    # returns intersecting level 0 results, that need to be "joined" back to the level 1 results
    intersection_0_1 = intersectnd(a_0, b_1[:, :-1])
    logging.debug(f'intersection_0_1: {intersection_0_1}')
    join_0_1 = b_1[np.in1d(b_1[:, :-1], intersection_0_1)]
    logging.debug(f'join_0_1: {join_0_1}')

    intersection_1_0 = intersectnd(a_1[:, :-1], b_0)
    logging.debug(f'intersection_1_0: {intersection_1_0}')
    join_1_0 = a_1[np.in1d(a_1[:, :-1], intersection_1_0)]
    logging.debug(f'join_1_0: {join_1_0}')

    # concatenate and deduplicate the 3 wide arrays
    concat_1 = np.unique(
        np.concatenate(
            (
                intersection_1,
                join_0_1.view(int).reshape((join_0_1.shape[0], 2)),
                join_1_0.view(int).reshape((join_1_0.shape[0], 2)),
            ),
            axis=0,
        ),
        axis=0,
    )
    logging.debug(f'concat_1: {concat_1}')

    return intersection_0, concat_1


def unionml(a, b):
    # a and b are 2-tuples of ndarrays where the first element is the highest (most general) level
    # TODO: expand to n-tuples
    logging.debug(f'a: {a}')
    logging.debug(f'b: {b}')
    a_0, a_1 = a
    b_0, b_1 = b

    union_0 = unionnd(a_0, b_0)
    logging.debug(f'union_0: {union_0}')
    union_1 = unionnd(a_1, b_1)
    logging.debug(f'union_1: {union_1}')

    join_1 = union_1[np.in1d(union_1[:, :-1], union_0.view(int).reshape((union_0.shape[0], -1)))]
    logging.debug(f'join_1: {join_1}')

    setdiff_1 = setdiffnd(union_1, join_1)
    logging.debug(f'setdiff_1: {setdiff_1}')

    return union_0, setdiff_1


def unionml2(a, b):
    # if a.shape[1] != b.shape[1]:
    #     raise ValueError

    if a[0].shape[1] == 0:
        return list()

    else:
        logging.debug(f'a: {a}')
        logging.debug(f'b: {b}')

        a_0, a_1 = a[-2:]
        b_0, b_1 = b[-2:]

        union_0 = unionnd(a_0, b_0)
        logging.debug(f'union_0: {union_0}')
        union_1 = unionnd(a_1, b_1)
        logging.debug(f'union_1: {union_1}')

        join_1 = union_1[np.in1d(union_1[:, :-1], union_0.view(int).reshape((union_0.shape[0], -1)))]
        logging.debug(f'join_1: {join_1}')

        setdiff_1 = setdiffnd(union_1, join_1)
        logging.debug(f'setdiff_1: {setdiff_1}')

        return unionml2(a[:-1], b[:-1]) + [(union_0, setdiff_1)]


def decompose(arr):
    if arr.shape[1] == 0:
        return tuple()
    else:
        nan_bool_idx = np.isnan(arr).any(axis=1)
        return decompose(arr[nan_bool_idx, :-1]) + (arr[~ nan_bool_idx, :].astype(int), )


def recompose(tup):
    pad_width = tup[-1].shape[1]

    return np.concatenate(
        tuple(
            np.pad(t.astype(float), ((0, 0), (0, pad_width - t.shape[1])), mode='constant', constant_values=np.nan) for t in tup
        )
    )


class MultilevelPanel:
    def __init__(self, arr):
        self.arr = arr

    def __getitem__(self, item):
        return decompose(self.arr)[item]

    def __eq__(self, other):
        # __ne__ is implicit in Python 3, but would need to be defined in Python 2
        # note that this does not guarantee the compared items are in the same order
        if not isinstance(other, type(self)):
            raise TypeError
        else:
            return all(np.all(s == o) for s, o in zip(decompose(self.arr), decompose(other.arr)))

    def intersect1(self, other):
        return type(self)(recompose(intersectml(self, other)))

    def union1(self, other):
        return type(self)(recompose(unionml(self, other)))

    def intersectn(self, *others):
        return type(self)(
            recompose(
                reduce(
                    intersectml,
                    (self, *others)
                )
            )
        )

    def unionn(self, *others):
        return type(self)(
            recompose(
                reduce(
                    unionml,
                    (self, *others)
                )
            )
        )


# 1. intersect/union lowest level / widest array
# 2. intersect/union next level / next widest array
# ... repeat until there is no more array
# 3. I/U LHS width - 1 with RHS width (will either produce an array of width, or width - 1)
# 4. I/U RHS width - 1 with LHS width (will either produce an array of width, or width - 1)
# 5. reconcile the four resulting arrays:
    # a. if I, results must be as specific as possible (i.e., width takes precedence over width - 1)
    # b. if U, results must be as general as possible (i.e., width - 1 takes precedence over width)

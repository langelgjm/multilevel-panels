import pytest

from multilevel_panels import *

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = np.array([[1, 2, 3], [6, 5, 4]])
c = np.array([[1, 2, 3], [9, 8, 7]])


@pytest.mark.parametrize(
    'op,args,expected',
    (
        (np.intersect1d, (a, b), np.array([[1, 2, 3]])),
        (np.union1d, (a, b), np.array([[1, 2, 3], [4, 5, 6], [6, 5, 4], [7, 8, 9]])),
        (np.setdiff1d, (a, b), np.array([[4, 5, 6], [7, 8, 9]])),
        (np.setxor1d, (a, b), np.array([[4, 5, 6], [6, 5, 4], [7, 8, 9]])),
    )
)
def test_setopnd_functor(op, args, expected):
    func = setopnd_functor(op)
    result = func(*args)
    np.testing.assert_array_equal(expected, result)


A = MultilevelPanel(
    np.array(
        [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [2, 0],
            [3, np.nan],
            [4, 0],
            [4, 1],
            [5, np.nan],
            [7, np.nan],
        ]
    )
)

B = MultilevelPanel(
    np.array(
        [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [2, 1],
            [3, 0],
            [3, 1],
            [4, np.nan],
            [6, np.nan],
            [7, np.nan],
        ]
    )
)

C = MultilevelPanel(
    np.array(
        [
            [0, 0],
            [1, 1],
            [2, 1],
            [3, 0],
            [3, 1],
            [7, np.nan],
            [8, 0],
            [8, 1],
            [9, np.nan],
        ]
    )
)

AB_intersect = MultilevelPanel(
    np.array(
        [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [3, 0],
            [3, 1],
            [4, 0],
            [4, 1],
            [7, np.nan],
        ]
    )
)

AB_union = MultilevelPanel(
    np.array(
        [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [2, 0],
            [2, 1],
            [3, np.nan],
            [4, np.nan],
            [5, np.nan],
            [6, np.nan],
            [7, np.nan],
        ]
    )
)


ABC_intersect = MultilevelPanel(
    np.array(
        [
            [0, 0],
            [1, 1],
            [3, 0],
            [3, 1],
            [7, np.nan],
        ]
    )
)

ABC_union = MultilevelPanel(
    np.array(
        [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [2, 0],
            [2, 1],
            [3, np.nan],
            [4, np.nan],
            [5, np.nan],
            [6, np.nan],
            [7, np.nan],
            [8, 0],
            [8, 1],
            [9, np.nan],
        ]
    )
)


def set_random_nans(arr, p=0.5, from_col=1):
    """Set sequential right-hand-side elements of rows (selected with probability `p`) of a 2-d array to NaN.
    Elements in columns <= `from_col` will not be set.
    """
    if arr.shape[1] == from_col:
        return arr
    else:
        rand_bool_idx = np.random.choice([True, False], size=arr.shape[0], p=(p, 1 - p))
        nan_padded_subset = np.hstack(
            (
                set_random_nans(arr[rand_bool_idx, :-1], p=p, from_col=from_col),
                np.full((rand_bool_idx.sum(), 1), fill_value=np.nan)
            )
        )

        return np.concatenate(
            (
                arr[~ rand_bool_idx],
                nan_padded_subset,
            )
        )


def get_random_mlp(size=(100_000, 2)):
    arr = np.unique(np.random.randint(10000, size=size).astype(float), axis=1)

    return MultilevelPanel(set_random_nans(arr))


def test_intersectml():
    result_0, result_1 = intersectml(A, B)

    np.testing.assert_array_equal(AB_intersect[0], result_0)
    np.testing.assert_array_equal(AB_intersect[1], result_1)


def test_unionml():
    result_0, result_1 = unionml(A, B)

    np.testing.assert_array_equal(AB_union[0], result_0)
    np.testing.assert_array_equal(AB_union[1], result_1)


class TestMultilevelPanel:
    def test_intersect1(self):
        assert A.intersect1(B) == AB_intersect
        assert A.intersect1(B).intersect1(C) == ABC_intersect

    def test_union1(self):
        assert A.union1(B) == AB_union
        assert A.union1(B).union1(C) == ABC_union

    def test_intersectn(self):
        assert A.intersectn(B, C) == ABC_intersect

    def unionn(self):
        assert A.unionn(B, C) == ABC_intersect


@pytest.mark.skip
class TestSetOperationPerformance:
    def test_intersect(self):
        result_0, result_1 = intersectml(get_random_mlp(), get_random_mlp())

        assert not np.isnan(result_0).any()
        assert not np.isnan(result_1).any()
        # assert not np.in1d(result_0, result_1[:, :-1]).any()

        logging.info(
            result_0.shape,
            result_1.shape,
        )

    def test_union(self):
        result_0, result_1 = unionml(get_random_mlp(), get_random_mlp())

        assert not np.isnan(result_0).any()
        assert not np.isnan(result_1).any()
        # assert not np.in1d(result_0, result_1[:, :-1]).any()

        logging.info(
            result_0.shape,
            result_1.shape,
        )


def test_decompose_and_recompose():
    arr = np.tril(np.ones((3, 3)))
    arr[arr == 0] = np.nan

    expected = (
        np.array([[1]]),
        np.array([[1, 1]]),
        np.array([[1, 1, 1]]),
    )

    decomposed = decompose(arr)

    for e, r in zip(expected, decomposed):
        np.testing.assert_array_equal(e, r)

    recomposed = recompose(decomposed)

    for e, r in zip(arr, recomposed):
        np.testing.assert_array_equal(e, r)

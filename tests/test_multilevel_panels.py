import pytest

from multilevel_panels import *

# for testing set operations
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = np.array([[1, 2, 3], [6, 5, 4]])
c = np.array([[1, 2, 3], [9, 8, 7]])

# for testing multilevel panels with length 2 elements
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

# for testing multilevel panels with length 3 elements
X = MultilevelPanel(
    np.array(
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 2],
            [1, 0, 0],
            [1, 0, 1],
            [1, 0, 2],
            [2, 0, 0],
            [3, 0, np.nan],
            [4, np.nan, np.nan],
            [5, 0, np.nan],
            [6, np.nan, np.nan],
        ]
    )
)

Y = MultilevelPanel(
    np.array(
        [
            [0, 0, 0],
            [0, 0, 2],
            [1, 1, 0],
            [1, 0, 1],
            [1, 1, 2],
            [2, 0, np.nan],
            [3, 0, 0],
            [3, 0, 1],
            [3, 1, 0],
            [4, np.nan, np.nan],
            [5, 0, np.nan],
            [7, np.nan, np.nan],
        ]
    )
)

Z = MultilevelPanel(
    np.array(
        [
            [0, 0, np.nan],
            [1, 1, 1],
            [2, 1, 2],
            [3, 0, 3],
            [3, 1, 3],
            [7, np.nan, np.nan],
            [8, 0, 8],
            [8, 1, 8],
            [9, np.nan, np.nan],
        ]
    )
)

XY_intersect = MultilevelPanel(
    np.array(
        [
            [0, 0, 0],
            [0, 0, 2],
            [1, 0, 1],
            [2, 0, 0],
            [3, 0, 0],
            [3, 0, 1],
            [4, np.nan, np.nan],
            [5, 0, np.nan],
        ]
    )
)

XY_union = MultilevelPanel(
    np.array(
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 2],
            [1, 0, 0],
            [1, 0, 1],
            [1, 0, 2],
            [1, 1, 0],
            [1, 1, 2],
            [2, 0, np.nan],
            [3, 0, np.nan],
            [3, 1, 0],
            [4, np.nan, np.nan],
            [5, 0, np.nan],
            [6, np.nan, np.nan],
            [7, np.nan, np.nan],
        ]
    )
)

XYZ_intersect = MultilevelPanel(
    np.array(
        [
            [0, 0, 0],
            [0, 0, 2],
            [7, np.nan, np.nan],
        ]
    )
)

XYZ_union = MultilevelPanel(
    np.array(
        [
            [0, 0, np.nan],
            [1, 0, 0],
            [1, 0, 1],
            [1, 0, 2],
            [1, 1, 0],
            [1, 1, 1],
            [1, 1, 2],
            [2, 0, np.nan],
            [2, 1, 2],
            [3, 0, np.nan],
            [3, 1, 0],
            [3, 1, 3],
            [4, np.nan, np.nan],
            [5, 0, np.nan],
            [6, np.nan, np.nan],
            [7, np.nan, np.nan],
            [8, 0, 8],
            [8, 1, 8],
            [9, np.nan, np.nan],
        ]
    )
)

# for testing multilevel panels with 4 elements
M = MultilevelPanel(
    np.array(
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [2, 2, 2, np.nan],
            [3, 3, np.nan, np.nan],
            [4, np.nan, np.nan, np.nan],
        ]
    )
)

N = MultilevelPanel(
    np.array(
        [
            [0, 0, 0, 0],
            [2, 2, 2, 2],
            [3, 3, 3, np.nan],
            [4, 4, np.nan, np.nan],
            [5, np.nan, np.nan, np.nan],
        ]
    )
)

MN_intersect = MultilevelPanel(
    np.array(
        [
            [0, 0, 0, 0],
            [2, 2, 2, 2],
            [3, 3, 3, np.nan],
            [4, 4, np.nan, np.nan],
        ]
    )
)

MN_union = MultilevelPanel(
    np.array(
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [2, 2, 2, np.nan],
            [3, 3, np.nan, np.nan],
            [4, np.nan, np.nan, np.nan],
            [5, np.nan, np.nan, np.nan],
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


def get_random_mlp(size, n):
    arr = np.random.randint(n, size=size).astype(float)
    rand_nan_arr = set_random_nans(arr)

    return MultilevelPanel(
        recompose(
            decompose(
                rand_nan_arr,
                assume_unique=False,
            )
        )
    )


@pytest.mark.parametrize(
    'op,args,expected',
    (
        (np.intersect1d, (a, b, c), np.array([[1, 2, 3]])),
        (np.union1d, (a, b, c), np.array([[1, 2, 3], [4, 5, 6], [6, 5, 4], [7, 8, 9], [9, 8, 7]])),
        (np.setdiff1d, (a, b, c), np.array([[4, 5, 6], [7, 8, 9]])),
    )
)
def test_setop2d_variadic_functor(op, args, expected):
    func = setop2d_variadic_functor(op)
    result = func(*args)
    np.testing.assert_array_equal(expected, result)


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


class TestMultilevelPanel:
    def test_flatten(self):
        arr = np.array(
            [
                [0, 0],
                [1, np.nan],
            ]
        )

        mlp = MultilevelPanel(arr)

        np.testing.assert_array_equal(
            np.sort(arr, axis=0),
            np.sort(mlp.flatten(), axis=0)
        )

    def test_intersect(self):
        assert A == A.intersect(A)
        assert AB_intersect == A.intersect(B)
        assert ABC_intersect == A.intersect(B, C)

        assert X == X.intersect(X)
        assert XY_intersect == X.intersect(Y)
        assert XYZ_intersect == X.intersect(Y, Z)

        assert MN_intersect == M.intersect(N)
        assert MN_intersect == N.intersect(M)

    def test_union(self):
        assert A == A.union(A)
        assert AB_union == A.union(B)
        assert ABC_union == A.union(B, C)

        assert X == X.union(X)
        assert XY_union == X.union(Y)
        assert XYZ_union == X.union(Y, Z)

        assert MN_union == M.union(N)
        assert MN_union == N.union(M)

    def test_empty_intersection(self):
        expected = np.empty([0, 4])

        mlp1 = MultilevelPanel(
            np.array(
                [
                    [0, 0, 0, 0],
                ]
            )
        )

        mlp2 = MultilevelPanel(
            np.array(
                [
                    [1, 1, 1, 1],
                ]
            )
        )

        result = mlp1.intersect(mlp2)
        np.testing.assert_array_equal(expected, result.flatten())

    def test_level_skipping_raises(self):
        D = MultilevelPanel(
            np.array(
                [
                    [1, np.nan, np.nan],
                ]
            )
        )

        E = MultilevelPanel(
            np.array(
                [
                    [1, 6, 4],
                    [1, 7, 4],
                ]
            )
        )

        with pytest.raises(NotImplementedError):
            assert D == D.union(E)

        with pytest.raises(NotImplementedError):
            assert E == D.intersect(E)


@pytest.mark.parametrize(
    'bool_lst,expected',
    (
        ([], False),
        ([False], False),
        ([False, False], False),
        ([False, True], False),
        ([True, False], False),
        ([False, False, False], False),
        ([False, False, True], False),
        ([False, True, False], False),
        ([False, True, True], False),
        ([True, False, False], False),
        ([True, False, True], True),
        ([True, True, False], False),
        ([True, True, True], False),
        ([False, True, False, True], True),
        ([True, True, False, True], True),
        ([True, False, True, False], True),
        ([True, False, True, True], True),
        ([True, True, True, True], False),
        ([True, False, False, True], True),
        ([True, False, False, False, True], True),
    )
)
def test_hasgaps(bool_lst, expected):
    assert expected == hasgaps(bool_lst)


@pytest.mark.skip
class TestMultilevelPanelPerformance:
    size = (100_000, 3)
    n = 100_000

    def test_intersect(self):
        result = get_random_mlp(self.size, self.n).intersect(get_random_mlp(self.size, self.n)).flatten()
        logging.info(result.shape)

    def test_union(self):
        result = get_random_mlp(self.size, self.n).union(get_random_mlp(self.size, self.n)).flatten()
        logging.info(result.shape)

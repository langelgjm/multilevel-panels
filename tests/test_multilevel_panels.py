from multilevel_panels import *

a = np.array([[3, 1, 2], [5, 8, 9], [7, 4, 3]])

b = np.array([[2, 3, 0], [3, 1, 2], [7, 4, 3]])

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


def get_random_mlp(levels=2):
    arr = np.unique(np.random.randint(1000, size=(100_000, levels)).astype(float), axis=0)
    arr[arr == np.random.randint(1000)] = np.nan
    # TODO: not actually likely to be a valid mlp
    return MultilevelPanel(arr)


def test_intersectml():
    result_0, result_1 = intersectml(A, B)

    np.testing.assert_array_equal(AB_intersect[0], result_0)
    np.testing.assert_array_equal(AB_intersect[1], result_1)


def test_unionml():
    result_0, result_1 = unionml(A, B)

    np.testing.assert_array_equal(AB_union[0], result_0)
    np.testing.assert_array_equal(AB_union[1], result_1)


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


def test_zero_to_ith_col_no_nans():
    z = np.tril(np.ones((3, 3)))
    z[z == 0] = np.nan

    expected = (
        np.array([[1]]),
        np.array([[1, 1]]),
        np.array([[1, 1, 1]]),
    )

    result = zero_to_ith_col_no_nans(z)

    for e, r in zip(expected, result):
        np.testing.assert_array_equal(e, r)

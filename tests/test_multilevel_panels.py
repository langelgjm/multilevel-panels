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

A_intersect_B = MultilevelPanel(
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

A_union_B = MultilevelPanel(
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

x = np.random.randint(1000, size=(100_000, 2)).astype(float)
x[x == np.random.randint(1000)] = np.nan
X = MultilevelPanel(x)

y = np.random.randint(1000, size=(100_000, 2)).astype(float)
y[y == np.random.randint(1000)] = np.nan
Y = MultilevelPanel(y)


def test_intersectml():
    result_0, result_1 = intersectml(
        (A.arr_0, A.arr_1),
        (B.arr_0, B.arr_1),
    )

    np.testing.assert_array_equal(A_intersect_B.arr_0, result_0)
    np.testing.assert_array_equal(A_intersect_B.arr_1, result_1)


def test_unionml():
    result_0, result_1 = unionml(
        (A.arr_0, A.arr_1),
        (B.arr_0, B.arr_1),
    )

    np.testing.assert_array_equal(A_union_B.arr_0, result_0)
    np.testing.assert_array_equal(A_union_B.arr_1, result_1)


class TestSetOperationPerformance:
    # TODO: add some assertions that no arr0 values are in arr1
    def test_intersect(self):
        result_0, result_1 = intersectml((X.arr_0, X.arr_1), (Y.arr_0, Y.arr_1))
        logging.info(
            result_0.shape,
            result_1.shape,
        )

    def test_union(self):
        result_0, result_1 = unionml((X.arr_0, X.arr_1), (Y.arr_0, Y.arr_1))
        logging.info(
            result_0.shape,
            result_1.shape,
        )

# Multilevel Panels

This package provides a class with methods to perform special hierarchy-preserving set operations on hierarchically organized data.

Examples of such hierarchically organized data include:

* genus, species
* countries, regions, cities
* treatment/control group, subject, observation date

Such data are sometimes referred to as multilevel or nested and are commonly encountered in social sciences.

By 'hierarchy-preserving set operations', we mean the following:
* when a row is intersected with another row that contains partially matching but less specific data, the row with more specific data is the result
* when a row is unioned with another row that contains partially matching but less specific data, the row with less specific data is the result

For example, assume the following two datasets, where the first column specifies genus, and the second column species.
`None` is used as a sentinel value to indicate "any".

    A = [
        ('Felis', 'silvestris'),
        ('Canis', 'lupus'),
        ('Homo', None),
        ('Ovis', None),
    ]
    
    B = [
        ('Felis', 'silvestris'),
        ('Homo', 'sapiens'),
        ('Homo', 'neanderthalensis'),
        ('Ovis', None),
    ]

Then we define `A ∩ B` to be:

    {
        ('Felis', 'silvestris'),
        ('Homo', 'sapiens'),
        ('Homo', 'neanderthalensis'),
        ('Ovis', None),
    }

And  `A ∪ B` to be:

    {
        ('Felis', 'silvestris'),
        ('Canis', 'lupus'),
        ('Homo', None),
        ('Ovis', None),
    }

As expected, the order of operands does not matter: `A ∩ B = B ∩ A` and `A ∪ B = B ∪ A`.
However, the order of the rows in the result is not guaranteed.

See the included [example](examples/example.py) for more information.

## Assumptions

* Input data must be 2-dimenisonal integer or floating point `numpy.ndarray` arrays.
    * It is trivial to convert non-numeric data to this format; see the included [example](examples/example.py).
* The special value `NaN` is a sentinel indicating a wildcard; it will match any other value in the same hierarchical path.
* Each input array's rows must be unique.
* The hierarchy is assumed to flow from left to right; i.e., the _0_-th column must contain the highest level of the hierarchy.
* If a value in a row of the hierarchy is `NaN`, all remaining values in the row must be `NaN`.
    * I.e.`(1., NaN, NaN)` is permitted, but `(1., NaN, 1.)` is not.
* Operations must be performed on arrays with equal numbers of columns.

## Usage

See the included [example](examples/example.py) for usage examples.

### Installation

Running `make install` will `pip install` the package into the current environment.

### Running Tests

Run `make develop` followed by `make test`.

## Algorithm

1. Decompose input arrays of width _c_ into _c_ arrays of widths `[1, c]`.
    * If `n ∈ [1, c]`, then the _n_-th array contains input rows of width _n_ whose original values in columns > _n_ contained only `NaN`.
    * Some of these _c_ arrays may be empty.

1. Intersect or union the arrays of width _c_, preserving hierarchy by examining values in the arrays of width  _c - 1_.
1. Concatenate and deduplicate these results as needed.
1. Recurse to step 2 with arrays of width  _c - 1_. When the base case is reached, return.

## Performance

This implementation can perform intersections and unions on datasets of shape `(100,000, 3)` in approximately 1 second on a MacBook Pro (Retina, 13-inch, Early 2015).

## Known Limitations

### Level Skipping

Input data containing rows that "skip" an intervening level of the hierarchy is not correctly handled. Such cases are detected and raise an exception. See the [test suite](tests/test_multilevel_panels.py) for an example.

This limitation only affects panels with > 2 columns.

## License

© 2018 [Gabriel J. Michael](http://www.gabrieljmichael.com)

This software is distributed under the MIT License. See the [license file](LICENSE.txt) for details.
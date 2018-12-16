# Multilevel Panels

This package provides a class with methods to perform special hierarchy-preserving set operations on hierarchically organized data.

Examples of such data include:

* countries, regions, cities
* genus, species
* treatment/control group, subject, observation date

By 'hierarchy-preserving', we mean the following:
* when a row is intersected with another row that contains partially matching but less specific data, the row with more specific data is the result
* when a row is unioned with another row that contains partially matching but less specific data, the row with less specific data is the result

## Algorithm

1. intersect/union lowest level / widest array
1. intersect/union next level / next widest array
    ... repeat until there is no more array
1. I/U LHS width - 1 with RHS width (will either produce an array of width, or width - 1)
1. I/U RHS width - 1 with LHS width (will either produce an array of width, or width - 1)
1. reconcile the four resulting arrays:
    1. if I, results must be as specific as possible (i.e., width takes precedence over width - 1)
    1. if U, results must be as general as possible (i.e., width - 1 takes precedence over width)

## Assumptions

* numerical values (floats) only
* input rows are unique


## Known Bugs and Limitations

Currently, input data that "skips" a level of specificity is not correctly handled. See the test suite for an example.
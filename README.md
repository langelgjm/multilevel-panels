# Multilevel Panels

This package provides a class with methods to perform special hierarchy-preserving set operations on hierarchically organized data.

Examples of such data include:

* countries, regions, cities
* genus, species
* treatment/control group, subject, observation date

By 'hierarchy-preserving', we mean the following:
* when a row is intersected with another row that contains partially matching but less specific data, the row with more specific data is the result
* when a row is unioned with another row that contains partially matching but less specific data, the row with less specific data is the result

## Known Bugs and Limitations

Currently, input data that "skips" a level of specificity is not correctly handled. See the test suite for an example.
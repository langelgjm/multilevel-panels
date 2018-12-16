from typing import Mapping, Sequence

import pandas as pd

from multilevel_panels import MultilevelPanel


known = [
    ('Felis', 'silvestris'),
    ('Canis', 'lupus'),
    ('Homo', None),
    ('Panthera', 'leo'),
    ('Panthera', 'tigris'),
    ('Bos', 'taurus'),
    ('Ovis', None),
]

candidate = [
    ('Felis', 'silvestris'),
    ('Canis', 'aureus'),
    ('Homo', 'sapiens'),
    ('Homo', 'neanderthalensis'),
    ('Homo', 'habilis'),
    ('Panthera', None),
    ('Capra', 'aegagrus'),
    ('Ovis', None),
]


def make_categorical_codes(*args: pd.DataFrame) -> Sequence[Sequence[Mapping]]:
    """Concatenate the passed arguments into a single DataFrame, convert each column to categorical, and return two
    sequences of sequences. Each element of an inner sequence is a mapping corresponding to the columns in the
    concatenated dataframe. The first sequence contains a sequence of mappings of categorical values to numerical codes,
    and the second sequence contains a sequence of mappings of numerical codes to categorical values.
    """
    # get categorical codes for the unique set of values in each column across both datasets
    df = pd.concat(args).astype('category')

    cat_to_code = tuple(
        {v: k for k, v in enumerate(df[col].cat.categories)} for col in df
    )
    code_to_cat = tuple(
        dict(enumerate(df[col].cat.categories)) for col in df
    )

    return cat_to_code, code_to_cat


def categorical_df_to_mlp(df: pd.DataFrame, cat_to_code: Sequence[Mapping]) -> MultilevelPanel:
    return MultilevelPanel(
        pd.concat(
            [df[i].map(cat_to_code[i]) for i in range(df.shape[1])],
            axis=1
        ).values
    )


def mlp_to_categorical_df(mlp: MultilevelPanel, code_to_cat: Sequence[Mapping]) -> pd.DataFrame:
    df = pd.DataFrame(mlp.flatten())

    return pd.concat(
        [df[i].map(code_to_cat[i]) for i in range(df.shape[1])],
        axis=1,
    )


def main():
    """
    # get the codes
    >>> cat_to_code, code_to_cat = make_categorical_codes(pd.DataFrame(known), pd.DataFrame(candidate))

    # convert the datasets to multilevel panels
    >>> known_mlp = categorical_df_to_mlp(pd.DataFrame(known), cat_to_code)
    >>> candidate_mlp = categorical_df_to_mlp(pd.DataFrame(candidate), cat_to_code)

    # what is the intersection between the known data and the candidate data?
    >>> known_mlp.intersect(candidate_mlp)
    [[ 5. nan]
     [ 3.  7.]
     [ 4.  2.]
     [ 4.  5.]
     [ 4.  6.]
     [ 6.  3.]
     [ 6.  9.]]

    # convert the numerical codes back to categories
    >>> mlp_to_categorical_df(known_mlp.intersect(candidate_mlp), code_to_cat)
              0                 1
    0      Ovis               NaN
    1     Felis        silvestris
    2      Homo           habilis
    3      Homo  neanderthalensis
    4      Homo           sapiens
    5  Panthera               leo
    6  Panthera            tigris

    # note that:
    # - genus/species pairs are intersected normally
    # - a genus without a species matches any genus/species pair of the same genus
    # -- the result of such matches only includes genus/species pairs
    # - a genus without a species matches the same genus without a species
    # - matching occurs in both directions
    # - the output rows are unordered

    # what is the union of the known data and the candidate data?
    >>> known_mlp.union(candidate_mlp)
    [[ 4. nan]
     [ 5. nan]
     [ 6. nan]
     [ 0.  8.]
     [ 1.  1.]
     [ 1.  4.]
     [ 2.  0.]
     [ 3.  7.]]

    # convert the numerical codes back to categories
    >>> mlp_to_categorical_df(known_mlp.union(candidate_mlp), code_to_cat)
              0           1
    0      Homo         NaN
    1      Ovis         NaN
    2  Panthera         NaN
    3       Bos      taurus
    4     Canis      aureus
    5     Canis       lupus
    6     Capra    aegagrus
    7     Felis  silvestris

    # note that:
    # - genus/species pairs are unioned normally
    # - a genus without a species matches any genus/species pair of the same genus
    # -- the result of such matches only includes genus without species
    # - a genus without a species matches the same genus without a species
    # - matching occurs in both directions
    # - the output rows are unordered
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

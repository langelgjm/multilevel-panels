import pandas as pd

from multilevel_panels import MultilevelPanel


authorized = [
    ('United States', 'Maryland', 'Baltimore'),
    ('United States', 'Connecticut', None),
    ('Chile', 'Metropolitana', 'Santiago'),
    ('Chile', 'Coquimbo', 'La Serena'),
    ('France', "Île-de-France", None),
]

locations = [
    ('United States', 'Alaska', 'Anchorage'),
    ('United States', 'Connecticut', 'New Haven'),
    ('Chile', 'Magallanes', None),
    ('France', "Île-de-France", 'Paris'),
    ('France', "Provence-Alpes-Côte d'Azur", 'Nice'),
    ('Singapore', None, None),
]

# get categorical codes for the unique set of values in each column across both datasets
df = pd.concat(
    [
        pd.DataFrame(authorized),
        pd.DataFrame(locations),
    ]
).astype('category')

# extract the codes
code_to_cat = tuple(
    dict(enumerate(df[col].cat.categories)) for col in df
)
cat_to_code = tuple(
    {v: k for k, v in enumerate(df[col].cat.categories)} for col in df
)


# map the string values to their corresponding codes
def categories_to_codes(df, codes):
    return MultilevelPanel(
        pd.concat(
            [df[i].map(codes[i]) for i in range(df.shape[1])],
            axis=1
        ).values
    )


# map the codes to their corresponding string values
def codes_to_categories(mlp, codes):
    df = pd.DataFrame(mlp.flatten())

    return pd.concat(
        [df[i].map(codes[i]) for i in range(df.shape[1])],
        axis=1,
    )


authorized_mlp = categories_to_codes(pd.DataFrame(authorized), cat_to_code)
locations_mlp = categories_to_codes(pd.DataFrame(locations), cat_to_code)

# produces information about which locations are authorized, either directly or at a higher level
codes_to_categories(authorized_mlp.intersect(locations_mlp), code_to_cat)

# produces the distinct set of locations, eliminating lower levels when they are subsumed by a higher level
codes_to_categories(authorized_mlp.union(locations_mlp), code_to_cat)

import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):

    # Specify your data loading logic here
    url = 'https://github.com/YoItsYong/billboard-200-pipeline/raw/main/data/billboard200_albums.csv.gz'

    df = pd.read_csv(url)
    print(df.dtypes)
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

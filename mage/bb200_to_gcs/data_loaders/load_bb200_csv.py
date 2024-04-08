import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    
    url = 'https://github.com/YoItsYong/billboard-200-pipeline/raw/main/data/billboard200_albums.csv.gz'

    df = pd.read_csv(url)
    print(df.dtypes)
    
    return df
import gzip
import shutil

albums_input = 'albums.csv'
albums_output = 'billboard200_albums.csv.gz'

acoustic_features_input = 'acoustic_features.csv'
acoustic_features_output = 'billboard200_features.csv.gz'

with open(acoustic_features_input, 'rb') as f_in:
    with gzip.open(acoustic_features_output, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
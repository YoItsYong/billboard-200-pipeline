"""
This file takes the resulting albums.csv file from the sqlite_to_csv.py script and compresses it further into a .csv.gz file
for the sake of conserving space.
"""
import gzip
import shutil

# albums.csv should be one of the resulting files of running sqllite_to_csv.py
albums_input = 'albums.csv'
albums_output = 'billboard200_albums.csv.gz'

acoustic_features_input = 'acoustic_features.csv'
acoustic_features_output = 'billboard200_features.csv.gz'

with open(acoustic_features_input, 'rb') as f_in:
    with gzip.open(acoustic_features_output, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
#!/usr/bin/env python
# coding: utf-8

import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.types import StringType, DateType, FloatType, IntegerType

parser = argparse.ArgumentParser()

parser.add_argument('--input_albums', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

input_albums = args.input_albums
output = args.output

spark = SparkSession.builder \
    .appName('spark_dataproc') \
    .getOrCreate()

#Replace temp_gcs_bucket with the name of your temporary bucket in GCS
temp_gcs_bucket = 'dataproc-temp-us-central1-692387679074-vn8xcn04'
spark.conf.set('temporaryGcsBucket', temp_gcs_bucket)

df = spark.read.parquet('gs://bb200/bb200_albums.parquet')

# Transformations
# Manage column dtypes
df = df \
    .withColumn('date', df['date'].cast(DateType())) \
    .withColumn('rank', df['rank'].cast(IntegerType())) \
    .withColumn('length', df['length'].cast(IntegerType()))

# Rename 'length' to 'number_of_tracks'
df = df \
    .withColumnRenamed('length', 'number_of_tracks')

# Handle null values
df = df.na.fill(value=0, subset=['number_of_tracks'])
df = df.na.fill(value=0, subset=['track_length'])

# Skip null values in first row
df = df.filter(df.id > 1)

df.registerTempTable('bb200_albums')

df_result = spark.sql("""
SELECT
    rank,
    date,
    artist,
    album,
    number_of_tracks,
    CONCAT(
        LPAD(FLOOR(track_length / 60000), 2, 0),
        ':',
        LPAD(FLOOR((track_length % 60000) / 1000), 2, 0)
        ) AS track_length
FROM
    bb200_albums
    """)

df.write.format('bigquery') \
    .option('table', output) \
    .save()


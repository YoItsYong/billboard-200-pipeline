import os
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(data, *args, **kwargs):
    # Specify your data exporting logic here
    os.system("""
    ./gsutil/google-cloud-sdk/bin/gcloud dataproc jobs submit pyspark \
        --project=INSERT_PROJECT_NAME \
        --cluster=music-chart-cluster \
        --region=us-central1 \
        --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.23.2.jar \
    gs://bb200/code/spark_dataproc.py \
        -- \
            --input_albums=gs://bb200/bb200_albums.parquet \
            --output=bb200_data.bb200_albums
    """)



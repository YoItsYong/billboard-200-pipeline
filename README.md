# Billboard 200 Music Chart Data Pipeline
## Introduction
The Billboard 200 is a weekly music chart that measures the top selling (or streaming) albums in the United States. Placing at the top of the chart has historically been a marker of a release's success and can often be an important factor in how an artist defines their legacy.

## Objective
While the Billboard 200 has been around since the 1940s, how we listen to and connect with music has evolved over the years. This project creates an end-to-end data pipeline to ingest existing Billboard 200 data from 1963 - 2019 to analyze and visualize the trends in charting artists over the years.

## Technologies
To create this pipeline, I used a variety of technologies to extract, transform, and load the data to the cloud, where it could be easily accesible for analysis. These technologies include:
- Infrastructure as Code (IaC): Terraform
- Containerization: Docker
- Cloud: Google Cloud Platform (GCP)
- Data Lake: Google Cloud Storage
- Data Warehouse: Google BigQuery
- Batch Processing: Apache Spark (PySpark)
- Workflow Orchestration: Mage
- Visualization: Google Data Studio

< Insert diagram here >

## Data Pipeline
### Preparing the Data
The data set orginates from [Components.one](https://www.dropbox.com/s/ahog97hcatpiddk/billboard-200.db?dl=1), a research platform that makes its data sets publicly available for use. The data from this site first comes in the form of a `.db` file, which is most commonly used with SQLite. Because this is not a file type I am used to working with, I opted to take this `.db` file and convert it to a `.csv.gz` for the sake of working more comfortably.

<!-- Make sure update any file or folder names referenced here -->
The files in the `**insert folder**` can be used to convert the original SQLite file to a `.csv.gz`. This can be run locally if you would like to convert the data into `.csv.gz` or you can simply use the converted [found here](https://github.com/YoItsYong/billboard-200-pipeline/tree/main/data).

### Ingesting the Data
After getting the `billboard200_albums.csv.gz` file, we will then ingest the data using the `insert file name` in Mage where we can orechestrate the ingestion and loading to our Data Lake in Google Cloud Storage (GCS).

During this step, we also convert the file from `.csv.gz` to `.parquet` to take up less space on GCS.

### Processing the Data
Now that the data is available in GCS, we'll then set up a separate pipeline to take this data from GCS, process and transform using Apache Spark, and export the data to BigQuery.

To run Spark within Mage, we have shell commands in place to make sure our Mage instance is connected to Dataproc in Google Cloud. This allows us to run Spark without issue and move some of the processing load to the cloud.

```
df = spark.read.parquet('gs://bb200/bb200_albums.parquet')
```

### Tranforming the Data
Data transformations are performed using Python and SQL within Spark. These tranformations include:
- **Manage column data types:** ensure data types are correctly defined
```
df = df \
    .withColumn('date', df['date'].cast(DateType())) \
    .withColumn('rank', df['rank'].cast(IntegerType())) \
    .withColumn('length', df['length'].cast(IntegerType()))
```
- **Rename columns:** the column named 'length' seemed to ambiguous, so I had it changed to 'number_of_tracks'
```
df = df.withColumnRenamed('length', 'number_of_tracks')
```
- **Skip null values in first row:** the first row of data always returns null values. To avoid issues, I skip this row entirely.
```
df = df.filter(df.id > 1)
```
- **Handle other null values:** Some of the columns return null values based on the type of album that is charting.

    For example, many re-released albums were showing null for either of these columns. To avoid null value errors, I opted to set these to 0 by default.
```
df = df.na.fill(value=0, subset=['number_of_tracks'])
df = df.na.fill(value=0, subset=['track_length'])
```

After this, the data is automatically loaded to BigQuery where it is then pulled into Google Data Studio for visualization.

## Dashboard
The dashboard below pulls from BiqQuery and creates charts and tables for further analysis.

The tiles I've selected for this dashboard includes:
- The artist with most chart placements at number 1
- The percentage of number 1s each of the top-charting artists has
- The number of artists that chart year over year

## Future Improvements
While the current iteration of the pipeline is functional, there are some additional steps and precaution that could be taken to improve overall performance.
- Partition data in GCS: There is room to partition the data for better organization.
- Implement CI/CD: I haven't implemented any more formal CI/CD processes for pushing changes to the project, but this is something that I will likely explore in the future for a more realistic production environment.
- Additional Calculations: There are likely some additional calculated columns that could be incorporated.

## Reproducibility
The instructions below will help you set up the project environment and connect to cloud tools.
### Prerequisites

### Setup

### 

## References
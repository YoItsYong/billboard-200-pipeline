# Billboard 200 Pipeline
< Include banner image of some kind >
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
- Streamline File Conversion Process: I plan to also look at streamlining the current process of converting the original SQLite file and implementing it into 
- Additional Calculations: There are likely some additional calculated columns that could be incorporated.
- Partition Data in GCS: There is room to partition the data for better organization.
- Implement CI/CD: I haven't implemented any more formal CI/CD processes for pushing changes to the project, but this is something that I will likely explore in the future for a more realistic p roduction environment.

## Reproducing the Project
The instructions below will help you set up the project environment and connect to cloud tools to reproduce the pipeline on your local machine.
### Prerequisites
- **Create Google Account:** Visit [cloud.google.com](https://cloud.google.com/?hl=en) and create a new Google account if you don't have one already
    - Create a new project
    - Create Service Account w/ Owner permissions
    -  Enable Google [Compute Engine Api](https://console.cloud.google.com/apis/library/compute.googleapis.com)
    - Download Service Account Key (JSON)
- **Install Terraform:** Follow [instructions here](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli) to install Terraform
### Using Terraform for Google Cloud Setup
First, we'll set up our Google Cloud Platform using Terraform. This makes it easier to ensure that the necessary storage resources are created.

Start by copying the `main.tf` and `variables.tf` in the [Terraform folder](link).

Within the `variables.tf`, replace the path to your Service Account Key file on your machine (as shown below).
```
variable "credentials" {
    description = "My Credentials"
    default = "./PATH/TO/GCS_KEY.json"
}
```
After adding the path to your Service Account Key, open a terminal and navigate to the `Terraform folder` on your machine and run the command below.
```
terraform init
```
Once the command above is complete, run this command.
```
terraform plan
```
Finally, we'll apply the changes to your Google Cloud Platform account.
```
terraform apply
```
### Configuring Google Cloud Platform
The Terraform files should have created a few resources within your Google Cloud Platform account.

Confirm the folllowing resources were created with their respective names.
- Google Cloud Platform Project = billboard-200-project
- Google Cloud Storage Bucket = bb200
- Google BigQuery Data Set = bb200_data
- Google Dataproc Cluster = music-chart-cluster

If any of these were not created created incorrectly, fix it manually.
### Configure Spark_Dataproc.py
After everything on Google Cloud is set up correctly, we'll configure the `spark_dataproc.py` file in `folder/`.

Replace the variables below with what matches your project.

```
# (Line 13) Replace with path to your Serivce Account Key
gcs_key = '/workspaces/billboard-200-pipeline/bb200-gcp-creds.json'

#(Line 30) Replace temp_gcs_bucket with the name of your temporary bucket in GCS
temp_gcs_bucket = 'dataproc-temp-us-central1-968744273040-pk1v5m8n'
spark.conf.set('temporaryGcsBucket', temp_gcs_bucket)
```

After updating these variables, we'll upload them to a the folder called `code` within your GCS bucket.

### Docker/Mage Image Setup
Next, we'll be setting up Mage within Docker using the [Quickstart Guide](https://docs.mage.ai/getting-started/setup#get-mage) provided by Mage.

Using your terminal, `cd ..` until you're in your home directory and create a new directory called `mage`. Next, we'll run the command below to copy the quickstart repo to your own.
```
git clone https://github.com/mage-ai/compose-quickstart.git mage \
&& cd mage \
```

In the `mage` directory, we'll update a couple files before starting up our Mage Container
- In `dev.env`, rename the Mage Project to `bb200_project`
- In `requirements.txt`, add:
```
pyspark==3.5.1
pyarrow==15.0.2
```

Next, run the following commands:
```
cp dev.env .env && rm dev.env
docker compose up
```

Your Mage instance should now be live on `localhost:6789`.
### Install Google Cloud CLI
Within the Mage UI, click on the `Terminal` button on the side menu as shown below.

< insert image >

Our goal is to run the Google Cloud CLI to be able to use `gcloud` scripts within Mage.

We'll start with installing the Google Cloud CLI. First, run the scripts below to download, extract, and install the files in the Mage Terminal.

```
#Download Google Cloud CLI
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-471.0.0-linux-x86_64.tar.gz

#Extract Google Cloud CLI
tar -xf google-cloud-cli-471.0.0-linux-x86_64.tar.gz

#Install Google Cloud CLI
./google-cloud-sdk/install.sh
```
Next, we'll run the following script to authorize Mage to make changes to your Google Cloud account and make sure the Google Cloud CLI knows which project to make changes to.
```
#Authorize Google Cloud Login
./gsutil/google-cloud-sdk/bin/gcloud auth login

#Set Google Cloud Project
./gsutil/google-cloud-sdk/bin/gcloud config set project < INSERT PROJECT ID >
```

_Note: You may have to edit the script above depending on your folder structure._

### Create Pipeline to Google Cloud Storage
Our first pipeline will take the `billbaord200_albums_data` found [here](https://github.com/YoItsYong/billboard-200-pipeline/raw/main/data/billboard200_albums.csv.gz) and upload it to our Data Lake in Google Cloud Storage.

For this, you can copy and paste the `data_loader.py` and `data_exporter` files in `insert folder`. Your pipeline should look like this:

< insert image >

Before running the pipeline, make sure to replace `insert variable` with your `variable`.

This moves the data to Google Cloud Storage and converts the `.csv.gz` to `parquet` using `PyArrow`.
### Create Pipeline to BigQuery
Now that our `.parquet` files are available in GCS, we will now process and transform this data, move it over to our Data Warehouse in Google BigQuery.

For this, you can copy and paste the `data_loader.py` and `data_exporter` files in `insert folder`. Your pipeline should look like this:

< insert image >

Before running the pipeline, make sure to replace `insert variable` with your `variable`.

Running this pipeline loads data from GCS and performs the transformations using `Apache Spark`. The transformed data is then moved to our BigQuery where we can connect to it with Google Data Studio for visualizations.

### Create Visualizations in Google Data Studio
Open Google Data Studio and connect to BigQuery as your data source.

After this is added, you will be able to create tables, charts, and more to visualize the Billboard 200 data.

### Removing Resources
To avoid accruing costs on Google Cloud Platform, you can run the following command in your system terminal (not your Mage one) to breakdown the Terraform resources.
`terraform destroy`

## References